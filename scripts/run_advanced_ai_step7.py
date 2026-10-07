#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate and update catalogs for Session 7 (2026-05-21).
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_advanced_ai_optimization import build_session, raw_lines
from scripts.run_advanced_ai_step import add_catalog_entry


def build_step_session7():
    lines_subset = raw_lines[13083:13788]
    sections_cfg = [
        ("🎯 自監督學習（SSL）概念：從文字 Word2Vec 詞向量到語音 Wav2Vec 2.0", (0.0, 0.33)),
        ("📊 多層特徵嵌入與隱藏向量抽取：聲學特徵編碼器與對比學習機制", (0.33, 0.66)),
        ("🔬 下游任務微調（Fine-Tuning）：語音辨識、分類遷移與期末評估準備", (0.66, 1.0)),
    ]
    summary_cfg = {
        "topic": "自監督學習（Self-Supervised Learning）、Word2Vec 詞嵌入、Wav2Vec 2.0 語音表徵學習與隱藏向量提取",
        "modules": "Self-Supervised Learning, Word2Vec, Wav2Vec 2.0, Latent Representations, Contrastive Loss, Downstream Fine-Tuning",
        "goal": "理解多模態深度表徵學習架構，掌握如何從大量未標註語音與文本中提取稠密特徵向量並微調下游任務",
        "exec_summary": "本週深入研討深度學習表徵學習（Representation Learning）最新進展。課程從經典文字嵌入 Word2Vec 的分散式表徵（Distributed Representation）切入，推進至語音領域當紅的自監督學習（SSL）模型——Wav2Vec 2.0。授課教師深入拆解模型內部結構：原始聲音訊號如何經過多層卷積特徵編碼器（Feature Encoder）轉換為高維隱藏特徵向量，並透過量化模組（Quantization）與對比學習損失函數（Contrastive Loss）進行無監督預訓練。課程最後引導學員如何抽取中繼層向量，並針對特定語音分類任務進行高效微調（Fine-Tuning）。",
        "mermaid_title": "Wav2Vec 2.0 語音表徵自監督學習與特徵提取架構",
        "mermaid": """flowchart TD
    Audio["原始音訊波形訊號 (Raw Audio Waveform)"] --> Encoder["多層卷積編碼器 (CNN Feature Encoder)"]
    Encoder --> Latent["潛在特徵向量 (Latent Representations Z)"]
    
    subgraph Pretraining["自監督預訓練 (SSL Pre-training)"]
        Mask["時間維度隨機遮罩 (Masking)"]
        Quant["Gumbel-Softmax 向量量化 (Quantization Q)"]
        Context["Transformer 上下文網絡 (Context Network C)"]
        Loss["對比學習損失 (Contrastive Loss: 辨識真實遮罩幀)"]
        Latent --> Mask --> Context --> Loss
        Latent --> Quant --> Loss
    end

    Context --> Freeze["凍結特徵提取層 / 抽取隱藏層向量"]
    Freeze --> Head["下游輕量分類頭 (Linear Classification Head)"]
    Head --> Output["語音辨識 / 意圖分類預測輸出"]""",
        "takeaways": [
            ("自監督學習大幅降低資料標註成本", "傳統語音辨識高度依賴逐字音訊對齊標註。Wav2Vec 2.0 透過自監督遮罩預訓練，只需極少量標註音訊即可微調出達到 SOTA 表現之語音分類模型。"),
            ("隱藏層向量的跨任務遷移價值", "預訓練模型的特徵提取層具備強大通用表徵力。實務上可直接提取 Context Network 之輸出向量作為固定特徵，快速串接下游分類器完成少樣本任務。")
        ]
    }
    build_session(
        date_str="2026-05-21",
        talk_id="AI-OPT-07-REPRESENTATION-LEARNING",
        title="進階人工智慧與最佳化 Lesson 07：Word2Vec 與 Wav2Vec 2.0 深度表徵學習與特徵提取架構",
        file_prefix="20260521-Word2Vec與Wav2Vec語音表徵學習",
        lines_subset=lines_subset,
        sections_cfg=sections_cfg,
        summary_cfg=summary_cfg
    )
    add_catalog_entry(
        session_no=185,
        topic="進階人工智慧與最佳化 Lesson 07：Word2Vec 與 Wav2Vec 2.0 深度表徵學習與特徵提取架構",
        speakers="授課講師, 學員",
        scenario="classroom-lecture",
        note_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260521-Word2Vec與Wav2Vec語音表徵學習.md",
        full_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260521-Word2Vec與Wav2Vec語音表徵學習.full.md"
    )


if __name__ == "__main__":
    build_step_session7()
