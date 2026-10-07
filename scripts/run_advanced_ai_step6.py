#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate and update catalogs for Session 6 (2026-04-09).
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_advanced_ai_optimization import build_session, raw_lines
from scripts.run_advanced_ai_step import add_catalog_entry


def build_step_session6():
    lines_subset = raw_lines[12199:13083]
    sections_cfg = [
        ("🎯 NLP 文本分類任務定義：從字詞符號化（Tokenization）到情感極性判斷", (0.0, 0.33)),
        ("📊 類別不平衡與分類閾值設定：正負向樣本動態定義與標註不確定性", (0.33, 0.66)),
        ("🔬 準確率（Accuracy）與混淆矩陣分析：模型效能評測與錯誤歸因", (0.66, 1.0)),
    ]
    summary_cfg = {
        "topic": "自然語言處理（NLP）、文本分類（Text Categorization）、情感二元分類與評估指標分析",
        "modules": "NLP Pipeline, Tokenization, Text Categorization, Binary Classification, Accuracy, F1-Score",
        "goal": "掌握文本數據從前處理、特徵表示到情感分類器訓練之全流程，學會分析分類閾值對預測準確率之影響",
        "exec_summary": "本週正式進入自然語言處理（NLP）核心模組。授課教師引導學員探討如何將非結構化文本轉換為特徵向量，並進行正向（Positive）與負向（Negative）情感極性分類。課程特別指出真實世界文本分類的挑戰：『很多時候正向與負向類別並沒有絕對靜態的邊界定義』。教師引導學員透過準確率（Accuracy，預測正確樣本數/總樣本數）與混淆矩陣（Confusion Matrix）剖析分類邊界，並示範如何調整決策門檻值以因應類別不平衡問題。",
        "mermaid_title": "NLP 文本情感分類處理與評估管線",
        "mermaid": """flowchart TD
    Text["原始非結構化文本 (Raw Text Data)"] --> Clean["文本清洗: 停用詞過濾、小寫化與標點去除"]
    Clean --> Token["符號化與特徵提取 (Tokenization & TF-IDF / Embeddings)"]
    Token --> Train["訓練分類器 (Logistic Regression / Naive Bayes / Transformer)"]
    Train --> Predict["機率輸出 P(y=Positive|x)"]
    
    Predict --> Threshold{"決策門檻值判定 (Threshold Tuning)"}
    Threshold --> Result["離散分類預測: Positive / Negative"]
    Result --> Eval["效能衡量: Accuracy / Precision / Recall / F1-Score"]""",
        "takeaways": [
            ("避免單純依賴單一 Accuracy 指標", "在文本情感分類中，樣本常存在正負比例失衡。若負向樣本佔 90%，盲目猜測全為負向即可獲得 90% 準確率。必須搭配 Precision、Recall 與 F1-Score 全面檢視。"),
            ("動態分類邊界與業務語境適配", "正面與負面的定義高度依賴業務情境（例如反諷、中性陳述）。模型設計應著重特徵詞上下文關聯，而非僅依賴孤立關鍵詞匹配。")
        ]
    }
    build_session(
        date_str="2026-04-09",
        talk_id="AI-OPT-06-NLP-SENTIMENT-CLASSIFICATION",
        title="進階人工智慧與最佳化 Lesson 06：自然語言處理（NLP）文本情感分類基準與評估指標設計",
        file_prefix="20260409-自然語言處理與情感分類基準",
        lines_subset=lines_subset,
        sections_cfg=sections_cfg,
        summary_cfg=summary_cfg
    )
    add_catalog_entry(
        session_no=184,
        topic="進階人工智慧與最佳化 Lesson 06：自然語言處理（NLP）文本情感分類基準與評估指標設計",
        speakers="授課講師, 學員",
        scenario="classroom-lecture",
        note_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260409-自然語言處理與情感分類基準.md",
        full_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260409-自然語言處理與情感分類基準.full.md"
    )


if __name__ == "__main__":
    build_step_session6()
