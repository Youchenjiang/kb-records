#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path
from collections import Counter

REPO = Path(__file__).resolve().parent.parent

def run_audit():
    print(f"=== Auditing repository rules under {REPO} ===")
    full_files = sorted(list(REPO.glob("5-Master/**/*.full.md")) + list(REPO.glob("4-University/**/*.full.md")))
    summary_files = sorted([f for f in (list(REPO.glob("5-Master/**/*.md")) + list(REPO.glob("4-University/**/*.md"))) if not f.name.endswith(".full.md") and f.name != "README.md"])
    print(f"Total .full.md files: {len(full_files)}")
    print(f"Total .md summary files: {len(summary_files)}")

    # 1. Transition markers (Unsplit sessions)
    transitions = ["換下一位", "換我報告", "換下一組", "好謝謝上一位", "下一位換", "下一位同仁", "換下一個同學"]
    unsplit = []
    for f in full_files:
        text = f.read_text(encoding="utf-8")
        found = [t for t in transitions if t in text]
        if found:
            unsplit.append((f, found))
    print(f"\n[Check 1: Unsplit Topic Transitions] Found {len(unsplit)} files:")
    for f, t in unsplit:
        print(f"  - {f.relative_to(REPO)}: contains {t}")

    # 2. Speaker Diversity in Lab/Seminar
    dom_speakers = []
    for f in full_files:
        if any(k in str(f) for k in ["Laboratory", "Seminar"]):
            text = f.read_text(encoding="utf-8")
            roles = re.findall(r"\*\*【(.*?)】\*\*：", text)
            if len(roles) >= 10:
                c = Counter(roles)
                total = len(roles)
                top_role, top_count = c.most_common(1)[0]
                ratio = top_count / total
                if ratio > 0.85:
                    dom_speakers.append((f, top_role, top_count, total, ratio, len(c)))
    print(f"\n[Check 2: Dominant Speaker (>85% turns) in Lab/Seminar] Found {len(dom_speakers)} files:")
    for f, top_role, top_count, total, ratio, unique_c in dom_speakers:
        print(f"  - {f.relative_to(REPO)}: {top_role} has {top_count}/{total} ({ratio:.1%}), unique roles={unique_c}")

    # 3. Typos for Youchen
    typos = ["右耳", "又成", "右臣", "侑成", "又誠"]
    typo_files = []
    for f in full_files + summary_files:
        text = f.read_text(encoding="utf-8")
        found_typos = [t for t in typos if t in text]
        if found_typos:
            typo_files.append((f, found_typos))
    print(f"\n[Check 3: Youchen Typo Detection] Found {len(typo_files)} files:")
    for f, tps in typo_files:
        print(f"  - {f.relative_to(REPO)}: contains {tps}")

    # 4. Boilerplate phrases in summaries
    boilerplate_phrases = ["請參閱配對之原話逐字稿", "如需查閱現場", "一字不漏之完整對話"]
    bp_files = []
    for s in summary_files:
        text = s.read_text(encoding="utf-8")
        found_bp = [bp for bp in boilerplate_phrases if bp in text]
        if found_bp:
            bp_files.append((s, found_bp))
    print(f"\n[Check 4: Boilerplate in Summaries] Found {len(bp_files)} files:")
    for s, bps in bp_files:
        print(f"  - {s.relative_to(REPO)}: contains {bps}")

    # 5. Youchen identity alignment
    # If file is related to Youchen, speaker should be **【侑宸】**：
    yc_alignment = []
    for f in full_files:
        text = f.read_text(encoding="utf-8")
        if "侑宸" in text:
            # Check if **【侑宸】** exists
            has_yc_tag = "**【侑宸】**：" in text
            fm = text[:text.find("---", 3)] if text.startswith("---") else ""
            has_yc_fm = "侑宸" in fm
            if not has_yc_tag or not has_yc_fm:
                yc_alignment.append((f, has_yc_tag, has_yc_fm))
    print(f"\n[Check 5: Youchen Entity Alignment in full transcripts] Found {len(yc_alignment)} files:")
    for f, tag, fm in yc_alignment:
        print(f"  - {f.relative_to(REPO)}: has_tag={tag}, has_fm={fm}")

if __name__ == "__main__":
    run_audit()
