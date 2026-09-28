# 🎙️ Technical Conferences, Security & Academic Transcripts Repository

This repository maintains high-fidelity, verified speech-to-text transcripts, domain-corrected texts, and structured executive summaries across cybersecurity conferences (**HITCON**, **OSINT & CTI**), enterprise developer summits (**Microsoft DevDays Asia**), **Master's Thesis Defenses**, and **Academic Conferences**.

Each conference topic or session provides two complementary, production-grade deliverables:

1. **📄 `proofread.md` (100% Verbatim Full Transcript)**: Sentence-by-sentence proofread transcript retaining all spoken words, colloquial nuances, live interactions, and Q&A. Domain jargon is strictly validated against custom dictionaries, and text is organized into clean, reader-friendly paragraphs with standardized YAML frontmatter.
2. **📑 `summary.md` (Executive Summary & Technical Digest)**: High-density structured breakdown including core methodologies, exploit/system architectures, **Mermaid sequence & flow diagrams**, ablation analyses, defense/implementation takeaways, and committee evaluations.

---

## 📖 Master Catalog of Transcripts

This repository adheres to a **decoupled architecture with automated catalog indexing**. The README focuses on project rules, standards, and toolchain mechanics. The comprehensive, up-to-date catalog of all indexed sessions is maintained in dedicated catalog files:

* 🌐 **[English Master Catalog (CATALOG.md)](./CATALOG.md)**: Full session table of contents with topics, speakers, scenario profiles, and direct file links.
* 🇹🇼 **[中文全局目錄索引 (CATALOG.zh-TW.md)](./CATALOG.zh-TW.md)**: Traditional Chinese comprehensive index.

---

## 🗂️ Core Knowledge Domains

| Directory | Scope & Events | Core Technical Topics |
| :--- | :--- | :--- |
| **`1-Security/`** | **HITCON 2026**<br/>**OSINT & CTI Sharing Session** | Android kernel & Mali GPU driver LPE, smart POS firmware dumping & 0-Day, red-team supply chain attacks, OSINT identity pivot chains, QR phishing infrastructure & MyCERT coordination. |
| **`2-Cloud-AI/`** | **Microsoft DevDays Asia 2026** | Azure OpenAI enterprise multi-agent systems, GitHub Copilot Workspace, Tokenomics cost optimization, cloud-native resiliency, Fabric unified data governance, Responsible AI (UL 315). |
| **`5-Master/`** | **Master's Thesis Defense (DRAVILaMA)**<br/>**Academic Conferences (Session G, H, I)** | Multimodal driving risk prediction, LLaVA visual instruction tuning, temporal causal attention mechanisms, aMCI discourse structure analysis, short-video recommendation, deepfake audio XAI. |

> 💡 **Navigation Tip**: To explore any specific transcript or summary, browse [CATALOG.md](./CATALOG.md) or navigate the directory paths above.

---

## 📐 4 Scenario Adapters Matrix (`PROOFREAD_RULES.md`)

To avoid "one-size-fits-all" formatting issues across diverse audio sources, all transcripts follow the **Universal Core Protocol + 4 Scenario Adapters**:

| Scenario ID | Use Case | Structure & Formatting Rules |
| :--- | :--- | :--- |
| **`single-talk`** | Standard Keynote / Tech Talk | Narrative technical flow. **NO speaker tags** in body paragraphs; explicit speaker tags enabled **only** during audience Q&A sessions. |
| **`multi-paper`** | Academic Conference Sessions | Dual-level tree structure: `## 論文 X: [題目]` followed by `## 🔬 論文 X 評審講評與 Q&A`. Full speaker attribution throughout; captures opening announcements and closing award ceremonies. |
| **`thesis-defense`** | Master's / Ph.D. Oral Defense | Technical presentation followed by dense, structured defense dialogue with strict committee role markers (`召集人`, `口試委員`, `指導教授`, `研究生`). |
| **`lightning-talks`** | Multi-Speaker Short Talks | Catalog of rapid-fire presentations with individual topic banners and speaker attribution. |

---

## 🛠️ Processing Pipeline & Architecture (`transcript_processor/`)

The repository features an in-house, production-grade transcript engineering toolkit designed for safe GPU execution, verbatim formatting, automated catalog generation, and strict validation:

```text
transcript_processor/
├── cleaner.py          # CJK space normalization, fullwidth/halfwidth punctuation standardization
├── corrector.py        # Domain-specific phonetic & OCR typo correction (Security/Cloud/Academic)
├── entity_guard.py     # Entity Gate: detects speakers, roles, titles and enforces human confirmation
├── asr.py              # Safe GPU memory allocation (0.60 ceiling), VRAM guard against Windows DWM TDR resets
├── structurer.py       # Verbatim transcript generator & ScenarioType validator (validate_transcript_structure)
├── summarizer.py       # High-density technical summary & Mermaid diagram generator
├── indexer.py          # Automated repository scanner: regenerates CATALOG.md and CATALOG.zh-TW.md
├── audio_manager.py    # Audio lifecycle manager: pending / processed staging and disk cleanup
├── pipeline.py         # End-to-end processing pipeline orchestrator
└── cli.py              # Command-line interface
```

### 💻 Common CLI Commands

```bash
# 1. Automatically scan repository and regenerate both CATALOG.md and CATALOG.zh-TW.md
python -m transcript_processor index

# 2. Inspect audio workspace status (audio/pending and audio/processed counts & disk usage)
python -m transcript_processor audio status

# 3. Move delivered audio file to processed (safe to delete)
python -m transcript_processor audio finish "錄音檔名.aac"

# 4. Safely clean up processed audio files to free disk space
python -m transcript_processor audio clean --yes

# 5. Clean raw transcript and normalize CJK spacing
python -m transcript_processor clean raw_transcript.txt -o cleaned.txt

# 6. Apply domain vocabulary corrections
python -m transcript_processor correct cleaned.txt -d common hitcon academic -o corrected.txt

# 7. Generate entity verification report for proper nouns and names
python -m transcript_processor entity-check corrected.txt -o entity_report.md

# 8. Display GPU VRAM safety limits
python -m transcript_processor vram-info
```

---

## 🧪 Unit Test Suite (`tests/`)

Run the test suite with:
```bash
python -m pytest tests/
```
* **Coverage**: Complete verification across text cleaners, punctuation normalizers, domain correction engines, entity guard candidate extraction, safe VRAM allocation scheduling, 4 scenario structure validators, the automated catalog indexer, and the audio lifecycle manager.
* **Status**: 33 unit tests passing (`33 passed in 0.44s`).
