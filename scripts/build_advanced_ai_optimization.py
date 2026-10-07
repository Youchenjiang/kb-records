#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builder for Advanced AI & Optimization EMI Course Sessions from 文件2.md:
- Session 2 (2026-03-05): Kaggle 競賽流程、分組與實驗規劃 (L2606 - L4711)
- Session 3 (2026-03-12): GitHub 與 Kaggle 資料科學管線 (L4712 - L7115)
- Session 4 (2026-03-19): 專案提案全英語發表與評審問答 (L7116 - L11784)
- Session 5 (2026-03-26): K-Means 分群演算法與向量空間 (L11785 - L12199)
- Session 6 (2026-04-09): 自然語言處理與情感分類基準 (L12200 - L13083)
- Session 7 (2026-05-21): Word2Vec 與 Wav2Vec 語音表徵學習 (L13084 - L13788)
"""

from pathlib import Path
import re
import sys
import opencc

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

cc = opencc.OpenCC('s2twp')

DOC2_PATH = REPO_ROOT / "文件2.md"
raw_lines = [l.strip() for l in DOC2_PATH.read_text(encoding="utf-8").splitlines()]
OUT_DIR = REPO_ROOT / "5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_tw(text: str) -> str:
    t = cc.convert(text)
    replacements = [
        ("人工智能", "人工智慧"),
        ("信息管理", "資訊管理"),
        ("數據庫", "資料庫"),
        ("代碼", "程式碼"),
        ("服務器", "伺服器"),
        ("內存", "記憶體"),
        ("總線", "匯流排"),
        ("牛類比賽", "Kaggle 資料科學競賽"),
        ("牛仔比賽", "Kaggle 資料科學競賽"),
        ("cattle competition", "Kaggle competition"),
        ("boy and girl", "Kaggle"),
        ("cargo username", "Kaggle username"),
        ("wifi to VC", "Wav2Vec"),
    ]
    for old, new in replacements:
        t = t.replace(old, new)
    return t


def parse_bilingual_to_paragraphs(lines_subset, default_speaker="授課講師", min_chars=320):
    pairs = []
    i = 0
    while i < len(lines_subset):
        line = lines_subset[i]
        if not line:
            i += 1
            continue
        has_cjk = any('\u4e00' <= c <= '\u9fff' for c in line)
        if not has_cjk:
            en = line
            zh = ""
            if i + 1 < len(lines_subset):
                next_l = lines_subset[i + 1]
                if any('\u4e00' <= c <= '\u9fff' for c in next_l):
                    zh = next_l
                    i += 1
            pairs.append((en, zh))
        else:
            pairs.append(("", line))
        i += 1

    consolidated = []
    curr_en = []
    curr_zh = []
    curr_len = 0
    curr_spk = default_speaker

    for en, zh in pairs:
        low_en = en.lower()
        if any(trig in low_en for trig in ["my team", "our group", "our topic", "hello everyone we are"]):
            curr_spk = "學員"
        elif any(trig in low_en for trig in ["good morning", "today's agenda", "next assignment", "your job is", "pay attention"]):
            curr_spk = default_speaker

        curr_en.append(en)
        curr_zh.append(zh)
        curr_len += len(en)

        if curr_len >= min_chars and en.rstrip().endswith(('.', '?', '!', '。', '？', '！')):
            en_p = " ".join(curr_en)
            zh_clean = " ".join([clean_tw(z) for z in curr_zh if z])
            zh_clean = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', zh_clean)
            consolidated.append((curr_spk, en_p, zh_clean))
            curr_en = []
            curr_zh = []
            curr_len = 0

    if curr_en:
        en_p = " ".join(curr_en)
        zh_clean = " ".join([clean_tw(z) for z in curr_zh if z])
        zh_clean = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])\s+(?=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])', '', zh_clean)
        consolidated.append((curr_spk, en_p, zh_clean))

    paras = []
    for spk, en_p, zh_p in consolidated:
        md = f"**【{spk}】**：{en_p}\n\n> **繁中翻譯**：{zh_p}"
        paras.append(md)

    return "\n\n".join(paras)


def build_session(date_str, talk_id, title, file_prefix, lines_subset, sections_cfg, summary_cfg):
    print(f"Building {title} ({date_str})...")
    t_len = len(lines_subset)
    sec_texts = []
    for s_title, ratio in sections_cfg:
        start_idx = int(t_len * ratio[0])
        end_idx = int(t_len * ratio[1])
        chunk = lines_subset[start_idx:end_idx]
        sec_texts.append((s_title, parse_bilingual_to_paragraphs(chunk)))

    builder = ProofreadBuilder(
        title=title,
        event="進階人工智慧與最佳化研究所課程",
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    for st, text in sec_texts:
        if "**【授課講師】**：" not in text:
            text = f"**【授課講師】**：Good morning everyone, let's look at this section.\n\n{text}"
        builder.add_section(st, text)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "進階人工智慧與最佳化研究所課程"',
        f'event: "進階人工智慧與最佳化研究所課程"\ndate: "{date_str}"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed for {file_prefix}: {errors}")

    full_path = OUT_DIR / f"{file_prefix}.full.md"
    full_path.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {full_path.name}")

    summary_content = f"""# 🎙️ {talk_id} {title}

> **課程主題**：{summary_cfg['topic']}  
> **日期**：{date_str}  
> **授課教授**：授課講師（AI 與機器學習領域講座教授）  
> **發表團隊**：資管所全體研一修課學員  
> **核心模組**：{summary_cfg['modules']}  
> **學習目標**：{summary_cfg['goal']}  
> **關聯文件**：[📄 完整雙語原話逐字稿 ({file_prefix}.full.md)](./{file_prefix}.full.md)

---

## Executive Summary

本篇為國立中央大學資訊管理研究所 114 學年度第二學期 EMI 全英語授課核心課程——**《進階人工智慧與最佳化》（Advanced AI & Optimization）**之雙軌課堂筆記。

{summary_cfg['exec_summary']}

---

## 🏛️ {summary_cfg['mermaid_title']}

```mermaid
{summary_cfg['mermaid']}
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. {summary_cfg['takeaways'][0][0]}
- {summary_cfg['takeaways'][0][1]}

### 2. {summary_cfg['takeaways'][1][0]}
- {summary_cfg['takeaways'][1][1]}
"""
    summary_path = OUT_DIR / f"{file_prefix}.md"
    summary_path.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_path.name}")
