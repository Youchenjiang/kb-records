#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AAC to MP3 Audio Converter
High-performance batch audio converter for AAC / M4A / ADTS to MP3.
Supports single file, batch folder processing, multi-threading, custom bitrate, and metadata preservation.
"""

import argparse
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Tuple


def find_ffmpeg_executable() -> Optional[str]:
    """Find FFmpeg executable in PATH, imageio_ffmpeg, or common Windows install locations."""
    # 1. Check system PATH
    ffmpeg_in_path = shutil.which("ffmpeg")
    if ffmpeg_in_path:
        return ffmpeg_in_path

    # 2. Check imageio_ffmpeg if installed
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass

    # 3. Check common Windows paths
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links" / "ffmpeg.exe",
        Path("C:/ffmpeg/bin/ffmpeg.exe"),
        Path("C:/Program Files/ffmpeg/bin/ffmpeg.exe"),
        Path("C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe"),
        Path(os.environ.get("APPDATA", "")) / "npm" / "node_modules" / "ffmpeg-static" / "ffmpeg.exe",
    ]

    for candidate in candidates:
        if candidate.is_file() and os.access(str(candidate), os.X_OK):
            return str(candidate)

    return None


def convert_single_file(
    input_path: Path,
    output_path: Path,
    ffmpeg_bin: str,
    bitrate: str = "320k",
    sample_rate: Optional[int] = None,
    overwrite: bool = True,
) -> Tuple[bool, str]:
    """Convert a single AAC/M4A file to MP3 using FFmpeg."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            ffmpeg_bin,
            "-y" if overwrite else "-n",
            "-i", str(input_path),
            "-c:a", "libmp3lame",
            "-b:a", bitrate,
            "-map_metadata", "0",
            "-id3v2_version", "3",
        ]

        if sample_rate:
            cmd.extend(["-ar", str(sample_rate)])

        cmd.append(str(output_path))

        # Run ffmpeg with hidden banner and log level error
        cmd.extend(["-hide_banner", "-loglevel", "error"])

        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        if proc.returncode != 0:
            return False, f"FFmpeg 錯誤: {proc.stderr.strip()}"

        return True, "成功"
    except Exception as e:
        return False, str(e)


def collect_audio_files(input_path: Path, recursive: bool = True) -> List[Path]:
    """Collect all AAC and related audio files from file or folder."""
    valid_exts = {".aac", ".m4a", ".adts", ".mp4", ".alac"}

    if input_path.is_file():
        if input_path.suffix.lower() in valid_exts or input_path.suffix.lower() == ".aac":
            return [input_path]
        return [input_path]

    if not input_path.is_dir():
        return []

    pattern = "**/*" if recursive else "*"
    files = [
        p for p in input_path.glob(pattern)
        if p.is_file() and p.suffix.lower() in valid_exts
    ]
    return sorted(files)


def batch_convert(
    input_paths: List[Path],
    output_dir: Optional[Path],
    ffmpeg_bin: str,
    bitrate: str = "320k",
    sample_rate: Optional[int] = None,
    overwrite: bool = True,
    threads: int = 4,
    base_input_dir: Optional[Path] = None,
) -> None:
    """Batch convert audio files with progress indicator and multithreading."""
    total = len(input_paths)
    if total == 0:
        print("⚠ 未找到任何符合條件的音訊檔案 (.aac, .m4a)。")
        return

    print(f"🎵 找到 {total} 個音訊檔案，開始轉檔為 MP3 (位元率: {bitrate})...")
    success_count = 0
    fail_count = 0

    tasks = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for file_path in input_paths:
            if output_dir:
                if base_input_dir and file_path.is_relative_to(base_input_dir):
                    rel_path = file_path.relative_to(base_input_dir)
                    target_file = output_dir / rel_path.with_suffix(".mp3")
                else:
                    target_file = output_dir / f"{file_path.stem}.mp3"
            else:
                target_file = file_path.with_suffix(".mp3")

            future = executor.submit(
                convert_single_file,
                file_path,
                target_file,
                ffmpeg_bin,
                bitrate=bitrate,
                sample_rate=sample_rate,
                overwrite=overwrite,
            )
            tasks.append((future, file_path, target_file))

        for idx, (future, src, dst) in enumerate(tasks, 1):
            ok, msg = future.result()
            if ok:
                success_count += 1
                print(f"[{idx}/{total}] ✔ {src.name} -> {dst.name}")
            else:
                fail_count += 1
                print(f"[{idx}/{total}] ❌ {src.name} 失敗: {msg}")

    print("\n" + "=" * 50)
    print(f"🎉 轉換完成！成功: {success_count} 筆，失敗: {fail_count} 筆")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="AAC to MP3 高效音訊轉檔工具 (支援單檔、資料夾批次、多執行緒與自訂位元率)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:
  python aac_to_mp3.py --input song.aac
  python aac_to_mp3.py --input song.aac --output converted_song.mp3 --bitrate 320k
  python aac_to_mp3.py --input ./music_folder --output ./mp3_folder --recursive --threads 8
        """,
    )

    parser.add_argument("-i", "--input", required=True, help="輸入 AAC 檔案或資料夾路徑")
    parser.add_argument("-o", "--output", help="輸出 MP3 檔案或目標資料夾路徑 (選填，預設同位置)")
    parser.add_argument("-b", "--bitrate", default="320k", help="輸出 MP3 音訊位元率 (預設: 320k，可選 128k, 192k, 256k, 320k)")
    parser.add_argument("-r", "--recursive", action="store_true", default=True, help="是否遞迴搜尋子目錄 (預設: True)")
    parser.add_argument("-t", "--threads", type=int, default=4, help="並行轉檔執行緒數量 (預設: 4)")
    parser.add_argument("--sample-rate", type=int, help="自訂取樣率 Hz (例如 44100, 48000)")
    parser.add_argument("--no-overwrite", action="store_true", help="若目標檔案已存在則略過不覆寫")
    parser.add_argument("--ffmpeg-path", help="手動指定 FFmpeg 執行檔路徑")

    args = parser.parse_args()

    ffmpeg_bin = args.ffmpeg_path or find_ffmpeg_executable()
    if not ffmpeg_bin:
        print("❌ 錯誤: 未找到 FFmpeg 執行檔！")
        print("\n💡 解決方案:")
        print("  1. 透過 pip 自動安裝 (推薦，免手動設定環境變數):")
        print("     pip install imageio-ffmpeg")
        print("  2. 或透過 winget 安裝 FFmpeg:")
        print("     winget install Gyan.FFmpeg")
        print("  3. 或在執行時透過 --ffmpeg-path 指定 ffmpeg.exe 路徑")
        sys.exit(1)

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"❌ 錯誤: 輸入路徑不存在: {input_path}")
        sys.exit(1)

    output_path = Path(args.output).resolve() if args.output else None

    if input_path.is_file():
        target_output = output_path or input_path.with_suffix(".mp3")
        print(f"🎵 正在轉換: {input_path.name} -> {target_output.name} (位元率: {args.bitrate})")
        ok, msg = convert_single_file(
            input_path,
            target_output,
            ffmpeg_bin,
            bitrate=args.bitrate,
            sample_rate=args.sample_rate,
            overwrite=not args.no_overwrite,
        )
        if ok:
            print(f"✔ 轉換成功: {target_output}")
        else:
            print(f"❌ 轉換失敗: {msg}")
            sys.exit(1)
    else:
        # Folder batch processing
        audio_files = collect_audio_files(input_path, recursive=args.recursive)
        batch_convert(
            audio_files,
            output_dir=output_path,
            ffmpeg_bin=ffmpeg_bin,
            bitrate=args.bitrate,
            sample_rate=args.sample_rate,
            overwrite=not args.no_overwrite,
            threads=args.threads,
            base_input_dir=input_path,
        )


if __name__ == "__main__":
    main()
