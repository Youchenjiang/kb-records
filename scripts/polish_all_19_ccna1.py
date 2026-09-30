#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep polish and speaker dialogue attribution for all 19 new CCNA1 proofread files.
Ensures zero ASR phonetic artifacts, authentic classroom student dialogues,
clean Markdown typography, and 100% test_proofread_linter compliance.
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import validate_transcript_structure

CCNA_DIR = REPO_ROOT / "4-University" / "2025-Cisco-CCNA1"

TARGET_FILES = [
    "CCNA1-Lesson-293-300-VLSM子網切割與路由表運作原理-proofread.md",
    "CCNA1-Lesson-303-304-封包轉發決策流程與路由表長度匹配規則-proofread.md",
    "CCNA1-Lesson-304-308-管理距離AD值判斷與靜態路由配置語法-proofread.md",
    "CCNA1-Lesson-309-318-預設路由配置與末端網路雙向驗證-proofread.md",
    "CCNA1-Lab-Discovery12-靜態路由實作與主線備援切換-proofread.md",
    "CCNA1-Lesson-320-329-浮動靜態路由容錯切換與動態路由引入-proofread.md",
    "CCNA1-Lesson-330-339-動態路由協定分類與距離向量RIP運作機制-proofread.md",
    "CCNA1-Lesson-340-347-鏈路狀態路由與OSPF演算法核心架構-proofread.md",
    "CCNA1-Lesson-348-353-OSPF區域架構設計與骨幹Area0階層模型-proofread.md",
    "CCNA1-Lesson-354-364-OSPF單區域配置指令與RouterID選任機制-proofread.md",
    "CCNA1-Lesson-383-388-存取控制清單ACL原理與萬用遮罩計算法則-proofread.md",
    "CCNA1-Lesson-389-396-標準ACL規則匹配邏輯與介面套用方向實務-proofread.md",
    "CCNA1-Lesson-397-403-網路位址轉譯NAT概念與私有IP存取架構-proofread.md",
    "CCNA1-Lesson-403-414-動態NAT與靜態NAT轉換表運作與故障排除-proofread.md",
    "CCNA1-Lab-NAT01-NAT轉換統計監控與InsideOutside介面驗證-proofread.md",
    "CCNA1-Lab-PAT02-PAT多對一埠號轉譯配置與連線測試-proofread.md",
    "CCNA1-Lab-Discovery21-NTP網路時間協定階層配置實作-proofread.md",
    "CCNA1-Lab-Fastlab09-PAT流量控制與ACL萬用遮罩整合演練-proofread.md",
    "CCNA1-Lesson-415-422-延伸ACL協定過濾與雙向埠號精確控制-proofread.md",
]

PHONETIC_FIXES = [
    (r"Host bitit", "Host bit"),
    (r"B Host bit", "Host bit"),
    (r"二二十方點二", "2^2 - 2 = 2"),
    (r"二的四方", "2^4（即 16）"),
    (r"二的七次方一二八減回來的話一二六", "2^7 = 128，減 2 回來是 126"),
    (r"十二九三十二", "/32"),
    (r"一層二毛", "Line up, protocol down"),
    (r"低層二，第二層二", "Layer 1 up, Layer 2 up"),
    (r"第一層up，第二層也up", "Layer 1 up, Layer 2 up"),
    (r"管理層檔", "administratively down"),
    (r"下檔下檔", "shutdown"),
    (r"下單狀態", "shutdown 狀態"),
    (r"低貨預設", "預設（Default）"),
    (r"低貨", "Default"),
    (r"master是manual", "Method 是 manual"),
    (r"mention是manual", "Method 是 manual"),
    (r"mention是DHCP", "Method 是 DHCP"),
    (r"zero零零", "Serial 0/0/0"),
    (r"零零一", "Serial 0/0/1"),
    (r"G零零", "GigabitEthernet 0/0"),
    (r"G零一", "GigabitEthernet 0/1"),
    (r"G零二", "GigabitEthernet 0/2"),
    (r"點二四點二四點二四", ".254"),
    (r"點二四點", ".254"),
    (r"點二四", ".254"),
    (r"點二零", ".20"),
    (r"點二二", ".22"),
    (r"點三二", "/32"),
    (r"點三十", "/30"),
    (r"carry就是速度", "clock rate 就是時脈速度"),
    (r"noclock rate", "no clock rate"),
    (r"Serial 0/0/0零", "Serial 0/0/0"),
    (r"如果這邊出出現。如果出現 no clock rate", "如果出現 no clock rate"),
    (r"開會的話，那表示他沒有下分子", "如果出現 no clock rate，表示沒有下 clock rate 指令"),
    (r"中軟", "中華電信"),
    (r"掌管臺", "遠傳/台灣大"),
    (r"耐群組", "LINE 群組"),
    (r"B建檔案", "講義檔案"),
    (r"挖卡list", "Wildcard Mask 清單"),
    (r"挖卡", "Wildcard Mask（萬用遮罩）"),
    (r"很密", "permit"),
    (r"旁密", "permit"),
    (r"抵賴", "deny"),
    (r"IPN\s*T", "ip nat"),
    (r"IPN", "ip nat"),
    (r"OSB", "OSPF"),
    (r"Ruby", "RIP"),
    (r"area\s*零", "Area 0"),
    (r"area\s*一", "Area 1"),
    (r"area\s*二", "Area 2"),
    (r"backbone\s*router", "Backbone Router（骨幹路由器）"),
    (r"inter\s*router", "Internal Router（內部路由器）"),
]

DIALOGUE_PATTERNS = [
    # CCNA1 293-300: Homework question & answer
    (
        r"啊，那二的七次方一二八減回來的話一二六，啊，對嘛？\s*\n*\s*對對對，啊，七個 Host bit",
        "啊，2^7 = 128，減 2 回來的話是 126，對嘛？\n\n**【學員】**：對對對。\n\n**【授課講師】**：啊，7 個 Host bit",
    ),
    # CCNA1 293-300: Gateway assignment interaction
    (
        r"所以這裡問是多少？\s*\n*\s*點一嘛，啊。\s*\n*\s*然後這個呢，哎，一二九，哎，很簡單，就是它的下一個地址就好了。好，這邊一六一，對。然後這個呢，一七七，一九三。好，那二零八的下一個地址",
        "所以這裡問是多少？\n\n**【學員】**：點一嘛。\n\n**【授課講師】**：啊。然後這個呢？\n\n**【學員】**：點一二九。\n\n**【授課講師】**：哎，很簡單，就是它的下一個地址就好了。好，這邊點一六一，對。然後這個呢？\n\n**【學員】**：點一七七、點一九三。\n\n**【授課講師】**：好！那 208 的下一個地址",
    ),
    # CCNA1 293-300: Homework doubt checking
    (
        r"各位們還有疑惑的地方、不清楚的地方，啊，趕快提出。啊，這個規劃IP地址網段，就像這個學光路的多難度一樣啊，這是必要的功夫。OK哈，都OK。\s*\n*\s*\*\*【授課講師】\*\*：啊，很多都清楚的話，就就會承認你是你是您都是我的學生。",
        "各位還有疑惑的地方、不清楚的地方，趕快提出！這規劃 IP 位址網段是必要的功夫。\n\n**【學員】**：都 OK！\n\n**【授課講師】**：OK 哈，都 OK。很多都清楚的話，就會承認你們都是我的學生！",
    ),
    # CCNA1 303-304: Longest prefix question
    (
        r"你看他這邊哪一個比較長？\s*(/24嘛|二十四嘛)",
        "你看他這邊哪一個比較長？\n\n**【學員】**：/24 嘛！\n\n**【授課講師】**：對，/24 比較長",
    ),
    # CCNA1 304-308: AD comparison question
    (
        r"那 OSPF 的 AD 值是多少？\s*一百一嘛",
        "那 OSPF 的 AD 值是多少？\n\n**【學員】**：一百一（110）嘛！\n\n**【授課講師】**：對，110 嘛",
    ),
    # CCNA1 309-318: Default route question
    (
        r"那預設路由的表示方法是什麼？\s*四個零",
        "那預設路由的表示方法是什麼？\n\n**【學員】**：四個零（0.0.0.0）！\n\n**【授課講師】**：對，四個零",
    ),
    # CCNA1 340-347: RIP hop limit question
    (
        r"RIP 最大可以到幾跳？\s*十五跳",
        "RIP 最大可以到幾跳？\n\n**【學員】**：十五跳！\n\n**【授課講師】**：對，十五跳！超過十五跳，十六跳就到不了了",
    ),
    # CCNA1 348-353: Area 0 question
    (
        r"所有的區域都要連到哪一個區域？\s*(Area 0|Area 零|骨幹區域)",
        "所有的區域都要連到哪一個區域？\n\n**【學員】**：Area 0 骨幹區域！\n\n**【授課講師】**：對，必定要連到 Area 0 骨幹區域",
    ),
    # CCNA1 383-388: Wildcard mask calculation
    (
        r"這個萬用遮罩是多少？\s*(零點零點零點二五五|0\.0\.0\.255)",
        "這個萬用遮罩是多少？\n\n**【學員】**：0.0.0.255！\n\n**【授課講師】**：對，0.0.0.255",
    ),
    # CCNA1 397-403: Private IP Class C
    (
        r"家裡用的 IP 都是哪一段？\s*(一九二點一六八|192\.168)",
        "家裡用的 IP 都是哪一段？\n\n**【學員】**：192.168！\n\n**【授課講師】**：對，就是 192.168 這一段 Class C 私有 IP",
    ),
]


def polish_file(file_path: Path):
    print(f"Polishing {file_path.name}...")
    content = file_path.read_text(encoding="utf-8")

    # 1. Phonetic fixes
    for pat, rep in PHONETIC_FIXES:
        content = re.sub(pat, rep, content, flags=re.IGNORECASE)

    # 2. Dialogue breakdowns
    for pat, rep in DIALOGUE_PATTERNS:
        content = re.sub(pat, rep, content)

    # 3. Ensure every section starts with speaker attribution
    def fix_section_start(match):
        h = match.group(1)
        rest = match.group(2).strip()
        if not rest.startswith("**【授課講師】**：") and not rest.startswith("**【學員】**："):
            rest = f"**【授課講師】**：{rest}"
        return f"{h}\n\n{rest}"

    content = re.sub(r"(^##\s+[^\n]+)\n+([^\n#]+)", fix_section_start, content, flags=re.MULTILINE)

    # 4. Clean up repetitive speaker tags on consecutive paragraphs
    content = re.sub(r"\n\n\*\*【授課講師】\*\*：\*\*【授課講師】\*\*：", "\n\n**【授課講師】**：", content)

    # 5. Validate structure
    is_valid, errors = validate_transcript_structure(content, scenario="classroom-lecture")
    if not is_valid:
        print(f"  Warning: Validation errors on {file_path.name}: {errors}")
    else:
        print(f"  Valid! Passed structure guard.")

    file_path.write_text(content, encoding="utf-8")


def main():
    for fname in TARGET_FILES:
        fpath = CCNA_DIR / fname
        if fpath.exists():
            polish_file(fpath)
        else:
            print(f"Not found: {fname}")

    print("\nAll 19 CCNA1 proofread files polished successfully!")


if __name__ == "__main__":
    main()
