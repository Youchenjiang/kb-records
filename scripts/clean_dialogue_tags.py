#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path

UNIV_DIR = Path("c:/Users/g1014308/Documents/GitHub/Youchen/record-list/4-University")

def main():
    for f in UNIV_DIR.glob("**/*-proofread.md"):
        t = f.read_text(encoding="utf-8")
        
        def repl(m):
            q = m.group(1).strip()
            ans = m.group(2).strip()
            return f"**【學員】**：{q}\n\n**【授課講師】**：{ans}"

        t = re.sub(r'學生問：[「"](.*?)["」]\n+([^\n]+)', repl, t)
        t = re.sub(r'同學問：[「"](.*?)["」]\n+([^\n]+)', repl, t)
        t = re.sub(r'有人問：[「"](.*?)["」]\n+([^\n]+)', repl, t)
        
        # Deduplicate consecutive tags
        t = re.sub(r"(\*\*【授課講師】\*\*：\s*)+", "**【授課講師】**：", t)
        t = re.sub(r"(\*\*【學員】\*\*：\s*)+", "**【學員】**：", t)
        
        f.write_text(t, encoding="utf-8")
        print(f"Cleaned dialogue in {f.name}")

if __name__ == "__main__":
    main()
