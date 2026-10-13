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

            # 2. Check Thesis-Progress: strictly reserved for Youchen's master thesis progress
            if "Thesis-Progress" in rel_path:
                if "**【侑宸】**：" not in text:
                    role_violations.append(
                        f"{rel_path}: Thesis-Progress is strictly reserved for Youchen's thesis progress! Must contain '**【侑宸】**：'"
                    )
                if "**【論文研究生】**：" in text or "**【發表研究生 (Youchen)】**：" in text:
                    role_violations.append(
                        f"{rel_path}: uses vague speaker tag instead of mandatory '**【侑宸】**：'"
                    )
                # Frontmatter check: speakers must contain 侑宸
                fm_end = text.find("---", 3)
                if fm_end != -1:
                    fm = text[3:fm_end]
                    if "speakers:" in fm and "侑宸" not in fm:
                        role_violations.append(f"{rel_path}: Thesis-Progress frontmatter 'speakers' missing '侑宸'")

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

    def test_filename_naming_conventions_and_banned_slugs(self):
        """
        Rule 0: Filename Naming Conventions & Banned Slugs.
        1. Date prefix must be 8 digits (YYYYMMDD), strictly no hyphens like YYYY-MM-DD.
        2. Strictly forbidden internal/hash slugs (e.g. Lesson-, NCU-IM-, Lab-Discovery).
        """
        banned_slugs = ["Lesson-", "NCU-IM-", "Lab-Discovery", "勤業眾信副總"]
        violations = []
        all_deliverables = self.full_files + self.summary_files

        for f in all_deliverables:
            name = f.name
            rel_path = str(f.relative_to(REPO_ROOT))

            # 1. Date format check: must start with 8 digits
            if re.match(r"^\d{4}-\d{2}-\d{2}", name):
                violations.append(f"{rel_path}: filename uses hyphenated date (YYYY-MM-DD), must use 8 digits (YYYYMMDD)")
            elif not re.match(r"^\d{8}", name):
                violations.append(f"{rel_path}: filename does not start with 8-digit date (YYYYMMDD)")

            # 2. Banned slugs check
            for slug in banned_slugs:
                if slug in name:
                    violations.append(f"{rel_path}: filename contains forbidden slug '{slug}'")

        self.assertEqual(violations, [], "Found filename convention violations:\n" + "\n".join(violations))

    def test_h2_heading_cleanliness(self):
        """
        Rule 3 & Structurer: Heading clean standards.
        H2 headings must not use artificial numbering like '一、', '二、', etc.
        """
        violations = []
        for f in self.full_files:
            text = f.read_text(encoding="utf-8")
            h2_matches = re.findall(r"^##\s+.*[一二三四五六七八九十]、", text, re.M)
            if h2_matches:
                rel_path = str(f.relative_to(REPO_ROOT))
                violations.append(f"{rel_path}: H2 headings contain artificial numbering: {h2_matches}")

        self.assertEqual(violations, [], "Found H2 artificial numbering violations:\n" + "\n".join(violations))

    def test_discourse_paragraph_length_boundaries(self):
        """
        Rule 2: Discourse Paragraphing Protocol (150-300 words).
        Strictly forbids huge unsegmented text blocks (>800 chars without newline) in body dialogue.
        """
        violations = []
        for f in self.full_files:
            text = f.read_text(encoding="utf-8")
            parts = text.split("---", 2)
            body = parts[2] if len(parts) >= 3 else text
            paras = body.split("\n\n")

            for idx, p in enumerate(paras):
                p_strip = p.strip()
                # Skip frontmatter, code blocks, tables, blockquotes, list blocks, headers
                if (
                    p_strip.startswith("```") or
                    p_strip.startswith("|") or
                    p_strip.startswith("- ") or
                    p_strip.startswith("1. ") or
                    p_strip.startswith(">") or
                    p_strip.startswith("#")
                ):
                    continue
                if len(p_strip) > 800:
                    rel_path = str(f.relative_to(REPO_ROOT))
                    violations.append(
                        f"{rel_path}: huge paragraph block ({len(p_strip)} chars) exceeding 800-char boundary: '{p_strip[:40]}...'"
                    )

        self.assertEqual(violations, [], "Found excessive text blocks violating paragraph boundaries:\n" + "\n".join(violations))

    def test_unsplit_transition_markers_in_single_topic_sessions(self):
        """
        Rule 11: Session Topic Atomicity in Academic Meetings.
        In laboratory, thesis progress, seminar, and defense meetings,
        inter-speaker transition markers (e.g. '謝謝上一位', '換下一組', '下一位換誰')
        signal unsplit topics and must be partitioned into independent sessions.
        """
        transition_markers = [
            "謝謝上一位",
            "換下一組",
            "下一位換",
            "接下來請下一位",
            "換下一個同學",
        ]
        violations = []
        for f in self.full_files:
            rel_path = str(f.relative_to(REPO_ROOT))
            # Focus on dedicated single-topic research meetings
            if any(k in rel_path for k in ["Laboratory", "Thesis-Progress", "Seminar", "Degree-Defense"]):
                text = f.read_text(encoding="utf-8")
                for marker in transition_markers:
                    if marker in text:
                        violations.append(f"{rel_path}: contains unsplit topic transition marker '{marker}'")

        self.assertEqual(violations, [], "Found unsplit topic transition markers in single-topic meetings:\n" + "\n".join(violations))

    # Explicit ratchet lists for staged remediation (Phase A: .full.md first; Phase B: .md summaries second).
    # Set environment variable STRICT_FULL_AUDIT=1 to bypass the ratchet and view all remaining items.
    PHASE_A_PENDING_PREFIXES = ()
    PHASE_B_PENDING_PREFIXES = (
        "5-Master\\2-Second-Year",
        "5-Master\\1-First-Year",
        "5-Master\\Archive",
        "4-University",
    )

    @classmethod
    def _is_phase_a_pending(cls, rel_path: str) -> bool:
        import os
        if os.environ.get("STRICT_FULL_AUDIT") == "1":
            return False
        norm = rel_path.replace("/", "\\")
        return any(norm.startswith(p) for p in cls.PHASE_A_PENDING_PREFIXES)

    @classmethod
    def _is_phase_b_pending(cls, rel_path: str) -> bool:
        import os
        if os.environ.get("STRICT_FULL_AUDIT") == "1":
            return False
        norm = rel_path.replace("/", "\\")
        return any(norm.startswith(p) for p in cls.PHASE_B_PENDING_PREFIXES)

    def test_laboratory_five_subdirectory_taxonomy(self):
        """
        Rule 0.2: 5-Master/Laboratory/ must strictly contain only the 5 canonical subdirectories:
        Degree-Defense, Project-Meeting, Security-News, Seminar, Thesis-Progress.
        """
        if self._is_phase_a_pending("5-Master\\Laboratory"):
            return
        allowed_subdirs = {
            "Degree-Defense",
            "Project-Meeting",
            "Security-News",
            "Seminar",
            "Thesis-Progress",
        }
        lab_dir = REPO_ROOT / "5-Master" / "Laboratory"
        actual_subdirs = {p.name for p in lab_dir.iterdir() if p.is_dir()}
        unexpected = sorted(actual_subdirs - allowed_subdirs)
        self.assertEqual(
            unexpected,
            [],
            f"Found non-canonical subdirectories under 5-Master/Laboratory/: {unexpected}. Allowed: {sorted(allowed_subdirs)}",
        )

    def test_full_transcript_semantic_chapter_segmentation(self):
        """
        Rule 18: Semantic Chapter Segmentation & Density Protocol for .full.md.
        1. Bans mechanical placeholder H2s ('章節段落 01', '現場原話實錄', '逐字記錄').
        2. Bans identical repeated H2 templates inside the same .full.md.
        3. Non-archive .full.md > 2,500 chars must have >= 2 H2 headings.
        4. Long .full.md (> 10,000 chars) must have average H2 span <= 8,000 chars.
        """
        violations = []
        for f in self.full_files:
            rel_path = str(f.relative_to(REPO_ROOT))
            if self._is_phase_a_pending(rel_path):
                continue
            text = f.read_text(encoding="utf-8")
            body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
            n_chars = len(body.strip())
            h2s = re.findall(r"^##\s+(.+)$", body, re.M)

            # 1. Ban placeholder H2s
            bad_h2s = [h for h in h2s if re.search(r"章節段落\s*\d*|現場原話實錄|逐字記錄", h)]
            if bad_h2s:
                violations.append(f"{rel_path}: contains placeholder H2 headings: {bad_h2s[:3]}")

            # 2. Ban identical repeated H2s
            if len(h2s) >= 2 and len(set(h2s)) < len(h2s):
                violations.append(f"{rel_path}: contains duplicate H2 headings: {h2s[:4]}")

            if "Archive" not in rel_path:
                # 3. Minimum 2 H2s for > 2,500 chars
                if n_chars > 2500 and len(h2s) < 2:
                    violations.append(
                        f"{rel_path}: body has {n_chars} chars but only {len(h2s)} H2 heading(s) (minimum 2 required)"
                    )
                # 4. Maximum average H2 span <= 8,000 chars for > 10,000 chars
                if n_chars > 10000 and len(h2s) >= 1 and (n_chars / len(h2s)) > 8000:
                    violations.append(
                        f"{rel_path}: sparse H2 segmentation ({len(h2s)} H2s across {n_chars} chars, avg {int(n_chars/len(h2s))} > 8000)"
                    )

        self.assertEqual(
            violations,
            [],
            f"Found .full.md chapter segmentation violations ({len(violations)}):\n" + "\n".join(violations[:30]),
        )

    def test_h1_cleanliness_and_summary_universal_header(self):
        """
        Section 7.1: Universal Header Protocol & H1 Cleanliness.
        1. Neither .full.md nor .md H1 titles may contain internal codes (e.g. MATH-02, SECPLUS-03, Lesson 01, # 📱 91 ).
        2. .md summaries must NOT start with YAML frontmatter (---).
        3. .md summaries must include '>' blockquote metadata and an exact relative link to ./{same_stem}.full.md.
        """
        violations = []
        internal_code_re = re.compile(r"[A-Z]{2,}-[A-Za-z0-9-]+|Lesson\s*\d+|#\s+\S+\s+\d{2,3}\s+")

        for f in self.full_files:
            rel_path = str(f.relative_to(REPO_ROOT))
            if self._is_phase_a_pending(rel_path):
                continue
            text = f.read_text(encoding="utf-8")
            body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
            h1_m = re.search(r"^#\s+(.+)$", body, re.M)
            if h1_m and internal_code_re.search(h1_m.group(0)):
                violations.append(f"{rel_path}: H1 contains banned internal code/number: '{h1_m.group(0)}'")

        for s in self.summary_files:
            rel_path = str(s.relative_to(REPO_ROOT))
            if self._is_phase_b_pending(rel_path):
                continue
            text = s.read_text(encoding="utf-8")

            if text.startswith("---"):
                violations.append(f"{rel_path}: summary (.md) must not contain YAML frontmatter")

            h1_m = re.search(r"^#\s+(.+)$", text, re.M)
            if not h1_m:
                violations.append(f"{rel_path}: missing H1 title")
            elif internal_code_re.search(h1_m.group(0)):
                violations.append(f"{rel_path}: H1 contains banned internal code/number: '{h1_m.group(0)}'")

            if not re.search(r"^>\s*\*\*", text, re.M):
                violations.append(f"{rel_path}: missing '>' blockquote metadata header")

            expected_full = s.name[:-3] + ".full.md"
            if f"(./{expected_full})" not in text:
                violations.append(f"{rel_path}: missing exact relative link '(./{expected_full})'")

        self.assertEqual(
            violations,
            [],
            f"Found H1 / Universal Header / Link violations ({len(violations)}):\n" + "\n".join(violations[:30]),
        )

    def test_no_control_chars_corrupted_latex_or_invalid_mermaid(self):
        """
        Section 7.4: Bans ASCII control chars (\\x07, \\x08, \\x09, \\x0c), corrupted LaTeX (rac{, unescaped floor),
        and invalid Mermaid syntax ('Note over' inside flowchart/graph).
        """
        violations = []
        for f in self.full_files:
            rel_path = str(f.relative_to(REPO_ROOT))
            if self._is_phase_a_pending(rel_path):
                continue
            text = f.read_text(encoding="utf-8")
            bad_ctrls = [repr(c) for c in ("\x07", "\x08", "\x09", "\x0c") if c in text]
            if bad_ctrls:
                violations.append(f"{rel_path}: contains unescaped ASCII control character(s) {bad_ctrls}")

        for s in self.summary_files:
            rel_path = str(s.relative_to(REPO_ROOT))
            if self._is_phase_b_pending(rel_path):
                continue
            text = s.read_text(encoding="utf-8")

            bad_ctrls = [repr(c) for c in ("\x07", "\x08", "\x09", "\x0c") if c in text]
            if bad_ctrls:
                violations.append(f"{rel_path}: contains unescaped ASCII control character(s) {bad_ctrls}")

            if re.search(r"(?<!\\f)rac\{|(?<!\\[lr])floor\b", text):
                violations.append(f"{rel_path}: contains corrupted LaTeX ('rac{{' or 'floor' missing backslash)")

            for m in re.finditer(r"```mermaid\s+(.*?)```", text, re.S):
                mbody = m.group(1).strip()
                if re.match(r"^(flowchart|graph)\b", mbody) and "Note over" in mbody:
                    violations.append(f"{rel_path}: Mermaid flowchart/graph illegally uses sequenceDiagram 'Note over'")

        self.assertEqual(
            violations,
            [],
            f"Found control char / LaTeX / Mermaid syntax violations ({len(violations)}):\n" + "\n".join(violations[:30]),
        )

    def test_summary_structure_and_depth_gate(self):
        """
        Rule 15 & Section 7.3/7.4: Zero Generic Boilerplate and Substantive Genre Depth in Summaries (.md).
        1. Forbids generic boilerplate phrases ('深入檢視問題根源', '針對演算法提出系統性評估', etc.).
        2. Non-archive summaries must have:
           - >= 3 H2 sections ('## ')
           - >= 1,500 chars (>= 1,200 chars if matching .full.md body < 5,000 chars)
           - At least 1 Mermaid diagram ('```mermaid')
        """
        generic_boilerplate = [
            "深入檢視問題根源",
            "針對演算法提出系統性評估",
            "提出具體可行之解決架構",
        ]
        violations = []
        for s in self.summary_files:
            rel_path = str(s.relative_to(REPO_ROOT))
            text = s.read_text(encoding="utf-8")

            # 1. Generic boilerplate check (always enforced)
            for phrase in generic_boilerplate:
                if phrase in text:
                    violations.append(f"{rel_path}: contains generic boilerplate '{phrase}'")

            # 2. Structural depth check (excluding archive chatter)
            if "Archive" not in rel_path:
                if self._is_phase_b_pending(rel_path):
                    if len(text.strip()) < 150:
                        violations.append(f"{rel_path}: summary too short (<150 chars)")
                    continue

                h2s = re.findall(r"^##\s+(.+)$", text, re.M)
                if len(h2s) < 3:
                    violations.append(f"{rel_path}: has only {len(h2s)} H2 section(s) (minimum 3 required)")

                full_path = s.parent / (s.name[:-3] + ".full.md")
                full_len = len(full_path.read_text(encoding="utf-8")) if full_path.exists() else 99999
                min_chars = 1200 if full_len < 5000 else 1500
                if len(text.strip()) < min_chars:
                    violations.append(
                        f"{rel_path}: summary too short ({len(text.strip())} chars < required {min_chars} chars)"
                    )

                if "```mermaid" not in text:
                    violations.append(f"{rel_path}: missing mandatory Mermaid diagram")

        self.assertEqual(
            violations,
            [],
            f"Found summary depth / structure violations ({len(violations)}):\n" + "\n".join(violations[:30]),
        )

if __name__ == "__main__":
    unittest.main()



