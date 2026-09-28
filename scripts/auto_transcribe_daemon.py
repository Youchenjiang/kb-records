#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Audio Transcription Daemon
- Continuously watches audio/pending/ for new audio files.
- Processes audio in FIFO order (earliest copied first).
- Verifies file size stability to ensure file copy is complete before processing.
- Uses Qwen3-ASR-1.7B with strict VRAM cap (65% ~ 5.2GB) to protect Windows DWM / RDP.
- Converts to Traditional Chinese (OpenCC s2twp) and generates proofread markdown.
- Automatically moves finished audio from audio/pending/ to audio/processed/.
- Stays alive to automatically detect and transcribe newly arriving audio files.
"""

import os
import sys
import time
import shutil
import logging
from pathlib import Path
from typing import List, Optional, Tuple

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

import av
import numpy as np
import torch
from opencc import OpenCC
from qwen_asr.inference.qwen3_asr import Qwen3ASRModel

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("safe_transcribe.log", encoding="utf-8", mode="a"),
    ],
)
logger = logging.getLogger("AutoTranscribeDaemon")

MODEL_PATH = r"C:\Users\g1014308\.cache\modelscope\hub\models\Qwen\Qwen3-ASR-1___7B"
CHUNK_SECONDS = 60
AUDIO_EXTENSIONS = {".aac", ".mp3", ".m4a", ".wav", ".flac", ".ogg", ".opus", ".wma"}

REPO_ROOT = Path(__file__).resolve().parent.parent
PENDING_DIR = REPO_ROOT / "audio" / "pending"
PROCESSED_DIR = REPO_ROOT / "audio" / "processed"
OUTPUT_BASE_DIR = REPO_ROOT / "transcribe_outputs"


def setup_gpu_safety():
    """Cap GPU VRAM to 65% to protect Windows DWM and Remote Desktop."""
    if torch.cuda.is_available():
        torch.cuda.set_per_process_memory_fraction(0.65, device=0)
        logger.info("GPU VRAM safety limit applied: Hard-capped at 65% (max ~5.2 GB).")


def is_file_ready(file_path: Path) -> bool:
    """
    Check if a file has finished being copied.
    Verifies that the file can be opened and its size is stable across 2 seconds.
    """
    try:
        if not file_path.exists():
            return False
        # Test open
        with open(file_path, "rb") as f:
            f.read(1024)
        s1 = file_path.stat().st_size
        time.sleep(2)
        s2 = file_path.stat().st_size
        return s1 == s2 and s1 > 0
    except (PermissionError, OSError):
        return False


def get_pending_queue() -> List[Path]:
    """
    Find all audio files in PENDING_DIR recursively, sorted by modification time (FIFO).
    """
    if not PENDING_DIR.exists():
        return []

    candidates = [
        f for f in PENDING_DIR.rglob("*")
        if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
    ]
    # Sort by modification time ascending (earliest first)
    candidates.sort(key=lambda x: x.stat().st_mtime)
    return candidates


def decode_audio_full(file_path: Path, target_sr: int = 16000) -> Tuple[np.ndarray, int]:
    """Decode audio file to 16kHz mono float32 array via PyAV packet-level demux with glitch tolerance."""
    logger.info(f"Decoding audio: {file_path.name}...")
    t0 = time.time()
    container = av.open(str(file_path))
    stream = container.streams.audio[0]
    resampler = av.AudioResampler(format="s16", layout="mono", rate=target_sr)

    samples = []
    bad_packets = 0
    for packet in container.demux(stream):
        try:
            for frame in packet.decode():
                for rf in resampler.resample(frame):
                    samples.append(rf.to_ndarray().flatten())
        except (av.error.FFmpegError, ValueError, Exception) as e:
            bad_packets += 1
            continue
    container.close()

    if not samples:
        raise RuntimeError(f"Failed to decode any valid audio frames from {file_path.name}")

    audio = np.concatenate(samples).astype(np.float32) / 32768.0
    dur = len(audio) / target_sr
    logger.info(f"Decoded {dur:.1f}s ({dur/60.0:.2f} min) in {time.time()-t0:.2f}s (skipped {bad_packets} bad packets)")
    return audio, target_sr


def transcribe_single_audio(
    model: Qwen3ASRModel,
    cc: OpenCC,
    audio_path: Path,
) -> bool:
    """
    Transcribe a single audio file and move it to audio/processed/.
    """
    file_name = audio_path.stem
    out_dir = OUTPUT_BASE_DIR / file_name
    out_dir.mkdir(parents=True, exist_ok=True)

    proofread_path = out_dir / f"{file_name}-proofread.md"
    raw_txt_path = out_dir / "raw_transcript.txt"
    tw_txt_path = out_dir / "transcript_zh_tw.txt"

    # If already fully processed before, skip transcription
    if proofread_path.exists() and proofread_path.stat().st_size > 500:
        logger.info(f"[{file_name}] Transcript already exists. Moving audio to processed/ directly.")
        dest = PROCESSED_DIR / audio_path.name
        shutil.move(str(audio_path), str(dest))
        return True

    # Decode audio
    audio, sr = decode_audio_full(audio_path)
    total_samples = len(audio)
    total_sec = total_samples / sr
    chunk_samples = CHUNK_SECONDS * sr
    total_chunks = int(np.ceil(total_samples / chunk_samples))

    logger.info(f"[{file_name}] Total Duration: {total_sec/60.0:.2f} min | Chunks: {total_chunks}")

    raw_chunks_text = []
    t_start = time.time()

    for idx in range(total_chunks):
        start_samp = idx * chunk_samples
        end_samp = min((idx + 1) * chunk_samples, total_samples)
        chunk_wav = audio[start_samp:end_samp]

        # Inference
        res = model.transcribe((chunk_wav, sr), language="Chinese")
        chunk_text = res[0].text if res else ""
        raw_chunks_text.append(chunk_text)

        if idx % 5 == 0:
            torch.cuda.empty_cache()

        elapsed = time.time() - t_start
        chunks_done = idx + 1
        avg_chunk_time = elapsed / chunks_done
        eta_sec = (total_chunks - chunks_done) * avg_chunk_time

        logger.info(
            f"[{file_name}] Chunk {chunks_done}/{total_chunks} ({chunks_done/total_chunks*100:.1f}%) "
            f"| ETA: {eta_sec/60:.1f}m | Text: {chunk_text[:30]}..."
        )

        # Progressive backup save
        raw_txt_path.write_text("".join(raw_chunks_text), encoding="utf-8")

    total_time = time.time() - t_start
    raw_full = "".join(raw_chunks_text)
    raw_txt_path.write_text(raw_full, encoding="utf-8")

    # Traditional Chinese conversion
    tw_full = cc.convert(raw_full)
    tw_txt_path.write_text(tw_full, encoding="utf-8")

    # Formatted Markdown
    paragraphs = [
        p.strip()
        for p in tw_full.replace("。", "。\n\n").replace("！", "！\n\n").replace("？", "？\n\n").split("\n\n")
        if p.strip()
    ]
    formatted_body = "\n\n".join(paragraphs)

    md_content = f"""# 🎙️ {file_name} 逐字稿校對版

- **原始音檔**：`{audio_path.name}`
- **錄音時長**：{total_sec/60.0:.2f} 分鐘 ({int(total_sec)} 秒)
- **轉錄引擎**：Qwen3-ASR-1.7B (阿里滿血旗艦版，60秒滑動切片)
- **推論耗時**：{total_time/60.0:.2f} 分鐘 (RTF: {total_time/total_sec:.3f})
- **輸出語系**：臺灣繁體中文 (OpenCC s2twp)
- **校對狀態**：高精度無漂移自動轉錄完成

---

## 逐字記錄

{formatted_body}
"""
    proofread_path.write_text(md_content, encoding="utf-8")
    logger.info(f"[{file_name}] Successfully completed: {proofread_path}")

    # Move finished audio to processed/
    dest = PROCESSED_DIR / audio_path.name
    shutil.move(str(audio_path), str(dest))
    logger.info(f"[{file_name}] Moved audio to: {dest}")

    torch.cuda.empty_cache()
    return True


def run_daemon():
    """Main daemon loop watching audio/pending/ indefinitely."""
    setup_gpu_safety()
    OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Initializing OpenCC (s2twp)...")
    cc = OpenCC("s2twp")

    logger.info(f"Loading Qwen3-ASR-1.7B from {MODEL_PATH}...")
    t0 = time.time()
    model = Qwen3ASRModel.from_pretrained(
        MODEL_PATH,
        dtype=torch.bfloat16,
        device_map="cuda:0",
        max_inference_batch_size=1,
    )
    logger.info(f"Model loaded in {time.time()-t0:.2f}s | Daemon is active!")

    poll_interval = 15  # seconds
    while True:
        try:
            queue = get_pending_queue()
            if not queue:
                logger.info(f"Pending queue empty. Sleeping {poll_interval}s before next check...")
                time.sleep(poll_interval)
                continue

            logger.info(f"Found {len(queue)} pending audio file(s) in queue.")

            processed_any = False
            for audio_file in queue:
                if not is_file_ready(audio_file):
                    logger.info(f"File {audio_file.name} is currently being copied/written. Skipping for now.")
                    continue

                logger.info(f"\n{'='*70}\n>>> STARTING TRANSCRIPTION: {audio_file.name}\n{'='*70}")
                try:
                    transcribe_single_audio(model, cc, audio_file)
                    processed_any = True
                except Exception as e:
                    logger.error(f"Error processing {audio_file.name}: {e}", exc_info=True)

            if not processed_any:
                time.sleep(poll_interval)

        except KeyboardInterrupt:
            logger.info("Daemon interrupted by user. Shutting down gracefully.")
            break
        except Exception as e:
            logger.error(f"Unexpected daemon error: {e}", exc_info=True)
            time.sleep(10)


if __name__ == "__main__":
    run_daemon()
