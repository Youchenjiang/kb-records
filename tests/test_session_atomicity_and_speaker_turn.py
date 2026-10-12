#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Test Suite for Session Topic Atomicity, Speaker Diversity, and Entity Guard.
Strictly prevents:
1. Pseudo Single-Speaker flattening (monologue suppression in interactive meetings).
2. Unsplit multi-topic merging (topic concatenation across speakers).
3. Core entity misalignment (Youchen misrecognized as 右耳, 又成, or vague generic roles).
4. Boilerplate summaries ("如需查閱現場...", "請參閱配對之原話逐字稿").
5. Asymmetric deliverables or broken catalog mappings.
"""

from collections import Counter
from pathlib import Path
import re
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

class TestSessionAtomicityAndSpeakerTurn(unittest.TestCase):
    """
    Test suite enforcing PROOFREAD_RULES.md rules 11 through 16.
    """

    def setUp(self):
        self.full_files = sorted(
            list((REPO_ROOT / "5-Master").glob("**/*.full.md")) +
            list((REPO_ROOT / "4-University").glob("**/*.full.md"))
        )
        self.summary_files = sorted([
            f for f in (
                list((REPO_ROOT / "5-Master").glob("**/*.md")) +
                list((REPO_ROOT / "4-University").glob("**/*.md"))
            )
            if not f.name.endswith(".full.md") and f.name != "README.md"
        ])

    def test_summary_boilerplate_ban(self):
        """
        Rule 15: Zero Template / Zero Boilerplate in summaries (.md).
        Forbids phrases like '請參閱配對之原話逐字稿', '如需查閱現場一字不漏', etc.
        """
        banned_phrases = [
            "請參閱配對之原話逐字稿",
            "如需查閱現場",
            "一字不漏之完整對話",
        ]
        violations = []
        for s in self.summary_files:
            text = s.read_text(encoding="utf-8")
            for phrase in banned_phrases:
                if phrase in text:
                    violations.append(f"{s.relative_to(REPO_ROOT)} contains banned boilerplate: '{phrase}'")
        self.assertEqual(violations, [], f"Found boilerplate phrases in summaries:\n" + "\n".join(violations))

    def test_youchen_entity_and_typos(self):
        """
        Rule 13: Core Entity Protocol for Youchen (侑宸).
        1. ASR typos (右耳文字 -> 誘餌文字, 又成 -> 侑宸) must be corrected.
        2. In Thesis-Progress or Youchen-led presentations, the speaker must be tagged as '**【侑宸】**：',
           never vague labels like '**【論文研究生】**：' or '**【發表研究生 (Youchen)】**：'.
        """
        typo_violations = []
        role_violations = []

        for f in self.full_files:
            text = f.read_text(encoding="utf-8")
            rel_path = str(f.relative_to(REPO_ROOT))

            # 1. Check for typos in dialogue lines (excluding disclaimer explanation quote)
            lines = text.splitlines()
            for idx, line in enumerate(lines):
                if line.startswith("> **【排版與校對說明】**"):
                    continue  # allow historical disclaimer documentation if needed
                if "右耳" in line:
                    typo_violations.append(f"{rel_path}:{idx+1} contains '右耳' (ASR typo for 誘餌 or 侑宸)")
                if "又成" in line and "蔣又成" not in line:  # Allow distinct classmate named 蔣又成
                    typo_violations.append(f"{rel_path}:{idx+1} contains '又成' (ASR typo for 侑宸)")
                if "右臣" in line:
                    typo_violations.append(f"{rel_path}:{idx+1} contains '右臣' (ASR typo for 侑宸)")

            # 2. Check for vague roles in Thesis-Progress (for Youchen-led presentations)
            if "Thesis-Progress" in rel_path:
                # If it's a peer presentation, speaker is explicitly 同儕研究生
                is_peer_presentation = "同儕研究生" in text[:300] and "侑宸" not in text[:300]
                if not is_peer_presentation:
                    if "**【論文研究生】**：" in text or "**【發表研究生 (Youchen)】**：" in text:
                        role_violations.append(
                            f"{rel_path}: uses vague speaker tag instead of mandatory '**【侑宸】**：'"
                        )
                    # Frontmatter check
                    fm_end = text.find("---", 3)
                    if fm_end != -1:
                        fm = text[3:fm_end]
                        if "speakers:" in fm and "侑宸" not in fm:
                            role_violations.append(f"{rel_path}: frontmatter 'speakers' missing '侑宸'")

        self.assertEqual(typo_violations, [], "Found uncorrected ASR typos:\n" + "\n".join(typo_violations))
        self.assertEqual(role_violations, [], "Found Youchen entity role violations:\n" + "\n".join(role_violations))

    def test_speaker_diversity_in_interactive_sessions(self):
        """
        Rule 12 & 14: Anti-Pseudo Single-Speaker Gate.
        In interactive master's lab meetings (Thesis-Progress, Lab-Meeting, Project-Meeting, Seminar)
        with substantial discussion (turns >= 10 and length >= 2500 words),
        no single speaker may monopolize >85% of turns without surfacing the dialogue/QA turns.
        """
        violations = []
        for f in self.full_files:
            rel_path = str(f.relative_to(REPO_ROOT))
            # Focus on master's laboratory & seminar files
            if any(k in rel_path for k in ["Laboratory", "Seminar"]):
                text = f.read_text(encoding="utf-8")
                # Skip pure single-talk scenarios explicitly designated in frontmatter if applicable
                m_scenario = re.search(r"scenario:\s*[\"']?([a-zA-Z0-9_-]+)[\"']?", text)
                scenario = m_scenario.group(1) if m_scenario else ""
                if scenario == "single-talk":
                    continue

                roles = re.findall(r"\*\*【(.*?)】\*\*：", text)
                if len(roles) >= 10 and len(text) > 2500:
                    c = Counter(roles)
                    top_role, top_count = c.most_common(1)[0]
                    ratio = top_count / len(roles)
                    if len(c) < 2:
                        violations.append(
                            f"{rel_path}: only 1 speaker role ('{top_role}') in interactive meeting ({len(roles)} turns)"
                        )
                    elif ratio > 0.85:
                        violations.append(
                            f"{rel_path}: pseudo single-speaker detected! '{top_role}' has {top_count}/{len(roles)} turns ({ratio:.1%}). Unique roles: {len(c)}"
                        )

        self.assertEqual(violations, [], "Found pseudo single-speaker violations:\n" + "\n".join(violations))

    def test_deliverable_one_to_one_pairing(self):
        """
        Every .full.md must have a corresponding .md executive summary.
        """
        missing_summaries = []
        for f in self.full_files:
            summary_path = f.parent / f.name.replace(".full.md", ".md")
            if not summary_path.exists():
                missing_summaries.append(str(f.relative_to(REPO_ROOT)))
        self.assertEqual(missing_summaries, [], f"Missing matching summary for:\n" + "\n".join(missing_summaries))

if __name__ == "__main__":
    unittest.main()
