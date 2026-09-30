#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit and update dates across deliverables using Xiaomi MediaCreated metadata.
"""

import subprocess
import re
import glob
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 1. Query MediaCreated from audio/processed via PowerShell
ps_cmd = """
$shell = New-Object -ComObject Shell.Application
$folder = $shell.Namespace((Get-Item "audio/processed").FullName)
$items = $folder.Items()
foreach ($item in $items) {
    $s214 = $folder.GetDetailsOf($item, 214)
    if ($s214) {
        $cleanDate = $s214 -replace "[\u200e\u200f]", ""
        Write-Output "$($item.Name):::$cleanDate"
    }
}
"""
out = subprocess.check_output(["powershell", "-Command", ps_cmd], text=True, encoding="utf-8")
audio_dates = {}
for line in out.splitlines():
    if ":::" in line:
        fn, dt_str = line.split(":::", 1)
        base = os.path.splitext(fn.strip())[0]
        m = re.search(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", dt_str)
        if m:
            iso_date = f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
            audio_dates[base] = (iso_date, dt_str.strip())

print(f"Loaded {len(audio_dates)} Xiaomi recording timestamps from audio/processed.")

# Mapping each audio folder / file to its exact deliverable markdown file
# Based on build scripts inspection:
mapping = {
    # Machine Learning (4-University/2024-UndergraduateCourses)
    "週一 09點08分": "4-University/2024-UndergraduateCourses/機器學習-01-監督式學習分類與決策樹演算法ID3-proofread.md",
    "週一 10點23分": "4-University/2024-UndergraduateCourses/機器學習-02-貝氏分類器與支援向量機SVM原理-proofread.md",
    "週一 10點12分": "4-University/2024-UndergraduateCourses/機器學習-03-深度學習導論與多層感知機類神經網路-proofread.md",
    "週一 11點05分": "4-University/2024-UndergraduateCourses/機器學習-04-特徵萃取與梯度下降損失函數最佳化-proofread.md",
    "週一 09點06分": "4-University/2024-UndergraduateCourses/機器學習-05-支援向量機SVM最大間距超平面與軟邊界最佳化-proofread.md",

    # Master Seminar (5-Master/2026-MasterSeminar-SoftwareSecurity)
    "週一 18點48分": "5-Master/2026-MasterSeminar-SoftwareSecurity/碩士專題討論-01-自動化漏洞修復APR根因分析與兩階段修補驗證-proofread.md",

    # NCU IM Conference (5-Master/2026-AcademicConference-NCU-IM)
    "週五 08點59分": "5-Master/2026-AcademicConference-NCU-IM/NCU-IM-01-智慧醫療-老年失智症多模態神經與認知特徵預測模型-proofread.md",
    "週五 11點35分": "5-Master/2026-AcademicConference-NCU-IM/NCU-IM-02-智慧金融-量化投資多因子選股與動態本益比進出場策略-proofread.md",
    "週五 14點17分": "5-Master/2026-AcademicConference-NCU-IM/NCU-IM-03-機器學習-特徵精簡與實例樣本選取雙向管線效能優化-proofread.md",

    # Industry Keynote (5-Master/2026-IndustryKeynote-GenAI-Cybersecurity)
    "週五 15點03分 ai 演講": "5-Master/2026-IndustryKeynote-GenAI-Cybersecurity/勤業眾信副總-生成式AI浪潮與企業資安治理-proofread.md",

    # Software Engineering (4-University/2025-SoftwareEngineering)
    "週三 14點03分 軟工結束": "4-University/2025-SoftwareEngineering/軟工期末-系統架構循序圖與高並發壓力測試-proofread.md",

    # Network Lab (4-University/2024-UndergraduateCourses)
    "週二 16點05分": "4-University/2024-UndergraduateCourses/電腦網路實驗-01-UTP雙絞線跳線製作與衰減標準-proofread.md",

    # DevOps & Database Security & CTF (4-University/2024-UndergraduateCourses)
    "週二 15點05分": "4-University/2024-UndergraduateCourses/DevOps自動化維運-01-Ansible無代理架構與Playbook宣告式部署-proofread.md",
    "週一 20點00分": "4-University/2024-UndergraduateCourses/資料庫資安-01-PostgreSQL抄寫協議認證繞過與特權提升漏洞解析-proofread.md",
    "週三 19點18分": "4-University/2024-UndergraduateCourses/資安實戰-01-CTF圖片隱寫術分析與OSINT地理定位解題實務-proofread.md",

    # HCI (4-University/2024-UndergraduateCourses)
    "週二 15點38分": "4-University/2024-UndergraduateCourses/人機互動與UX設計-01-行為動機與人境互動模式-proofread.md",
    "週二 16點53分": "4-University/2024-UndergraduateCourses/人機互動與UX設計-02-使用者經驗定義與智慧產品易用性-proofread.md",

    # Research Methodology (5-Master/2025-ResearchMethodology)
    "週三 14點00分": "5-Master/2025-ResearchMethodology/研究方法-01-概念層次操作化與變數定義-proofread.md",
    "週三 15點42分": "5-Master/2025-ResearchMethodology/研究方法-02-假說建立與理論框架實證檢驗-proofread.md",

    # Master Research (5-Master/2026-MasterResearch-AndroidMalware)
    "週四 12點28分": "5-Master/2026-MasterResearch-AndroidMalware/實驗室專案會議-新年度整合型研究計畫與平台架構規劃-proofread.md",
    "週四 12點35分": "5-Master/2026-MasterResearch-AndroidMalware/碩士研究專題-Android惡意程式行為子圖與抗混淆GNN檢測-proofread.md",

    # English Presentation (4-University/2024-UndergraduateCourses)
    "週三 20點11分": "4-University/2024-UndergraduateCourses/英語專題發表-AI教育表現特徵工程與學習成效過濾法預測-proofread.md",

    # Advanced AI Optimization (5-Master/2025-AdvancedAI-Optimization)
    "週四 09點11分": "5-Master/2025-AdvancedAI-Optimization/AI-Optimization-01-課程導論與學術倫理規範-proofread.md",
    "週四 10點03分": "5-Master/2025-AdvancedAI-Optimization/AI-Optimization-02-對抗性機器學習與蒙特卡羅最佳化-proofread.md",
    "週四 11點30分": "5-Master/2025-AdvancedAI-Optimization/AI-Optimization-03-感測器能源模型與高並發基準測試-proofread.md",
}

print(f"\nPerforming exact date updates on {len(mapping)} deliverables...")

updated_count = 0
for audio_key, rel_proof in mapping.items():
    if audio_key not in audio_dates:
        print(f"[SKIP] Audio key not in audio_dates: {audio_key}")
        continue

    iso_date, raw_dt = audio_dates[audio_key]
    proof_path = REPO_ROOT / rel_proof

    if not proof_path.exists():
        print(f"[WARNING] Proofread file not found: {proof_path}")
        continue

    text = proof_path.read_text(encoding="utf-8")
    
    # Check current date in frontmatter
    dm = re.search(r'date:\s*"([^"]+)"', text)
    current_date = dm.group(1) if dm else "None"

    if current_date != iso_date:
        if dm:
            new_text = re.sub(r'date:\s*"[^"]+"', f'date: "{iso_date}"', text, count=1)
        else:
            # insert date into frontmatter
            new_text = re.sub(r'(---\n)', f'\\1date: "{iso_date}"\n', text, count=1)

        proof_path.write_text(new_text, encoding="utf-8")
        print(f"  [UPDATED] {proof_path.name}")
        print(f"            {current_date} -> {iso_date} ({raw_dt})")
        updated_count += 1
    else:
        print(f"  [UNCHANGED] {proof_path.name} (already {iso_date})")

print(f"\nSuccessfully updated {updated_count} files.")
