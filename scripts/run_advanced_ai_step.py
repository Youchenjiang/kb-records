#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate and update catalogs for individual sessions of Advanced AI.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_advanced_ai_optimization import build_session, raw_lines


def add_catalog_entry(session_no, topic, speakers, scenario, note_path, full_path, note_text_zh="筆記", full_text_zh="全文"):
    cat_en_path = REPO_ROOT / "CATALOG.md"
    cat_zh_path = REPO_ROOT / "CATALOG.zh-TW.md"
    en = cat_en_path.read_text(encoding="utf-8")
    zh = cat_zh_path.read_text(encoding="utf-8")

    row_en = f"| {session_no} | **{topic}** | {speakers} | `{scenario}` | [📑 Notes]({note_path}) · [📄 Full]({full_path}) |\n"
    row_zh = f"| {session_no} | **{topic}** | {speakers} | `{scenario}` | [📑 {note_text_zh}]({note_path}) · [📄 {full_text_zh}]({full_path}) |\n"

    # Append before final '---'
    en = en.rstrip()
    if en.endswith('---'):
        en = en[:-3].rstrip() + "\n" + row_en + "\n---\n"
    else:
        en = en + "\n" + row_en

    zh = zh.rstrip()
    if zh.endswith('---'):
        zh = zh[:-3].rstrip() + "\n" + row_zh + "\n---\n"
    else:
        zh = zh + "\n" + row_zh

    cat_en_path.write_text(en, encoding="utf-8")
    cat_zh_path.write_text(zh, encoding="utf-8")
    print(f"Registered session {session_no} in catalogs.")


def build_step_session2():
    lines_subset = raw_lines[2605:4711]
    sections_cfg = [
        ("🎯 競賽導引與團隊分組規範：Kaggle 實戰競賽定位與小組協作名單確認", (0.0, 0.33)),
        ("📊 機器學習開發管線剖析：資料預處理、特徵工程與交叉驗證切分", (0.33, 0.66)),
        ("🔬 實驗假說設定與模型迭代準則：從基準 Baseline 到進階集成模型探索", (0.66, 1.0)),
    ]
    summary_cfg = {
        "topic": "Kaggle 競賽機制、小組團隊建立（3~4人）、資料科學端到端開發管線與實驗設計",
        "modules": "Kaggle Pipeline, Cross-Validation, Feature Engineering, Baseline Modeling, Experiment Planning",
        "goal": "掌握資料科學競賽專案從團隊組建、題目拆解、資料探勘到建立可復現基準模型之完整工作流程",
        "exec_summary": "本週正式啟動本學期核心實務專案——Kaggle 資料科學機器學習競賽。授課教師要求全班學員於課堂 10 分鐘內透過線上協作表單完成 3~4 人分組與團隊命名。課程詳細拆解了現代資料科學與機器學習的端到端開發管線（Pipeline），強調不可盲目調參，而應建立嚴謹的交叉驗證策略（CV Strategy）防止資料外洩（Data Leakage），並指導學員如何規劃可追蹤的實驗紀錄與假設檢驗流程。",
        "mermaid_title": "Kaggle 資料科學端到端競賽開發管線",
        "mermaid": """flowchart TD
    Raw["競賽原始數據集 (Train & Test Datasets)"] --> EDA["探索性資料分析 (EDA: 分布與遺漏值)"]
    EDA --> Split["防洩漏驗證切分 (Stratified K-Fold CV)"]
    
    subgraph FeatureEngineering["特徵工程 (Feature Engineering)"]
        Feat1["數值特徵標準化與偏態校正"]
        Feat2["類別特徵編碼 (Target / One-Hot)"]
        Feat3["跨欄位組合與統計聚合特徵"]
    end
    
    Split --> FeatureEngineering
    FeatureEngineering --> Baseline["建立基準模型 (Baseline Model)"]
    Baseline --> Iterate["模型調優與集成 (Ensembling / Stacking)"]
    Iterate --> Submit["產生預測並提交排行榜 (Leaderboard Submission)"]""",
        "takeaways": [
            ("建立乾淨的驗證策略（Validation Strategy）", "任何競賽與實務專案的第一步都是建立與測試集分布一致的本地驗證集。若本地 CV 與線上 Leaderboard 分數脫鉤，後續所有特徵優化皆將徒勞無功。"),
            ("敏捷團隊分工與實驗版本控管", "各組成員應分別認領特徵挖掘、模型架構試驗與後處理工作，嚴格記錄每次提交之代碼版本與本地指標，確保模型具備高復現性。")
        ]
    }
    build_session(
        date_str="2026-03-05",
        talk_id="AI-OPT-02-KAGGLE-PIPELINE",
        title="進階人工智慧與最佳化 Lesson 02：Kaggle 競賽流程、團隊分組與機器學習實驗規劃",
        file_prefix="20260305-Kaggle競賽流程與團隊實驗規劃",
        lines_subset=lines_subset,
        sections_cfg=sections_cfg,
        summary_cfg=summary_cfg
    )
    add_catalog_entry(
        session_no=180,
        topic="進階人工智慧與最佳化 Lesson 02：Kaggle 競賽流程、團隊分組與機器學習實驗規劃",
        speakers="授課講師, 學員",
        scenario="classroom-lecture",
        note_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260305-Kaggle競賽流程與團隊實驗規劃.md",
        full_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260305-Kaggle競賽流程與團隊實驗規劃.full.md"
    )


if __name__ == "__main__":
    build_step_session2()
