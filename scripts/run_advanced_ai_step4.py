#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate and update catalogs for Session 4 (2026-03-19).
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_advanced_ai_optimization import build_session, raw_lines
from scripts.run_advanced_ai_step import add_catalog_entry


def build_step_session4():
    lines_subset = raw_lines[7115:11784]
    sections_cfg = [
        ("🎯 全英語專題發表規範與評分指標：8分鐘限時、結構化論述與觀眾連結", (0.0, 0.33)),
        ("🗣️ 各組研究提案實戰發表：資料集洞察、假說建立與技術架構展示", (0.33, 0.66)),
        ("💬 教師講評與同儕深度問答：模型泛化性、評估指標合理性與下一步方向", (0.66, 1.0)),
    ]
    summary_cfg = {
        "topic": "專題提案全英語發表（EMI Proposal Rehearsal）、8分鐘時間控制、同儕互動與問題答辯",
        "modules": "EMI Presentation, Time Management, Peer Review, Problem Formulation, Model Evaluation",
        "goal": "訓練學員於國際研討會情境下進行全英文學術簡報，掌握結論先行、精準控時與答辯應變技巧",
        "exec_summary": "本週進行學期專題提案（Project Proposal）全英文發表考核。授課教師嚴格設定每組 8 分鐘發表限制，強調「先發表或後發表並不影響分數，關鍵在於講者的颱風、時間掌握與訊息精煉度」。各組依序登台展示針對選定資料集之探索洞見、預計採用之機器學習演算法與驗證指標。教師針對各組簡報之視覺文字密度、模型泛化能力假設及評估指標合理性進行逐一點評，並引導全班進行高強度同儕詰問與技術交流。",
        "mermaid_title": "8分鐘學術專題全英文發表結構與時間分配",
        "mermaid": """flowchart TD
    Intro["00:00 - 01:30 引言與問題意識<br/>背景挑戰、商業/學術痛點、核心假說"] --> Data
    Data["01:30 - 03:30 資料集與特徵工程<br/>資料分布、偏誤處理、關鍵特徵抽取"] --> Model
    Model["03:30 - 06:00 演算法與架構設計<br/>模型選擇依據、驗證策略、集成架構"] --> Metrics
    Metrics["06:00 - 07:00 預期成果與衡量指標<br/>AUC / F1 / RMSE 指標定義、商業價值"] --> Wrap
    Wrap["07:00 - 08:00 結論與未來工作<br/>核心結論摘要、下一階段里程碑"] --> QA
    QA["Q&A 答辯環節: 教師講評與同儕詰問"]""",
        "takeaways": [
            ("嚴格遵守發表時間紀律（Time Discipline）", "演講超時在國際學術研討會中是嚴重扣分項。學員必須經過反覆排練，將內容濃縮在 8 分鐘內，確保核心結論在時間結束前完整交付。"),
            ("以受眾為中心（Audience-Centric）的投影片設計", "投影片是輔助溝通的工具，切忌密密麻麻放置大量代碼或文字。應以清晰架構圖、統計分布圖為核心，講者面向觀眾眼神接觸，而非背對觀眾念稿。")
        ]
    }
    build_session(
        date_str="2026-03-19",
        talk_id="AI-OPT-04-PROPOSAL-PRESENTATIONS",
        title="進階人工智慧與最佳化 Lesson 04：專案提案全英語發表演練、限時控時與同儕評核",
        file_prefix="20260319-專案提案全英語發表與評審問答",
        lines_subset=lines_subset,
        sections_cfg=sections_cfg,
        summary_cfg=summary_cfg
    )
    add_catalog_entry(
        session_no=182,
        topic="進階人工智慧與最佳化 Lesson 04：專案提案全英語發表演練、限時控時與同儕評核",
        speakers="授課講師, 學員",
        scenario="classroom-lecture",
        note_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260319-專案提案全英語發表與評審問答.md",
        full_path="./5-Master/1-First-Year/Spring-Semester/AdvancedAI-Optimization/20260319-專案提案全英語發表與評審問答.full.md"
    )


if __name__ == "__main__":
    build_step_session4()
