#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate and update catalogs for Session 5 (2026-03-26).
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_advanced_ai_optimization import build_session, raw_lines
from scripts.run_advanced_ai_step import add_catalog_entry


def build_step_session5():
    lines_subset = raw_lines[11784:12199]
    sections_cfg = [
        ("🎯 非監督式學習與分群任務定義：無標籤資料探勘與質心初始設定", (0.0, 0.33)),
        ("📊 歐氏距離計算與向量空間分群：資料點指派與簇內平方和（WCSS）最小化", (0.33, 0.66)),
        ("🔬 質心更新與收斂停止條件：肘部法則（Elbow Method）與群聚評估指標", (0.66, 1.0)),
    ]
    summary_cfg = {
        "topic": "非監督式學習（Unsupervised Learning）、K-Means 演算法數學原理、向量空間歐氏距離與質心迭代",
        "modules": "K-Means, Centroid Initialization, Euclidean Distance, WCSS, Elbow Method, Silhouette Score",
        "goal": "掌握 K-Means 演算法在無標籤資料探勘中的數學推導與實作步驟，學會選取最優群數 K 值並評估分群品質",
        "exec_summary": "本週深入講授非監督式學習經典演算法——K-Means 分群模型。授課教師以設定群數 K=5 為例，詳細推導演算法在多維向量空間中的運作流程：從隨機初始化 5 個質心（Centroids）出發，透過歐氏距離（Euclidean Distance）將所有資料點指派給最近之質心，再依各簇內樣本之幾何中心重新計算新質心位置。課程推導了簇內平方和（WCSS）的收斂過程，並指導學員如何運用肘部法則（Elbow Method）與輪廓係數（Silhouette Score）科學化決定最佳群數。",
        "mermaid_title": "K-Means 演算法迭代收斂與質心更新流程",
        "mermaid": """flowchart TD
    Init["初始化: 在特徵向量空間中隨機挑選 K 個初始質心 (Centroids)"] --> Assign
    Assign["階段一: 樣本指派 (Assignment)<br/>計算各樣本與所有質心之歐氏距離，將樣本指派至最近之簇"] --> Update
    Update["階段二: 質心重算 (Update)<br/>計算各簇內所有樣本之特徵均值，更新質心座標位置"] --> Check{"檢查收斂條件<br/>(質心位移小於門檻 ε 或達到最大迭代次數)"}
    
    Check -->|未收斂| Assign
    Check -->|已收斂| Evaluate["分群品質評估: 計算輪廓係數 (Silhouette) 與 WCSS"]""",
        "takeaways": [
            ("敏感於初始質心選取與尺度縮放", "K-Means 演算法極易陷入局部最優解（Local Optima），且對特徵量綱極度敏感。實務中必須先進行特徵標準化（Standardization），並採用 K-Means++ 機率初始化策略以加快收斂。"),
            ("肘部法則（Elbow Method）的客觀判讀", "透過繪製 WCSS 隨群數 K 增加之折線圖，尋找下降斜率劇烈變緩的轉折點（Elbow Point），搭配輪廓係數（Silhouette Score）檢驗簇內緊密度與簇間分離度。")
        ]
    }
    build_session(
        date_str="2026-03-26",
        talk_id="AI-OPT-05-KMEANS-CLUSTERING",
        title="進階人工智慧與最佳化 Lesson 05：K-Means 非監督式分群演算法原理、向量空間與質心迭代收斂",
        file_prefix="20260326-KMeans分群演算法與向量空間",
        lines_subset=lines_subset,
        sections_cfg=sections_cfg,
        summary_cfg=summary_cfg
    )
    add_catalog_entry(
        session_no=183,
        topic="進階人工智慧與最佳化 Lesson 05：K-Means 非監督式分群演算法原理、向量空間與質心迭代收斂",
        speakers="授課講師, 學員",
        scenario="classroom-lecture",
        note_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260326-KMeans分群演算法與向量空間.md",
        full_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260326-KMeans分群演算法與向量空間.full.md"
    )


if __name__ == "__main__":
    build_step_session5()
