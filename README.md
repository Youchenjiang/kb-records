# 🎙️ Technical Conferences & Academic Transcripts: Verbatim Records & Executive Summaries

This repository maintains high-fidelity transcripts, domain-corrected texts, and structured executive summaries covering top cybersecurity conferences (**HITCON**), enterprise developer summits (**Microsoft DevDays Asia**), **Master's Thesis Defenses**, and **Academic Conferences**.

Each conference topic or session is structured into a dedicated directory providing two complementary, production-grade deliverables:

1. **`proofread.md` (100% Verbatim Full Transcript)**: Sentence-by-sentence proofread transcript retaining all spoken words, colloquial expressions, live interactions, and Q&A. Domain jargon is strictly validated against custom dictionaries, and text is organized into clean, reader-friendly paragraphs with standardized YAML frontmatter.
2. **`summary.md` (Executive Summary & Technical Digest)**: High-density structured breakdown including core methodologies, exploit/system architectures, **Mermaid sequence & flow diagrams**, ablation analyses, defense/implementation takeaways, and committee evaluations.

---

## 📐 Scenario Adapters Matrix (`PROOFREAD_RULES.md`)

To avoid "one-size-fits-all" formatting issues across diverse audio sources, transcripts follow the **Universal Core Protocol + 4 Scenario Adapters**:

| Scenario ID | Use Case | Structure & Formatting Rules |
| :--- | :--- | :--- |
| **`single-talk`** | Standard Keynote / Tech Talk | Narrative technical flow. **NO speaker tags** in body paragraphs; explicit speaker tags enabled **only** during audience Q&A sessions. |
| **`multi-paper`** | Academic Conference Sessions | Dual-level tree structure: `## 論文 X: [題目]` followed by `## 🔬 論文 X 評審講評與 Q&A`. Full speaker attribution throughout; captures opening announcements and closing award ceremonies. |
| **`thesis-defense`** | Master's / Ph.D. Oral Defense | Technical presentation followed by dense, structured defense dialogue with strict committee role markers (`召集人`, `口試委員`, `指導教授`, `研究生`). |
| **`lightning-talks`** | Multi-Speaker Short Talks | Catalog of rapid-fire presentations with individual topic banners and speaker attribution. |

---

## 🗂️ Repository Directory

### 🛡️ 1-Security: HITCON 2026

* **[91 - Pixel 8A ARM Mali GPU Driver Exploit](./1-Security/20260821-HITCON-2026/91-Pixel8A-GPU漏洞挖掘/summary.md)**
  * Speaker: Nan Wang
  * Topics: Android kernel & Mali GPU driver LPE, UAF vulnerability, physical page spraying, zero-out technique.
  * Links: [📄 Verbatim Transcript](./1-Security/20260821-HITCON-2026/91-Pixel8A-GPU漏洞挖掘/proofread.md) | [📑 Technical Summary](./1-Security/20260821-HITCON-2026/91-Pixel8A-GPU漏洞挖掘/summary.md)
* **[92 - POS Terminal Reverse Engineering & AI 0-Day Discovery](./1-Security/20260821-HITCON-2026/92-POS-ADB-0Day-AI輔助/summary.md)**
  * Speaker: Vickie
  * Topics: Smart POS firmware dumping, hidden ADB service exploitation, AI-assisted taint analysis, hardware attack surfaces.
  * Links: [📄 Verbatim Transcript](./1-Security/20260821-HITCON-2026/92-POS-ADB-0Day-AI輔助/proofread.md) | [📑 Technical Summary](./1-Security/20260821-HITCON-2026/92-POS-ADB-0Day-AI輔助/summary.md)
* **[93 - Supply Chain Attacks: Targeting Red Teams & Researchers](./1-Security/20260821-HITCON-2026/93-供應鏈攻擊-黑吃黑/summary.md)**
  * Speaker: splitline
  * Topics: Open-source offensive tool backdooring, GitHub malicious PRs, VS Code workspace trust bypass, OPSEC defense.
  * Links: [📄 Verbatim Transcript](./1-Security/20260821-HITCON-2026/93-供應鏈攻擊-黑吃黑/proofread.md) | [📑 Technical Summary](./1-Security/20260821-HITCON-2026/93-供應鏈攻擊-黑吃黑/summary.md)
* **[94 - HITCON 2026 Lightning Talks (6 Talks Collection)](./1-Security/20260821-HITCON-2026/94-閃電秀6場合輯/summary.md)**
  * Topics: Community lightning talks including firmware security, web exploits, AI hacking, bug bounty experiences, and CTF recaps.
  * Links: [📄 Verbatim Transcript](./1-Security/20260821-HITCON-2026/94-閃電秀6場合輯/proofread.md) | [📑 Technical Summary](./1-Security/20260821-HITCON-2026/94-閃電秀6場合輯/summary.md)
* **[Introduction to OSINT & Cyber Threat Intelligence (CTI) Sharing Session](./1-Security/20260927-Intro-to-OSINT-CTI/summary.md)**
  * Speakers: Tunku Irfan (OSINT Researcher) & foxy (Cyber Threat Intelligence Researcher)
  * Topics: Passive reconnaissance pivot chain (Truecaller -> DuitNow -> SSM), Google Dorking, Sherlock username enumeration, permanent social media UIDs, QR phishing active infrastructure breakdown, evidence screenshot preservation, defamation legal risks, MyCERT vulnerability reporting, and in-meeting live chat log.
  * Links: [📄 Bilingual Verbatim Transcript (proofread.md)](./1-Security/20260927-Intro-to-OSINT-CTI/proofread.md) | [📑 Technical Summary (summary.md)](./1-Security/20260927-Intro-to-OSINT-CTI/summary.md)

---

### ☁️ 2-Cloud-AI: Microsoft DevDays Asia 2026

* **[121 - Azure OpenAI Enterprise Agentic Architecture](./2-Cloud-AI/20260922-DevDaysAsia-2026/121-Azure-OpenAI企業級應用實踐/summary.md)**
  * Topics: Multi-agent orchestration, enterprise RAG, token cost control, semantic caching, vector search optimization.
  * Links: [📄 Verbatim Transcript](./2-Cloud-AI/20260922-DevDaysAsia-2026/121-Azure-OpenAI企業級應用實踐/proofread.md) | [📑 Technical Summary](./2-Cloud-AI/20260922-DevDaysAsia-2026/121-Azure-OpenAI企業級應用實踐/summary.md)
* **[122 - GitHub Copilot Workspace & Agentic Development](./2-Cloud-AI/20260922-DevDaysAsia-2026/122-GitHub-Copilot工作區與Agent/summary.md)**
  * Topics: Task specification, automated workspace planning, repo-wide multi-file diff generation, pull request synthesis.
  * Links: [📄 Verbatim Transcript](./2-Cloud-AI/20260922-DevDaysAsia-2026/122-GitHub-Copilot工作區與Agent/proofread.md) | [📑 Technical Summary](./2-Cloud-AI/20260922-DevDaysAsia-2026/122-GitHub-Copilot工作區與Agent/summary.md)
* **[123 - Cloud-Native Microservices & Distributed Resiliency](./2-Cloud-AI/20260922-DevDaysAsia-2026/123-雲原生微服務與分散式架構/summary.md)**
  * Topics: Kubernetes ingress patterns, Dapr runtime, circuit breaking, event-driven messaging, zero-trust service mesh.
  * Links: [📄 Verbatim Transcript](./2-Cloud-AI/20260922-DevDaysAsia-2026/123-雲原生微服務與分散式架構/proofread.md) | [📑 Technical Summary](./2-Cloud-AI/20260922-DevDaysAsia-2026/123-雲原生微服務與分散式架構/summary.md)
* **[124 - Enterprise Data Platform & Fabric Unified Governance](./2-Cloud-AI/20260922-DevDaysAsia-2026/124-企業數據平臺與Fabric治理/summary.md)**
  * Topics: OneLake lakehouse architecture, Delta Parquet storage, cross-tenant data virtualization, Purview access governance.
  * Links: [📄 Verbatim Transcript](./2-Cloud-AI/20260922-DevDaysAsia-2026/124-企業數據平臺與Fabric治理/proofread.md) | [📑 Technical Summary](./2-Cloud-AI/20260922-DevDaysAsia-2026/124-企業數據平臺與Fabric治理/summary.md)
* **[125 - GenAI Security, Red Teaming & Guardrails](./2-Cloud-AI/20260922-DevDaysAsia-2026/125-生成式AI資安防護與紅隊演練/summary.md)**
  * Topics: Prompt injection mitigation, jailbreak testing, LLM content safety guardrails, automated red-teaming pipelines.
  * Links: [📄 Verbatim Transcript](./2-Cloud-AI/20260922-DevDaysAsia-2026/125-生成式AI資安防護與紅隊演練/proofread.md) | [📑 Technical Summary](./2-Cloud-AI/20260922-DevDaysAsia-2026/125-生成式AI資安防護與紅隊演練/summary.md)

---

### 🎓 5-Master: Master's Thesis Defense (DRAVILaMA)

* **[DRAVILaMA Master's Thesis Oral Defense Collection (2026/07/14)](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA論文簡報-summary.md)**
  * Candidate: 沈柏寧 (Advisor: 陳奕明博士)
  * Topics: Dashcam driving risk prediction via multimodal LLMs and visual instruction tuning, temporal behavior subgraph extraction, temporal causal attention mechanisms, cross-scenario confusion matrix defense.
  * Deliverables:
    * Presentation: [📄 Verbatim Transcript](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA論文簡報-proofread.md) | [📑 Technical Summary](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA論文簡報-summary.md)
    * Committee Defense Part 1: [📄 Verbatim Transcript](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA審查質詢-Part1-proofread.md) | [📑 Technical Summary](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA審查質詢-Part1-summary.md)
    * Committee Defense Part 2: [📄 Verbatim Transcript](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA審查質詢-Part2-proofread.md) | [📑 Technical Summary](./5-Master/20260714-MasterDefense-DRAVILaMA/DRAVILaMA審查質詢-Part2-summary.md)

---

### 🏛️ 5-Master: Academic Conferences (2026/03/27)

* **[Academic Conference Multi-Session Papers & Keynotes Collection](./5-Master/20260327-AcademicConference/SessionG-aMCI語篇研究-summary.md)**
  * **Session G (National Central University - Linguistics & Multimodal AI)**:
    * Paper 1: 戴文芳 — Integrating Linguistic Indicators and Semantic Embeddings for aMCI Discourse Proposition Structure & Topic Drift Analysis (Advisors: 曾小平教授, 蘇國良博士).
    * Paper 2: 林之璇 — Sequential Recommendation via Intent-Aware Multi-Interest Representation (Advisor: 何國瑞教授).
    * Paper 3: 陳玉偉 — Competency Modeling for Enterprise AI Talent Transformation.
    * Paper 4: 彭博勝 — Node Behavior-Guided Contrastive Learning for Cross-Domain Image Classification (NBGCL) (Advisor: 王建興教授).
    * Evaluation & Awards: Committee critiques and NCU paper award presentation ceremony.
    * Links: [📄 Verbatim Transcript](./5-Master/20260327-AcademicConference/SessionG-aMCI語篇研究-proofread.md) | [📑 Technical Summary](./5-Master/20260327-AcademicConference/SessionG-aMCI語篇研究-summary.md)
  * **Session H (Social Sentiment, Audio Deepfakes & Applied AI)**:
    * Paper 1: Anonymous Speaker — Public Generative AI Anxiety Mining & Measurement on Social Media (Pushshift / PRAW / LIWC / BERTopic).
    * Paper 2: 高一婷 — Multimodal Attention Fusion for Short Video Sequential Recommendation (ImageBind Feature Extraction).
    * Paper 3: Prof. Chih-Cheng Hsu Lab — Declarative Backtesting & Event-Driven Algorithmic Trading Framework (Financial Description Language, FDL).
    * Paper 4: 鍾國 — End-to-End Deepfake Audio Explainable AI with Spectral Representations (Deepfake Audio XAI).
    * Paper 5: 張子龍 — Dynamic Retrieval-Augmented Generation (RAG) Architecture for Enterprise Showcase & Advisory.
    * Evaluation & Closing: Committee evaluations, session closing, and group photos.
    * Links: [📄 Verbatim Transcript](./5-Master/20260327-AcademicConference/SessionG-AI焦慮與語音偽造-proofread.md) | [📑 Technical Summary](./5-Master/20260327-AcademicConference/SessionG-AI焦慮與語音偽造-summary.md)
  * **Session I (Invited Keynote & Graph Machine Learning)**:
    * Keynote: 沈柏寧 (Advisor: 陳奕明博士) — DRAVILaMA: Driving Risk Assessment via Multimodal Instruction Tuning.
    * Paper 1: 張玉瑤 — Smart Contract-Based Renewable Energy P2P Trading Matching Mechanism.
    * Paper 2: 林玉慧 — Sensitivity Analysis of Data Preprocessing & Data Quality on Machine Learning Classifiers.
    * Paper 3: Dr. Chih-Fong Tsai Student — Semi-Supervised Feature Selection & Multi-Label CNN for Hyperspectral Medical Imaging.
    * Paper 4: 許紫薇 — Sequential Temporal Attention Graph (Sequential TAG) for Financial Causality Prediction.
    * Evaluation & Honors: In-depth academic discussion led by Prof. Chang-Long Ouyang and appreciation plaque presentation.
    * Links: [📄 Verbatim Transcript](./5-Master/20260327-AcademicConference/SessionI-特邀專題與學生論文-proofread.md) | [📑 Technical Summary](./5-Master/20260327-AcademicConference/SessionI-特邀專題與學生論文-summary.md)

---

## 🛠️ Processing Pipeline & Architecture (`transcript_processor/`)

The repository features an in-house, production-grade transcript engineering toolkit designed for safe GPU execution, verbatim formatting, and strict validation:

```
transcript_processor/
├── cleaner.py          # CJK space normalization, fullwidth/halfwidth punctuation standardization
├── corrector.py        # Domain-specific phonetic & OCR typo correction (Security/Cloud/Academic)
├── entity_guard.py     # Entity Gate: detects speakers, roles, titles and enforces human confirmation
├── asr.py              # Safe GPU memory allocation (0.60 ceiling), VRAM guard against Windows DWM TDR resets
├── structurer.py       # Verbatim transcript generator & ScenarioType validator (single-talk, multi-paper, defense, etc.)
├── summarizer.py       # High-density technical summary & Mermaid diagram generator
├── pipeline.py         # End-to-end processing pipeline orchestrator
└── cli.py              # Command-line interface (`python -m transcript_processor [clean|correct|entity-check|vram-info|info]`)
```

### 🧪 Unit Test Suite (`tests/`)
Run the test suite with:
```bash
python -m pytest tests/
```
* **Coverage**: Complete verification across text cleaners, punctuation normalizers, domain correction engines, entity guard candidate extraction, safe VRAM allocation scheduling, and scenario structure validators.
* **Status**: 25 unit tests passing.
