# 🎙️ Technical Conferences, Security, Academic & University Transcripts Repository

This repository maintains high-fidelity, verified speech-to-text transcripts, domain-corrected texts, and structured executive summaries across undergraduate & graduate courses, certifications, cybersecurity conferences (**HITCON**, **OSINT & CTI**), enterprise developer summits (**Microsoft DevDays Asia**), **Master's Thesis Defenses**, and **Academic Conferences**.

The repository houses **172 indexed sessions** comprising **344 production-grade deliverables**, strictly structured under the **Option 3-A Primary/Companion Architecture**:

1. **📑 `{YYYYMMDD}-{Topic}.md` (Core Notes & Executive Summary)**: Primary document for rapid review. High-density structured breakdown including core methodologies, exploit/system architectures, **Mermaid sequence & flow diagrams**, ablation analyses, and key takeaways.
2. **📄 `{YYYYMMDD}-{Topic}.full.md` (100% Verbatim Full Transcript)**: Companion document for complete reference. Sentence-by-sentence proofread transcript retaining all spoken words, colloquial nuances, live classroom/defense interactions, and Q&A.

---

## 📖 Master Catalog of Transcripts

This repository adheres to a **decoupled architecture with automated catalog indexing**. The README focuses on project rules, standards, and toolchain mechanics. The comprehensive, up-to-date catalog of all 172 indexed sessions is maintained in dedicated catalog files:

* 🌐 **[English Master Catalog (CATALOG.md)](./CATALOG.md)**: Full session table of contents with topics, speakers, scenario profiles, and direct file links.
* 🇹🇼 **[中文全局目錄索引 (CATALOG.zh-TW.md)](./CATALOG.zh-TW.md)**: Traditional Chinese comprehensive index.

---

## 🗂️ Core Knowledge Domains

| Directory | Structure & Scope | Core Technical Topics |
| :--- | :--- | :--- |
| **`4-University/`** | **Undergraduate Programs**<br/>・`1-Studies/` (Year 1: Freshman)<br/>・`2-Curriculum/` (Year 2: Sophomore)<br/>・`3-Specialization/` (Year 3: Junior)<br/>・`4-Capstone/` (Year 4: Senior)<br/>・`5-Extracurricular/` (Ecology Field Surveys)<br/>・`Archive/` (Administrative & Routine Archive)<br/>Subdivided by `Fall-Semester`, `Spring-Semester`, and `Holiday` | Basic Math, General Physics, Biology Lab, Career Development, Computer Networks, MIS, Cloud Computing, IoT Security, Project Management, Cisco CCNA 1, CompTIA Security+, Coastal Land Crab Ecology Surveys.<br/>*Archive*: Campus door/window checks, sports day voting, club financial reviews, and peer evaluation consultations. |
| **`5-Master/`** | **Graduate & Research Programs**<br/>・`1-First-Year/` (M1: Courses & Activities)<br/>・`2-Second-Year/` (M2: Courses & Activities)<br/>・`Laboratory/` (Dedicated: Degree-Defense, Project-Meeting, Security-News, Seminar, Thesis-Progress)<br/>・`Archive/` (Informal & Daily Life Archive) | Software Engineering, DevOps, Computer Network Lab, Machine Learning, HCI/UX, CTF Security, Advanced AI Optimization, Research Methodology, English AI Presentation, NCU IM Academic Conference, HITCON 2026, DevDays Asia 2026, OSINT & CTI, Deloitte GenAI Keynote, UIC Explainable AI, DRAVILaMA Thesis Defense, APR Bug Repair, Project Meeting, Security News (PostgreSQL Vulnerability), Android Malware GNN.<br/>*Archive*: Pre-meeting travel planning and laboratory daily life chatter. |
| **`audio/`** | **Audio Lifecycle Management**<br/>・`pending/` (Incoming audio staging)<br/>・`processed/` (Completed transcripts ready for cleanup)<br/>・`preserved/` (Non-speech acoustic isolation) | 38 preserved non-speech audio recordings (37 guitar/instrumental performance recordings + 1 silence track), verified via spectral flatness and chroma variance, safely documented in `audio/preserved/MANIFEST.md`. |

> 💡 **Navigation Tip**: To explore any specific transcript or summary, browse [CATALOG.md](./CATALOG.md) or navigate the directory paths above.

---

## 📐 5 Scenario Adapters Matrix (`PROOFREAD_RULES.md`)

To avoid "one-size-fits-all" formatting issues across diverse audio sources, all transcripts follow the **Universal Core Protocol + 5 Scenario Adapters**:

| Scenario ID | Use Case | Structure & Formatting Rules |
| :--- | :--- | :--- |
| **`classroom-lecture`** | University & Graduate Courses | Explicit speaker attribution for instructors (`**【授課講師】**：`) and students (`**【學員】**：`), capturing whiteboard derivations and classroom Q&A. |
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
├── audio_manager.py    # Audio lifecycle manager: pending / processed staging, disk cleanup, preserved isolation
├── splitter.py         # Long audio segmenter and chunk tracker
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

# 8. Run 4-stage automated self-verification gate
python scripts/self_check.py
```

---

## 🧪 Quality Assurance & Unit Test Suite (`tests/`)

The repository maintains rigorous quality assurance across regression, structure conformity, and audio lifecycle safety:

```bash
# Run comprehensive self-check gate
python scripts/self_check.py

# Run complete unit test suite
python -m unittest discover tests
```

* **Test Suites & Coverage**:
  * Text cleaning and punctuation normalization (`test_processor.py`)
  * Domain dictionary entity extraction and gatekeeping (`test_entity_guard.py`)
  * Safe GPU VRAM allocation ceiling (`test_asr.py`)
  * Verbatim scenario structure compliance (`test_scenarios.py`)
  * Automated bilingual catalog generator and link validator (`test_indexer.py`)
  * Audio lifecycle and deletion safety (`test_audio_manager.py`)
  * Repository-wide verbatim proofread linter (`test_proofread_linter.py`)
  * Long audio splitting and chunk recombination (`test_splitter.py`)
* **Current Status**: **44/44 unit tests passing** (`OK`), 100% deliverable pairing fidelity.
