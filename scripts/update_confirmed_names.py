#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Confirmed Proper Names across scripts, proofreads, and summaries:
1. 研究生 / 報告人: 沈柏寧 (Confirmed by user)
2. 指導教授: 陳奕明博士 (Confirmed by user)
3. 論文二指導教授: 蔡志豐博士 (Confirmed by user)
"""

from pathlib import Path
import re

BASE_DIR = Path("c:/Users/g1014308/Documents/GitHub/Youchen/record-list")

# 1. Update build_perfect_proofreads.py
script_file = BASE_DIR / "scripts" / "build_perfect_proofreads.py"
code = script_file.read_text(encoding="utf-8")

code = code.replace("沈國立", "沈柏寧")
code = code.replace("沈博寧", "沈柏寧")
code = code.replace("陳博士", "陳奕明博士")
code = code.replace("蔡志峰", "蔡志豐")
# avoid 陳奕明博士博士 if any
code = code.replace("陳奕明博士博士", "陳奕明博士")

script_file.write_text(code, encoding="utf-8")
print(f"Updated {script_file}")

# 2. Run build_perfect_proofreads.py
import subprocess
res = subprocess.run(
    ["C:\\MyAPP\\Anaconda3\\envs\\recording-transcribe-gpu\\python.exe", str(script_file)],
    capture_output=True,
    text=True,
    cwd=str(BASE_DIR.parent)
)
print("build_perfect_proofreads output:")
print(res.stdout)
if res.stderr:
    print("build_perfect_proofreads error:", res.stderr)

# 3. Update summaries
outputs_dir = BASE_DIR / "transcribe_outputs"
for sum_file in outputs_dir.rglob("*-summary.md"):
    text = sum_file.read_text(encoding="utf-8")
    orig = text
    text = text.replace("沈國立", "沈柏寧")
    text = text.replace("沈博寧", "沈柏寧")
    text = text.replace("陳一鳴", "陳奕明博士")
    text = text.replace("陳博士", "陳奕明博士")
    text = text.replace("蔡志峰", "蔡志豐")
    text = text.replace("陳奕明博士博士", "陳奕明博士")
    if text != orig:
        sum_file.write_text(text, encoding="utf-8")
        print(f"Updated summary: {sum_file.name}")

print("All confirmed names updated successfully!")
