# Agent Persistent Memory

> **Every agent session MUST read this file first** (defined in .agent/rules.md).
> **Every agent session MUST update this file before ending.**

---

## 🔑 User Preferences
- **Language**: 繁體中文 preferred for casual conversation; code/commits in English.
- **Style**: Direct, no fluff. Get things done with high engineering rigor.

---

## 📋 Current Active Tasks
- HITCON 資安演講逐字稿校對與 Executive Summaries 產出。

---

## 🏗️ Architectural Context
- **Project**: record-list (HITCON Security Talks & Transcripts)
- **Rules Reference**: `PROOFREAD_RULES.md`
- **Pipeline**:
  - `scripts/aac_to_mp3.py` (音檔轉檔)
  - `scripts/format_transcript.py` (語音辨識校對與自然段落切分)
- **Structure**: `{Category}/{YYYYMMDD}-{EventName}/{ID}-{ShortTitle}-{proofread|summary}.md`

---

## ✅ Completed Decisions & Lessons Learned
- Initialized with `research` scaffolding preset.
- Linked `PROOFREAD_RULES.md` into Agent Rules.