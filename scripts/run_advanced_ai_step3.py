#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate and update catalogs for Session 3 (2026-03-12).
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_advanced_ai_optimization import build_session, raw_lines
from scripts.run_advanced_ai_step import add_catalog_entry


def build_step_session3():
    lines_subset = raw_lines[4711:7115]
    sections_cfg = [
        ("🎯 GitHub 與 Kaggle 認證整合：環境建立、版本控制與團隊名單綁定", (0.0, 0.33)),
        ("📊 資料科學特徵管線實務：缺失值補全、特徵編碼與本地交叉驗證機制", (0.33, 0.66)),
        ("🔬 基準模型建立與提交演練：避免資料外洩與 Leaderboard 榜單解讀", (0.66, 1.0)),
    ]
    summary_cfg = {
        "topic": "GitHub 團隊版本庫串接、Kaggle 實名帳號登錄、特徵工程管線與提交驗證",
        "modules": "GitHub Workflow, Kaggle Submission, Pipeline Serialization, Data Leakage Prevention",
        "goal": "掌握跨人協作的 Git/GitHub 分支管理規範，並完成 Kaggle 競賽線上實名登錄與端到端推論測試",
        "exec_summary": "本週課程聚焦於現代軟體工程與資料科學研發之基礎設施整合。授課教師逐一核實各小組之 Kaggle 使用者名稱與 GitHub 帳號，指導各團隊建立標準專案結構（包含 data/、src/、notebooks/）與分支協作規範。課堂實戰演示了如何利用 Scikit-Learn Pipeline 封裝預處理與模型訓練流程，確保特徵變換邏輯能嚴格隔離於訓練集內，防止測試資料外洩（Data Leakage），並完成首波基準預測檔生成與線上提交測試。",
        "mermaid_title": "GitHub 與 Kaggle 整合之特徵工程推論管線",
        "mermaid": """flowchart TD
    subgraph Repo["GitHub 團隊專案協作管理"]
        Main["main 穩定主分支"]
        Feature["feature/fe 分支: 特徵工程研發"]
        ModelBranch["feature/model 分支: 演算法評測"]
        Feature --> PR["Pull Request 程式碼審查與合併"]
        ModelBranch --> PR
        PR --> Main
    end

    subgraph Pipeline["端到端 Scikit-Learn Pipeline 封裝"]
        Fit["fit() 階段: 僅在 Train CV 折次計算統計量"]
        Transform["transform() 階段: 無偏應用於 Test 集"]
        NoLeak["絕不全域呼叫 fit_transform (零資料外洩)"]
        Fit --> Transform --> NoLeak
    end

    Main --> Pipeline
    Pipeline --> Submit["產出 submission.csv ➔ Kaggle API 自動提交驗證"]""",
        "takeaways": [
            ("管線序列化與防外洩（Leakage-Proof Pipeline）", "所有標準化、編碼與缺失值填補器必須以 Pipeline 形式封裝，所有統計參數（如平均數、標準差）僅能由訓練折次計算，嚴禁在分割前對全量數據進行全局操作。"),
            ("Git 規範化協作防止程式碼覆蓋", "小組成員應遵循功能分支（Feature Branch）開發規範，每次提交附帶清楚的實驗描述與指標日誌，避免 Notebook 衝突造成代碼遺失。")
        ]
    }
    build_session(
        date_str="2026-03-12",
        talk_id="AI-OPT-03-GITHUB-KAGGLE-PIPELINE",
        title="進階人工智慧與最佳化 Lesson 03：GitHub 專案協作、Kaggle 認證與端到端特徵管線實作",
        file_prefix="20260312-GitHub與Kaggle資料科學管線",
        lines_subset=lines_subset,
        sections_cfg=sections_cfg,
        summary_cfg=summary_cfg
    )
    add_catalog_entry(
        session_no=181,
        topic="進階人工智慧與最佳化 Lesson 03：GitHub 專案協作、Kaggle 認證與端到端特徵管線實作",
        speakers="授課講師, 學員",
        scenario="classroom-lecture",
        note_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260312-GitHub與Kaggle資料科學管線.md",
        full_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260312-GitHub與Kaggle資料科學管線.full.md"
    )


if __name__ == "__main__":
    build_step_session3()
