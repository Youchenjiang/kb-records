#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Entrypoint for Transcript Processor Toolkit
Supports standalone commands for cleaning, correcting, and building transcripts.
"""

import argparse
import sys
from pathlib import Path

from .cleaner import clean_transcript
from .corrector import CorrectionEngine
from .entity_guard import EntityGuard
from .asr import SafeASREngine
from .pipeline import TranscriptPipeline


def main():
    parser = argparse.ArgumentParser(
        description="Transcript Processor Toolkit: Modular ASR Cleaning, Correction & Summarization"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

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
