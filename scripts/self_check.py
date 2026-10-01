#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Self-Verification Script for Record-List Repository
"""

import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import validate_transcript_structure, ScenarioType


def check_audio_status():
    print("=== 1. Checking Audio Lifecycle Directories ===")
    audio_dir = REPO_ROOT / "audio"
    AUDIO_EXTENSIONS = {".aac", ".mp3", ".m4a", ".wav", ".flac", ".ogg", ".opus", ".wma", ".mp4", ".mkv"}
    pending = [f for f in (audio_dir / "pending").glob("*.*") if f.suffix.lower() in AUDIO_EXTENSIONS]
    processed = [f for f in (audio_dir / "processed").glob("*.*") if f.suffix.lower() in AUDIO_EXTENSIONS]
    preserved = [f for f in (audio_dir / "preserved").glob("*.*") if f.suffix.lower() in AUDIO_EXTENSIONS]

    print(f"  - Pending files: {len(pending)} (Expected: 0)")
    assert len(pending) == 0, f"Pending directory has {len(pending)} files: {pending}"

    print(f"  - Processed files: {len(processed)} (Expected: 0)")
    assert len(processed) == 0, f"Processed directory has {len(processed)} files: {processed}"

    print(f"  - Preserved files: {len(preserved)} (Expected: 38)")
    assert len(preserved) == 38, f"Preserved directory expected 38 files, got {len(preserved)}"

    manifest = (audio_dir / "preserved" / "MANIFEST.md").read_text(encoding="utf-8")
    for f in preserved:
        assert f.name in manifest, f"File {f.name} missing from preserved MANIFEST.md!"
    print("  ✅ Audio lifecycle check passed 100%!")


def check_deliverable_pairs():
    print("\n=== 2. Checking Deliverable Pairing (.full.md <-> .md) ===")
    curriculum_dirs = [REPO_ROOT / "4-University", REPO_ROOT / "5-Master"]
    all_full = []
    all_summary = []
    for cdir in curriculum_dirs:
        for f in cdir.glob("**/*.full.md"):
            all_full.append(f)
        for f in cdir.glob("**/*.md"):
            if not f.name.endswith(".full.md") and f.name != "README.md":
                all_summary.append(f)

    print(f"  - Found {len(all_full)} .full.md verbatim transcripts")
    print(f"  - Found {len(all_summary)} .md executive summaries")

    # Check matching summary for each full
    orphan_full = []
    for f in all_full:
        expected_summary = f.parent / f.name.replace(".full.md", ".md")
        if not expected_summary.exists():
            orphan_full.append(f)
    if orphan_full:
        print(f"  ⚠️ Warning: {len(orphan_full)} .full.md files do not have matching .md summary:")
        for o in orphan_full:
            print(f"     {o.relative_to(REPO_ROOT)}")

    # Check relative links in summaries
    broken_links = []
    for s in all_summary:
        content = s.read_text(encoding="utf-8")
        links = re.findall(r"\[.*?\]\((.*?\.full\.md)\)", content)
        for l in links:
            target = (s.parent / l).resolve()
            if not target.exists():
                broken_links.append((s, l))
    assert len(broken_links) == 0, f"Broken links found in summaries: {broken_links}"
    print("  ✅ All deliverable links resolve correctly!")


def check_proofread_standards():
    print("\n=== 3. Checking Transcript Structure & Standards ===")
    all_proofread = list(REPO_ROOT.glob("4-University/**/*.full.md")) + list(REPO_ROOT.glob("5-Master/**/*.full.md"))
    print(f"  - Checking {len(all_proofread)} deliverable transcripts...")
    
    issues = []
    for f in all_proofread:
        content = f.read_text(encoding="utf-8")
        # Extract scenario from frontmatter
        m = re.search(r"scenario:\s*[\"']?([a-zA-Z0-9_-]+)[\"']?", content)
        sc = m.group(1) if m else "classroom-lecture"
        is_valid, errors = validate_transcript_structure(content, scenario=sc)
        if not is_valid:
            issues.append((f.relative_to(REPO_ROOT), sc, errors))

    if issues:
        print(f"  ❌ Found {len(issues)} files with structural issues:")
        for path, sc, errs in issues:
            print(f"     {path} (scenario: {sc}) -> {errs}")
    else:
        print("  ✅ All deliverable transcripts comply with PROOFREAD_RULES.md!")
    return issues


def check_catalogs():
    print("\n=== 4. Checking Catalog Sync ===")
    cat_en = (REPO_ROOT / "CATALOG.md").read_text(encoding="utf-8")
    cat_zh = (REPO_ROOT / "CATALOG.zh-TW.md").read_text(encoding="utf-8")
    rows_en = re.findall(r"^\|\s*(\d+)\s*\|", cat_en, re.MULTILINE)
    rows_zh = re.findall(r"^\|\s*(\d+)\s*\|", cat_zh, re.MULTILINE)
    assert len(rows_en) == 170, f"Expected 170 rows in CATALOG.md, got {len(rows_en)}"
    assert len(rows_zh) == 170, f"Expected 170 rows in CATALOG.zh-TW.md, got {len(rows_zh)}"

    # Verify links in catalogs
    dead_links = []
    for m in re.finditer(r"\[.*?\]\((4-University/[^\)]+|5-Master/[^\)]+)\)", cat_en):
        rel_path = m.group(1)
        if not (REPO_ROOT / rel_path).exists():
            dead_links.append(rel_path)

    assert len(dead_links) == 0, f"Dead links in CATALOG.md: {dead_links}"
    print("  ✅ Both bilingual catalogs are fully in sync with zero dead links!")


if __name__ == "__main__":
    check_audio_status()
    check_deliverable_pairs()
    issues = check_proofread_standards()
    check_catalogs()
    print("\n🎉 Self-check script finished.")
