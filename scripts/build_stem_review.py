#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build STEM & Networking Semester Review deliverables:
- NET-FINAL: Computer Networking Final Exam Review (IPv4, Subnetting, Security)
- PHYS-01: General Physics: Circular Motion, Tangential Velocity, Coulomb's Law
- PHYS-02: General Physics: Magnetic Fields, Closed Field Lines, Magnetic Flux
- MATH-01: Mathematics: Number System Expansion, Imaginary Unit i, Complex Numbers
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_undergrad_courses import clean_text, segment_into_dialogue_paragraphs
from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "4-University" / "2024-Fall-SemesterCourses"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"


def fix_stem_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in STEM review lectures."""
    replacements = [
        ("整數與分鐘", "等速率圓周運動"),
        ("整數度", "等速度"),
        ("整數率", "等速率"),
        ("正變、負變", "正電、負電"),
        ("十一線", "電力線與磁力線"),
        ("日半人", "日耳曼人"),
        ("德魯", "條頓"),
        ("羅泰人", "猶太人"),
        ("i 的迴圈", "虛數單位 i 的四次循環週期"),
        ("DDNS", "DDNS (動態 DNS)"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_net_final():
    print("Building NET-FINAL (12月23日 期末)...")
    raw_path = RAW_DIR / "12月23日 期末" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_stem_typos(raw)

    title = "電腦網路期末總複習：IPv4 分類編址、子網路遮罩切割運算與網路安全加解密"
    talk_id = "NET-FINAL-REVIEW-IPV4-SUBNETTING"
    event = "大學部電腦網路核心課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.50)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:])

    builder.add_section("🎯 IPv4 分類編址架構：Class A/B/C 前導位元、私有 IP 與子網路遮罩切割", sec1)
    builder.add_section("📊 網路安全核心範疇：對稱與非對稱金鑰加密、動態 DNS 實機演練與考試須知", sec2)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部電腦網路核心課程"',
        'event: "大學部電腦網路核心課程"\ndate: "2024-12-23"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "電腦網路-期末總複習-IPv4分類編址子網路切割與網路安全實務-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：電腦網路期末考點總盤點、IPv4 分類編址（Class A/B/C）、子網路遮罩切割（Subnetting）、密碼學加解密與 DDNS 實作  
> **授課教授**：授課講師（電腦網路授課教授）  
> **核心模組**：IPv4 Classful Addressing, Subnet Masking, FLSM, Symmetric/Asymmetric Encryption, DDNS  
> **學習目標**：精熟 IPv4 分類編址前導位元判定與子網路借位遮罩計算，掌握現代密碼學安全目標與動態網域名稱解析  
> **關聯文件**：[📄 完整原話逐字稿 (電腦網路-期末總複習-IPv4分類編址子網路切割與網路安全實務-proofread.md)](./電腦網路-期末總複習-IPv4分類編址子網路切割與網路安全實務-proofread.md)

---

## 🏛️ IPv4 傳統分類編址 (Classful Addressing) 結構

```mermaid
flowchart TD
    IP["32-bit IPv4 位址"]
    
    ClassA["Class A: 0xxxxxxx (1.0.0.0 ~ 126.255.255.255)<br/>/8 預設遮罩 (255.0.0.0) | 容納 1600 萬台主機"]
    ClassB["Class B: 10xxxxxx (128.0.0.0 ~ 191.255.255.255)<br/>/16 預設遮罩 (255.255.0.0) | 容納 65534 台主機"]
    ClassC["Class C: 110xxxxx (192.0.0.0 ~ 223.255.255.255)<br/>/24 預設遮罩 (255.255.255.0) | 容納 254 台主機"]

    IP --> ClassA
    IP --> ClassB
    IP --> ClassC
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. IPv4 Class A/B/C 前導位元特徵
- **Class A**：第一個位元固定為 `0`（範圍 1 ~ 126）。第 1 個 Byte 為 Net ID，後 3 個 Bytes 為 Host ID。
- **Class B**：前兩個位元固定為 `10`（範圍 128 ~ 191）。前 2 個 Bytes 為 Net ID，後 2 個 Bytes 為 Host ID。
- **Class C**：前三個位元固定為 `110`（範圍 192 ~ 223）。前 3 個 Bytes 為 Net ID，最後 1 個 Byte 為 Host ID。

### 2. 子網路遮罩 (Subnet Mask) 切割公式
- **可用子網路數**：$2^n$，其中 $n$ 為向主機位元借用的位元數。
- **每個子網路可用主機數**：$2^h - 2$，其中 $h$ 為剩餘的主機位元數（減去網路位址與廣播位址）。

### 3. 資訊安全與加密核心
- **對稱式金鑰（Symmetric）**：加密與解密使用相同金鑰（如 AES），速度快，適合傳輸巨量數據。
- **非對稱式金鑰（Asymmetric）**：公鑰加密、私鑰解密（如 RSA/ECC），解決了金鑰分發難題。
"""
    summary_file = OUT_DIR / "電腦網路-期末總複習-IPv4分類編址子網路切割與網路安全實務-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_phys_01():
    print("Building PHYS-01 (10月25日 下午1點27分)...")
    raw_path = RAW_DIR / "10月25日 下午1點27分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_stem_typos(raw)

    title = "普通物理學 Lesson 01：等速圓周運動切線速率、向心加速度與靜電庫侖定律"
    talk_id = "PHYSICS-01-CIRCULAR-MOTION-COULOMB"
    event = "大學部普通物理核心課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 圓周運動運動學：等速率 vs. 等速度定義辨析、切線速度方向與球體脫離軌跡", sec1)
    builder.add_section("📊 靜電物理學基礎：正負電荷分類、同性相斥異性相吸與庫侖靜電力作用", sec2)
    builder.add_section("💼 電力線與電場分佈：電場強度向量、疏密程度物理意義與解題實例剖析", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部普通物理核心課程"',
        'event: "大學部普通物理核心課程"\ndate: "2024-10-25"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "普通物理-01-等速圓周運動切線速率與靜電庫侖定律-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：等速率圓周運動（Uniform Circular Motion）、切線速度向量、向心力、靜電荷庫侖定律與電場力線  
> **授課教授**：授課講師（普通物理授課教授）  
> **核心模組**：Uniform Circular Motion, Tangential Velocity, Centripetal Acceleration, Coulomb's Law, Electric Field Lines  
> **學習目標**：精確辨析等速度與等速率之向量本質，理解切線速度與向心加速度之幾何關係，掌握靜電作用力與電力線分佈  
> **關聯文件**：[📄 完整原話逐字稿 (普通物理-01-等速圓周運動切線速率與靜電庫侖定律-proofread.md)](./普通物理-01-等速圓周運動切線速率與靜電庫侖定律-proofread.md)

---

## 🏛️ 等速圓周運動之速度與加速度向量結構

```mermaid
flowchart TD
    Center["圓心 (O)"]
    Particle["運動質點 (m)"]
    Tangential["切線速度向量 v<br/>(大小恆定，方向時時刻刻改變)"]
    Centripetal["向心加速度 a_c<br/>(始終垂直於速度，指向圓心 O)"]

    Particle --> Tangential
    Particle -- "向心力 F_c = m v^2 / r" --> Center
    Particle --> Centripetal
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 「等速圓周運動」的真正物理意義
- **等速率而非等速度**：速度是具備「大小」與「方向」的向量。圓周運動中速率（純量大小）雖保持不變，但運動方向隨時間持續旋轉，因此**絕非等速度運動**，而是一種**具備加速度的變速度運動**。
- **沿切線飛出**：當繩索斷裂或向心力瞬間消失時，物體將依慣性定律（牛頓第一運動定律），沿著該瞬間的**切線方向（Tangential Direction）**以等速度直線飛出。

### 2. 靜電庫侖定律 (Coulomb's Law)
- **相互作用力**：帶電體間之靜電力大小與兩者電量乘積成正比，與距離平方成反比：
  $$F = k \frac{|q_1 q_2|}{r^2}$$
- **電力線特徵**：由正電荷出發、終止於負電荷；線條疏密代表該處電場強度。
"""
    summary_file = OUT_DIR / "普通物理-01-等速圓周運動切線速率與靜電庫侖定律-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_phys_02():
    print("Building PHYS-02 (10月25日 下午2點27分)...")
    raw_path = RAW_DIR / "10月25日 下午2點27分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_stem_typos(raw)

    title = "普通物理學 Lesson 02：磁場分佈、磁力線封閉特性與磁通量物理機制"
    talk_id = "PHYSICS-02-MAGNETIC-FIELDS-FLUX-LINES"
    event = "大學部普通物理核心課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 磁力線封閉特性：磁鐵外部 N 至 S 與內部 S 至 N 的完整無起點終點曲線", sec1)
    builder.add_section("📊 磁場強度度量：磁力線空間疏密程度、向量切線方向與高斯磁定律本質", sec2)
    builder.add_section("💼 電磁學歷史脈絡與期中複習：科學制度思維、第四章考點重點整理與練習指引", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部普通物理核心課程"',
        'event: "大學部普通物理核心課程"\ndate: "2024-10-25"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "普通物理-02-磁場分佈磁力線封閉特性與磁通量解析-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：磁場（Magnetic Field）、磁力線封閉性、高斯磁定律（無磁單極）、磁通量與電磁學考點梳理  
> **授課教授**：授課講師（普通物理授課教授）  
> **核心模組**：Magnetic Field Lines, Closed Loops, Gauss's Law for Magnetism, Magnetic Flux, Dipole  
> **學習目標**：掌握磁力線內部與外部之連續封閉迴圈物理特性，理解磁力線疏密代表磁場強度大小之幾何意涵  
> **關聯文件**：[📄 完整原話逐字稿 (普通物理-02-磁場分佈磁力線封閉特性與磁通量解析-proofread.md)](./普通物理-02-磁場分佈磁力線封閉特性與磁通量解析-proofread.md)

---

## 🏛️ 磁力線封閉迴圈 (Closed Loops) 拓撲流向

```mermaid
flowchart LR
    subgraph Magnet["磁鐵本體 (Magnet Dipole)"]
        S_Pole["S 極 (南極)"]
        N_Pole["N 極 (北極)"]
    end

    External["外部空間：由 N 極指向 S 極<br/>(N -> S)"]
    Internal["磁鐵內部：由 S 極指向 N 極<br/>(S -> N)"]

    N_Pole -- "外部空間擴散" --> External
    External --> S_Pole
    S_Pole -- "磁鐵內部貫通" --> Internal
    Internal --> N_Pole
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 磁力線的「封閉曲線」本質
- **無起點亦無終點**：電力線有始有終（始於正電荷，終於負電荷）；但磁力線是一條**連續不斷的封閉平滑曲線（Closed Loop）**。
- **流向規則**：
  - **磁鐵外部**：由 **N 極指向 S 極**。
  - **磁鐵內部**：由 **S 極指向 N 極**。
- **高斯磁定律（Gauss's Law for Magnetism）**：自然界中不存在孤立的磁單極（Magnetic Monopole），通過任何封閉曲面的淨磁通量必恆等於零：$\oint \mathbf{B} \cdot d\mathbf{A} = 0$。

### 2. 磁場強度與空間疏密關係
- **空間密集度**：磁力線越密集的地方（如磁極兩端近處），磁場強度越大；磁力線稀疏的地方，磁場強度越弱。
- **切線方向**：磁力線上任意一點的切線方向，即代表小磁針 N 極在該點所受磁力方向。
"""
    summary_file = OUT_DIR / "普通物理-02-磁場分佈磁力線封閉特性與磁通量解析-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_math_01():
    print("Building MATH-01 (10月29日 下午2點26分)...")
    raw_path = RAW_DIR / "10月29日 下午2點26分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_stem_typos(raw)

    title = "基礎數學與先修代數 Lesson 01：數系擴張、虛數單位 i 定義與複數運算架構"
    talk_id = "MATH-01-COMPLEX-NUMBERS-SYSTEM-EXPANSION"
    event = "大學部基礎數學與微積分先修課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 數系擴張歷史脈絡：從實數無解邁向複數解、虛數單位定義與代數基本定理", sec1)
    builder.add_section("📊 虛數單位 i 循環律：i 之四次方週期變換特性與高階多項式簡化運算", sec2)
    builder.add_section("💼 複數四則運算與因式分解：實部與虛部分離、不可約多項式判定與課堂練習", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部基礎數學與微積分先修課程"',
        'event: "大學部基礎數學與微積分先修課程"\ndate: "2024-10-29"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "基礎數學-01-數系擴張虛數單位i與複數運算實務-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：數系擴張（Number System Expansion）、虛數單位 $i$、複數標準式 $a+bi$、虛數四次循環律與複數四則運算  
> **授課教授**：授課講師（應用數學授課教授）  
> **核心模組**：Number Systems, Imaginary Unit i, Complex Numbers, Cyclic Powers, Fundamental Theorem of Algebra  
> **學習目標**：理解數學史上將實數系擴張至複數系之必要性，精熟虛數單位 $i$ 的四次方循環特性與複數四則代數運算  
> **關聯文件**：[📄 完整原話逐字稿 (基礎數學-01-數系擴張虛數單位i與複數運算實務-proofread.md)](./基礎數學-01-數系擴張虛數單位i與複數運算實務-proofread.md)

---

## 🏛️ 數系擴張層級架構 (Hierarchy of Number Systems)

```mermaid
flowchart TD
    N["自然數集 N (正整數)"] --> Z["整數集 Z (含零與負整數)"]
    Z --> Q["有理數集 Q (可表示為分數 p/q)"]
    Q --> R["實數集 R (加入無理數: 根號2, pi 等)"]
    R -- "解 x^2 + 1 = 0 引入虛數單位 i" --> C["複數集 C (形如 a + bi, a,b 屬於 R)"]
```

---

## 🔄 虛數單位 $i$ 之四次循環律 (Period-4 Cyclic Property)

```mermaid
flowchart LR
    i1["i^1 = i"] --> i2["i^2 = -1"]
    i2 --> i3["i^3 = -i"]
    i3 --> i4["i^4 = 1"]
    i4 --> i1
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 數系擴張與「無解」的本質
- **無實數解 vs. 無解**：方程式 $x^2 + 1 = 0$ 在傳統實數系（$\mathbb{R}$）中無解；但透過數系擴張定義**虛數單位（Imaginary Unit）**：
  $$i = \sqrt{-1} \implies i^2 = -1$$
  使得該方程式在複數系中具備兩根 $x = \pm i$。
- **複數標準表示式**：任意複數 $z \in \mathbb{C}$ 均可寫為 $z = a + bi$，其中 $a = \text{Re}(z)$ 為實部，$b = \text{Im}(z)$ 為虛部。

### 2. 虛數單位 $i$ 的四次方週期循環律
- 任意整數次方 $i^n$ 均滿足以 4 為週期的循環規律：
  $$i^{4k+1} = i, \quad i^{4k+2} = -1, \quad i^{4k+3} = -i, \quad i^{4k} = 1 \quad (k \in \mathbb{Z})$$
- 此特性使得高次項代數運算可透過「指數除以 4 取餘數」快速化簡。
"""
    summary_file = OUT_DIR / "基礎數學-01-數系擴張虛數單位i與複數運算實務-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_net_final()
    build_phys_01()
    build_phys_02()
    build_math_01()
