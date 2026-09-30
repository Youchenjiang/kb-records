#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Entrypoint for Transcript Processor Toolkit
Supports standalone commands for cleaning, correcting, and building transcripts.
"""

import argparse
import json
import sys
from pathlib import Path

from .cleaner import clean_transcript
from .corrector import CorrectionEngine
from .entity_guard import EntityGuard
from .asr import SafeASREngine
from .indexer import CatalogIndexer
from .pipeline import TranscriptPipeline
from .audio_manager import AudioManager
from .splitter import TranscriptSplitter, SplitSegmentConfig


def main():
    parser = argparse.ArgumentParser(
        description="Transcript Processor Toolkit: Modular ASR Cleaning, Correction & Summarization"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Command: audio
    audio_parser = subparsers.add_parser("audio", help="Manage audio staging lifecycle (pending/processed)")
    audio_subparsers = audio_parser.add_subparsers(dest="audio_action", help="Audio actions")

    # audio status
    audio_subparsers.add_parser("status", help="Show audio files and disk usage in pending & processed")

    # audio finish <file_pattern>
    finish_parser = audio_subparsers.add_parser("finish", help="Move audio file(s) from pending to processed")
    finish_parser.add_argument("target", type=str, help="Filename or glob pattern to move to processed")

    # audio import <source_file>
    import_parser = audio_subparsers.add_parser("import", help="Import audio file into audio/pending/")
    import_parser.add_argument("source", type=str, help="Source audio file to stage into pending")

    # audio clean [--yes]
    clean_audio_parser = audio_subparsers.add_parser("clean", help="Clean up (delete) all audio files in audio/processed/ to free disk space")
    clean_audio_parser.add_argument("--yes", "-y", action="store_true", help="Confirm deletion without prompting")

    # Command: index
    index_parser = subparsers.add_parser("index", help="Automatically scan and regenerate CATALOG.md and CATALOG.zh-TW.md")
    index_parser.add_argument("--root", type=str, default=".", help="Root directory to scan (default: current directory)")
    index_parser.add_argument("--out-en", type=str, default="CATALOG.md", help="English catalog output path (default: CATALOG.md)")
    index_parser.add_argument("--out-zh", type=str, default="CATALOG.zh-TW.md", help="Chinese catalog output path (default: CATALOG.zh-TW.md)")

    # Command: split
    split_parser = subparsers.add_parser("split", help="Inspect and split mixed transcripts into independent deliverables")
    split_subparsers = split_parser.add_subparsers(dest="split_action", help="Split actions")

    # split inspect <file>
    inspect_parser = split_subparsers.add_parser("inspect", help="Inspect ## section boundaries in transcript")
    inspect_parser.add_argument("file", type=str, help="Path to transcript file")

    # split run <config_file>
    split_run_parser = split_subparsers.add_parser("run", help="Execute transcript splitting from JSON config")
    split_run_parser.add_argument("config", type=str, help="Path to split config JSON file")

    # Command: clean
    clean_parser = subparsers.add_parser("clean", help="Normalize CJK spacing and punctuation")
    clean_parser.add_argument("input_file", type=str, help="Path to raw transcript file")
    clean_parser.add_argument("-o", "--output", type=str, help="Path to output file (default: stdout)")

    # Command: correct
    correct_parser = subparsers.add_parser("correct", help="Clean text and apply domain vocabulary corrections")
    correct_parser.add_argument("input_file", type=str, help="Path to raw transcript file")
    correct_parser.add_argument(
        "-d",
        "--domains",
        nargs="+",
        default=["common", "hitcon", "microsoft", "academic"],
        help="Domains to apply (default: common hitcon microsoft academic)",
    )
    correct_parser.add_argument("-o", "--output", type=str, help="Path to output file (default: stdout)")

    # Command: entity-check
    entity_parser = subparsers.add_parser("entity-check", help="Extract proper noun candidates and generate verification report")
    entity_parser.add_argument("input_file", type=str, help="Path to raw transcript file")
    entity_parser.add_argument("-o", "--output", type=str, help="Path to output report markdown file (default: stdout)")

    # Command: vram-info
    subparsers.add_parser("vram-info", help="Display GPU / VRAM safety parameters and memory status")

    # Command: info
    subparsers.add_parser("info", help="Display registered correction domains and rule counts")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "index":
        indexer = CatalogIndexer(root_dir=Path(args.root))
        count, en_path, zh_path = indexer.update_catalog_files(
            output_en=Path(args.out_en),
            output_zh=Path(args.out_zh),
        )
        print(f"✅ Catalog successfully generated: {count} sessions indexed.")
        print(f"   - English Catalog: {en_path}")
        print(f"   - Chinese Catalog: {zh_path}")
        sys.exit(0)

    if args.command == "info":
        engine = CorrectionEngine()
        print("=== Registered Correction Domains ===")
        for d, rules in engine.domains.items():
            print(f"Domain [{d}]: {len(rules)} substitution rules")
        sys.exit(0)

    if args.command == "vram-info":
        asr = SafeASREngine()
        info = asr.get_vram_info()
        print("=== ASR Hardware & VRAM Safety Info ===")
        for k, v in info.items():
            print(f"{k}: {v}")
    if args.command == "audio":
        manager = AudioManager()
        if not args.audio_action or args.audio_action == "status":
            status = manager.get_status()
            print("=== 🎙️ Audio Lifecycle Status ===")
            print(f"📥 Pending (待處理): {status['pending']['count']} files ({status['pending']['total_mb']} MB)")
            for f in status['pending']['files']:
                print(f"   - {f['name']} ({f['size_mb']} MB)")
            print(f"📦 Processed (已交付/可刪除): {status['processed']['count']} files ({status['processed']['total_mb']} MB)")
            for f in status['processed']['files']:
                print(f"   - {f['name']} ({f['size_mb']} MB)")
            sys.exit(0)

        elif args.audio_action == "finish":
            moved = manager.mark_as_processed(args.target)
            if moved:
                print(f"✅ Moved {len(moved)} file(s) to audio/processed/:")
                for m in moved:
                    print(f"   - {m.name}")
            else:
                print(f"⚠️ No matching audio files found for: {args.target}")
            sys.exit(0)

        elif args.audio_action == "import":
            try:
                dest = manager.import_to_pending(args.source)
                print(f"✅ Imported audio to pending: {dest.name}")
            except Exception as e:
                print(f"❌ Error: {e}", file=sys.stderr)
                sys.exit(1)
            sys.exit(0)

        elif args.audio_action == "clean":
            status = manager.get_status()
            count = status['processed']['count']
            mb = status['processed']['total_mb']
            if count == 0:
                print("ℹ️ audio/processed/ is already empty.")
                sys.exit(0)
            if not args.yes:
                confirm = input(f"⚠️ Are you sure you want to delete {count} files in audio/processed/ freeing {mb} MB? [y/N]: ")
                if confirm.lower() != "y":
                    print("Aborted.")
                    sys.exit(0)
            c, freed = manager.clean_processed(dry_run=False)
            print(f"🧹 Successfully cleaned {c} files, freed {freed} MB.")
            sys.exit(0)

    if args.command == "split":
        splitter = TranscriptSplitter()
        if not args.split_action or args.split_action == "inspect":
            target_f = Path(args.file)
            if not target_f.exists():
                print(f"Error: File not found: {target_f}", file=sys.stderr)
                sys.exit(1)
            sections = splitter.inspect_sections(target_f)
            print(f"=== Sections found in {target_f.name} ({len(sections)}) ===")
            for s in sections:
                print(f"Line {s['line']:4d}: {s['header']}")
            sys.exit(0)
        elif args.split_action == "run":
            cfg_p = Path(args.config)
            if not cfg_p.exists():
                print(f"Error: Config file not found: {cfg_p}", file=sys.stderr)
                sys.exit(1)
            cfg_data = json.loads(cfg_p.read_text(encoding="utf-8"))
            full_src = cfg_data["source_full_md"]
            sum_src = cfg_data.get("source_summary_md")
            segments = [
                SplitSegmentConfig(**seg)
                for seg in cfg_data["segments"]
            ]
            created = splitter.split_transcript(full_src, segments, summary_md_path=sum_src)
            print(f"✅ Successfully split into {len(created)} segment deliverables:")
            for full_p, sum_p in created:
                print(f"   - Full: {full_p}")
                if sum_p:
                    print(f"     Summary: {sum_p}")
            sys.exit(0)

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    raw_text = input_path.read_text(encoding="utf-8")

    if args.command == "clean":
        result = clean_transcript(raw_text)
    elif args.command == "correct":
        engine = CorrectionEngine()
        cleaned = clean_transcript(raw_text)
        result = engine.correct(cleaned, domains=args.domains)
    elif args.command == "entity-check":
        guard = EntityGuard()
        candidates = guard.extract_candidates(raw_text)
        result = guard.generate_verification_report(candidates)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
        print(f"Result written to {out_path} ({len(result)} characters)")
    else:
        print(result)



if __name__ == "__main__":
    main()
