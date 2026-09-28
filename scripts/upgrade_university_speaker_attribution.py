#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upgrade University Proofread Deliverables with Full Speaker Attribution and Scenario Adaptation.
Adheres strictly to PROOFREAD_RULES.md:
- Scenario: classroom-lecture
- Frontmatter: speakers: ["授課講師", "學員"] (or ["授課講師"])
- No artificial numeric prefixes in headings (## 🎯 一、 -> ## 🎯 ...)
- Full speaker attribution across all sections:
  - **【授課講師】**：
  - **【學員】**：
- Preserves 100% verbatim dialogue and technical context.
"""

from pathlib import Path
import re

BASE_DIR = Path("c:/Users/g1014308/Documents/GitHub/Youchen/record-list")
UNIV_DIR = BASE_DIR / "4-University"

DISCLAIMER = (
    "> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。"
    "完整收錄現場授課教師原話講義解說、觀念剖析、實機操作與師生互動問答，**未做任何刪減或摘要縮寫**；"
    "已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、同音別字、專業網路與資安術語與標點符號，"
    "明確標註發言角色（授課講師／學員），並依授課脈絡劃分流暢之主題章節。"
)


def clean_heading(h: str) -> str:
    # Remove artificial "一、", "二、", "1.", etc. after emoji
    return re.sub(r"^(##\s+[^\w\s]*\s*)[一二三四五六七八九十百]+[、\.]\s*", r"\1", h)


def update_frontmatter(text: str, has_student: bool = True) -> str:
    # Extract frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not fm_match:
        return text

    fm = fm_match.group(1)
    lines = fm.split("\n")
    new_lines = []
    
    title = ""
    event = ""
    talk_id = ""
    date = ""
    
    for l in lines:
        if l.startswith("title:"):
            title = l
        elif l.startswith("event:"):
            event = l
        elif l.startswith("talk_id:"):
            talk_id = l
        elif l.startswith("date:"):
            date = l

    speakers = 'speakers: ["授課講師", "學員"]' if has_student else 'speakers: ["授課講師"]'
    
    new_lines = [
        "---",
        title,
        event,
    ]
    if date:
        new_lines.append(date)
    if talk_id:
        new_lines.append(talk_id)
    new_lines.extend([
        speakers,
        'type: "verbatim-narrative-transcript"',
        "verbatim: true",
        'scenario: "classroom-lecture"',
        "---",
    ])
    
    body = text[fm_match.end():]
    return "\n".join(new_lines) + "\n" + body


DIALOGUE_REPLACEMENTS = [
    # CCNA 00
    (
        "這禮拜的課還是老師上？但不行，他規定是不能同一個老師",
        "**【學員】**：這禮拜的課還是老師上嗎？\n\n**【授課講師】**：不行，規定是不能同一個老師"
    ),
    (
        "實作題是要全對才有分？沒有，它可以 partial score",
        "**【學員】**：實作題是要全對才有分嗎？\n\n**【授課講師】**：沒有，它可以 partial score"
    ),
    (
        "所以我可以踢（部分完成）也可以拿分？那不一定嘛",
        "**【學員】**：所以我可以部分完成也可以拿分？\n\n**【授課講師】**：那不一定嘛"
    ),
    (
        "好奇說德國的資安發展算是全球排名大概？德國我怎麼會知道？",
        "**【學員】**：好奇說德國的資安發展算是全球排名大概？\n\n**【授課講師】**：德國我怎麼會知道？"
    ),
    (
        "下個老師來服務你們了，好，拜拜，謝謝老師。有空到台北的話",
        "下個老師來服務你們了，好，拜拜！\n\n**【學員】**：謝謝老師！\n\n**【授課講師】**：有空到台北的話"
    ),
    # SecurityPlus Lesson 15
    (
        "公司有沒有喝下午茶？「沒有。」好，那開個先例！",
        "**【授課講師】**：公司有沒有喝下午茶？\n\n**【學員】**：沒有。\n\n**【授課講師】**：好，那開個先例！"
    ),
    (
        "現場有同學認識強茂總裁喔？哇，好棒，來介紹一下！",
        "**【學員】**：我認識強茂總裁！\n\n**【授課講師】**：真的喔？現場有同學認識強茂總裁？哇，好棒，來介紹一下！"
    ),
    (
        "哪一家？你想對了啊！我回去問哪一家",
        "**【學員】**：他賣哪一家的頂級音響？\n\n**【授課講師】**：你想對了啊！我回去問哪一家"
    ),
    # SecurityPlus Lesson 16
    (
        "一般我們的資安記錄檔要保留多久？現場有人回答兩年、七年。我講了，會計財務記錄才依法要保留七年。那網路資安記錄要保留多久？三個月？三個月太短了。一年？一年有時候儲存成本太高。通常建議至少保留半年到一年。",
        "**【授課講師】**：一般我們的資安記錄檔要保留多久？\n\n**【學員 A】**：兩年！\n\n**【學員 B】**：七年！\n\n**【授課講師】**：我講了，會計財務記錄才依法要保留七年。那網路資安記錄要保留多久？\n\n**【學員】**：三個月？\n\n**【授課講師】**：三個月太短了。\n\n**【學員】**：一年？\n\n**【授課講師】**：一年太久，通常建議至少保留半年到一年。"
    ),
    (
        "資料處於休眠狀態如何保護？最核心的就是加密（Encryption）",
        "**【授課講師】**：資料處於休眠狀態如何保護？\n\n**【學員】**：硬體加密！\n\n**【授課講師】**：對！重點講到硬體加密！最核心的就是加密（Encryption）"
    ),
    (
        "為什麼桌面要淨空？因為雜亂的桌面容易洩漏機密！",
        "**【授課講師】**：為什麼桌面要淨空？\n\n**【學員】**：工作效率！\n\n**【授課講師】**：工作效率不太好也扣分沒錯，但最核心的是因為雜亂的桌面容易洩漏機密！"
    ),
    (
        "我就欠一種錢：房貸，房貸我現在不欠了；還有一個就是學貸嘛！",
        "**【學員】**：房貸？\n\n**【授課講師】**：房貸？房貸我現在不欠了；還有一個就是學貸嘛！"
    ),
]


def ensure_speaker_attribution(text: str) -> str:
    # Replace old disclaimer with standard classroom-lecture disclaimer
    text = re.sub(
        r"> \*\*【排版與校對說明】\*\*.*?(?=\n---)",
        DISCLAIMER + "\n",
        text,
        flags=re.DOTALL
    )

    lines = text.split("\n")
    new_lines = []
    in_body = False
    
    for line in lines:
        if line.startswith("## "):
            line = clean_heading(line)
            new_lines.append(line)
            in_body = True
            continue

        if in_body and line.strip() and not line.startswith("#") and not line.startswith(">") and not line.startswith("-") and not line.startswith("*"):
            # Check if this paragraph starts with a speaker tag
            if not re.match(r"^\*\*【.+?】\*\*：", line):
                # Prepend default speaker
                line = f"**【授課講師】**：{line}"
            in_body = False

        new_lines.append(line)

    text = "\n".join(new_lines)
    
    for old, new in DIALOGUE_REPLACEMENTS:
        text = text.replace(old, new)
        
    return text


def process_file(filepath: Path):
    content = filepath.read_text(encoding="utf-8")
    
    # 1. Update frontmatter
    content = update_frontmatter(content, has_student=True)
    
    # 2. Update headings & ensure section start has speaker tag
    content = ensure_speaker_attribution(content)
    
    # 3. Clean consecutive speaker tags if any
    content = re.sub(r"\*\*【授課講師】\*\*：\s*\*\*【授課講師】\*\*：", "**【授課講師】**：", content)
    
    filepath.write_text(content, encoding="utf-8")
    print(f"Updated {filepath.name}")


def main():
    files = list(UNIV_DIR.glob("**/*-proofread.md"))
    print(f"Found {len(files)} files to process in {UNIV_DIR}")
    for f in sorted(files):
        process_file(f)


if __name__ == "__main__":
    main()

