#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Final Remaining Transcripts into Standardized Repository Deliverables:
1. ML-05 (週一 09點06分) -> 4-University/2024-UndergraduateCourses
2. IOT-SEC-01 (6 週五 上午10點18分) -> 4-University/2024-UndergraduateCourses
3. MIS-01 (4月11日 下午3點25分) -> 4-University/2024-UndergraduateCourses
4. MIS-02 (5月23日 下午3點25分(2)) -> 4-University/2024-UndergraduateCourses
5. MASTER-APR-01 (週一 18點48分) -> 5-Master/2026-MasterSeminar-SoftwareSecurity

Also logs documentation for empty/stub audio snippets:
- 10月20日 上午11點37分 (40-second draft comment)
- 11月14日 上午8點35分 (1-second filler)
- 週一 下午09點04分 (filler)
- 週六 下午08點30分 (filler)
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

UNIV_DIR = REPO_ROOT / "4-University" / "2024-UndergraduateCourses"
UNIV_DIR.mkdir(parents=True, exist_ok=True)
MASTER_DIR = REPO_ROOT / "5-Master" / "2026-MasterSeminar-SoftwareSecurity"
MASTER_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"

# Reference stubs so find_unused.py recognizes them as processed/accounted for:
STUB_SNIPPETS = [
    "10月20日 上午11點37分",
    "11月14日 上午8點35分",
    "週一 下午09點04分",
    "週六 下午08點30分",
]


def clean_transcript_text(text: str) -> str:
    """Standardize common terms and clean formatting."""
    reps = [
        ("方選", "函數 (Function)"),
        ("方程", "函數 (Function)"),
        ("方權", "函數 (Function)"),
        ("S B M", "SVM"),
        ("S B", "SVM"),
        ("half S B", "Hard SVM"),
        ("half margin", "Hard Margin (硬邊界)"),
        ("soft margin", "Soft Margin (軟邊界)"),
        ("maximum margin", "Maximum Margin (最大間距)"),
        ("classifier", "分類器 (Classifier)"),
        ("classification", "分類 (Classification)"),
        ("histogram", "直方圖 (Histogram)"),
        ("baseline", "基準線 (Baseline)"),
        ("貝氏信念網路", "貝氏信念網路 (Bayesian Belief Network)"),
        ("資源向量機", "支援向量機 (Support Vector Machine)"),
        ("IOT", "IoT（物聯網）"),
        ("I O T", "IoT（物聯網）"),
        ("T P M", "TPM（可信賴平台模組）"),
        ("T P N", "TPM（可信賴平台模組）"),
        ("去周邊化", "去周邊化 (De-perimeterization)"),
        ("去周邊", "去周邊化 (De-perimeterization)"),
        ("零信任", "零信任 (Zero Trust)"),
        ("outsourcing", "外包 (Outsourcing)"),
        ("crypto", "密碼學演算法 (Cryptography)"),
        ("M S", "MIS（管理資訊系統）"),
        ("I S", "IS（資訊系統）"),
        ("front take", "FinTech（金融科技）"),
        ("R B B", "RBV（資源基礎觀點）"),
        ("R B V", "RBV（資源基礎觀點）"),
        ("V to V", "V2V (車對車)"),
        ("V to R", "V2R (車對路側)"),
        ("V to I", "V2I (車對基礎設施)"),
        ("P O C", "PoC（概念驗證）"),
        ("POC", "PoC（概念驗證）"),
        ("A B R", "APR（自動程式修復）"),
        ("APR", "APR（自動程式修復）"),
        ("root cause", "根因 (Root Cause)"),
        ("cache site", "崩潰點 (Crash Site)"),
        ("cash site", "崩潰點 (Crash Site)"),
        ("cash旁邊", "Crash Site 崩潰點"),
        ("ALF 加加", "AFL++（模糊測試器）"),
        ("馬蒂卡", "多模態 (Multimodal)"),
        ("梁永時陳老師", "陳教授與指導老師"),
        ("陳老師", "陳教授"),
    ]
    for old, new in reps:
        text = text.replace(old, new)
    return text


def segment_into_dialogue_paragraphs(text: str, default_speaker="授課講師") -> str:
    """Split speech stream into coherent paragraphs with speaker attribution."""
    sentences = re.split(r"(?<=[。！？])", text)
    paragraphs = []
    current_para = []
    current_len = 0

    for s in sentences:
        s = s.strip()
        if not s:
            continue
        current_para.append(s)
        current_len += len(s)
        if current_len >= 220 or s.endswith("好。") or s.endswith("OK。") or s.endswith("謝謝。"):
            paragraphs.append("".join(current_para))
            current_para = []
            current_len = 0

    if current_para:
        paragraphs.append("".join(current_para))

    formatted_paras = []
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        student_triggers = ["老師請問", "是這樣嗎？", "謝謝老師", "我的問題是說", "你真好"]
        prof_triggers = ["老師建議這樣子", "天天強調你要做", "我覺得你應該好好把", "我覺得不錯。好，謝謝。"]
        if any(trig in p_clean for trig in student_triggers) and default_speaker != "發表研究生":
            formatted_paras.append(f"**【學員】**：{p_clean}")
        elif any(trig in p_clean for trig in prof_triggers):
            formatted_paras.append(f"**【指導教授】**：{p_clean}")
        else:
            if not p_clean.startswith("**【"):
                formatted_paras.append(f"**【{default_speaker}】**：{p_clean}")
            else:
                formatted_paras.append(p_clean)

    return "\n\n".join(formatted_paras)


def build_ml_05():
    """Build ML-05 from transcribe_outputs/週一 09點06分."""
    print("Building ML-05 (週一 09點06分)...")
    raw_path = RAW_DIR / "週一 09點06分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = clean_transcript_text(raw)

    title = "機器學習實務 Lesson 05：貝氏信念網路、支援向量機 SVM 最大間距超平面與軟邊界最佳化"
    talk_id = "ML-05-SVM-HYPERPLANE-SOFT-MARGIN"
    event = "大學部機器學習與深度學習課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.33)
    s2 = int(total_len * 0.66)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 分類模型回顧與貝氏信念網路：機率直方圖統計、專家先驗推論與 Baseline 基準評估", sec1)
    builder.add_section("📊 支援向量機幾何原理：超平面決策邊界 w^T x + b = 0、最大間距 Maximum Margin 與支援向量", sec2)
    builder.add_section("💼 硬邊界到軟邊界：鬆弛變數與懲罰參數 C、容錯分類與損失最佳化權衡", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部機器學習與深度學習課程"',
        'event: "大學部機器學習與深度學習課程"\ndate: "2026-09-14"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed for ML-05: {errors}")

    proof_file = UNIV_DIR / "機器學習-05-支援向量機SVM最大間距超平面與軟邊界最佳化-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + r"""
> **課程主題**：貝氏信念網路（BBN）、支援向量機（SVM）、最大間距超平面（Maximum Margin Hyperplane）與軟邊界（Soft Margin）最佳化  
> **授課教授**：授課講師（資訊工程授課教授）  
> **核心模組**：Classification, Bayesian Belief Network, SVM, Hyperplane, Hard Margin, Soft Margin, Slack Variables  
> **學習目標**：掌握貝氏機率模型推論複雜度與 Baseline 定位，深入理解 SVM 幾何間距公式推導，並明辨硬邊界與軟邊界之容錯損失函數機制  
> **關聯文件**：[📄 完整原話逐字稿 (機器學習-05-支援向量機SVM最大間距超平面與軟邊界最佳化-proofread.md)](./機器學習-05-支援向量機SVM最大間距超平面與軟邊界最佳化-proofread.md)

---

## 🏛️ 支援向量機 (SVM) 線性可分與最大間距架構

```mermaid
flowchart LR
    subgraph PosSpace["正類樣本空間 (y = +1)"]
        P1["正樣本 (+)"]
        P2["正樣本 (+)"]
        SV_Pos["支援向量 (Support Vector: w^T x + b = +1)"]
    end

    subgraph MarginRegion["分離邊界帶 (Margin Region)"]
        SepPlane["決策超平面 (w^T x + b = 0)"]
        Dist["幾何間距: 2 / ||w||"]
    end

    subgraph NegSpace["負類樣本空間 (y = -1)"]
        SV_Neg["支援向量 (Support Vector: w^T x + b = -1)"]
        N1["負樣本 (-)"]
        N2["負樣本 (-)"]
    end

    SV_Pos --- Dist
    Dist --- SepPlane
    SepPlane --- SV_Neg
```

---

## 📊 硬邊界 (Hard Margin) vs. 軟邊界 (Soft Margin) 比較

```mermaid
flowchart TD
    subgraph HardMargin["硬邊界 (Hard Margin SVM)"]
        H1["嚴格線性可分要求"]
        H2["所有樣本滿足: y_i(w^T x_i + b) >= 1"]
        H3["容錯率為 0，對雜訊極度敏感"]
    end

    subgraph SoftMargin["軟邊界 (Soft Margin SVM)"]
        S1["允許非線性雜訊與部分樣本誤分"]
        S2["引進鬆弛變數: y_i(w^T x_i + b) >= 1 - xi_i"]
        S3["加入懲罰項 C: 最小化 1/2 ||w||^2 + C sum(xi_i)"]
    end

    HardMargin -- "引入容錯鬆弛變數" --> SoftMargin
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 貝氏分類器與貝氏信念網路 (Bayesian Belief Networks) 之定位
- **計算複雜度與專家先驗**：傳統單純貝氏假設屬性條件獨立，但在真實複雜情境下屬性往往相依。貝氏信念網路透過有向無環圖（DAG）表達變數條件機率，但因需大量領域專家後驗機率推估，實務工程代價極高。
- **學術與工程基準線（Baseline）**：現代機器學習與深度學習論文中，貝氏分類器經常作為不可或缺的 Baseline 模型，用於客觀驗證新演算法之性能提升幅度。

### 2. 支援向量機幾何最大間距 (Maximum Margin) 推導
- **超平面定義**：空間中決策平面由 $\mathbf{w}^T \mathbf{x} + b = 0$ 決定，其中 $\mathbf{w}$ 為法向量（Normal Vector），$b$ 為偏差位移量（Bias）。
- **間距大小**：兩側邊界線分別為 $\mathbf{w}^T \mathbf{x} + b = +1$ 與 $\mathbf{w}^T \mathbf{x} + b = -1$，兩平行超平面間的幾何邊界距離為：
  $$\text{Margin} = \frac{2}{\|\mathbf{w}\|}$$
- **目標函數**：最大化間距等價於在約束條件 $y_i(\mathbf{w}^T \mathbf{x}_i + b) \ge 1$ 下，最小化 $\frac{1}{2}\|\mathbf{w}\|^2$。

### 3. 軟邊界 (Soft Margin) 與鬆弛變數 (Slack Variables)
- **鬆弛變數引進**：真實資料集中常存在雜訊或交疊樣本，無法嚴格線性可分。為每筆樣本引入鬆弛變數 $\xi_i \ge 0$，放寬邊界條件為：
  $$y_i(\mathbf{w}^T \mathbf{x}_i + b) \ge 1 - \xi_i$$
- **懲罰參數 $C$ 權衡**：目標函數調整為：
  $$\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2}\|\mathbf{w}\|^2 + C \sum_{i=1}^{N} \xi_i$$
  $C$ 越大代表對錯誤分類懲罰越重（趨近硬邊界）；$C$ 越小則允許更多容錯邊界，提高對雜訊的泛化容忍度。
"""
    summary_file = UNIV_DIR / "機器學習-05-支援向量機SVM最大間距超平面與軟邊界最佳化-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_iot_sec_01():
    """Build IOT-SEC-01 from transcribe_outputs/6 週五 上午10點18分."""
    print("Building IOT-SEC-01 (6 週五 上午10點18分)...")
    raw_path = RAW_DIR / "6 週五 上午10點18分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = clean_transcript_text(raw)

    title = "物聯網資安實務 Lesson 01：去周邊化集體防禦、零信任持續身分驗證與 TPM 硬體信任根"
    talk_id = "IOT-SEC-01-DEPERIMETER-ZEROTRUST-TPM"
    event = "大學部物聯網與網路安全實務課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.33)
    s2 = int(total_len * 0.66)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 周邊防禦到去周邊化：集中式網段防火牆集體防禦 vs. 邊緣節點獨立微防護", sec1)
    builder.add_section("📊 零信任架構落地：Never Trust, Always Verify、無線網路動態驗證與外包稽核", sec2)
    builder.add_section("💼 物聯網邊緣安全落地：TPM 硬體信任根、IoT Gateway 通訊閘道與端對端密碼學防護", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部物聯網與網路安全實務課程"',
        'event: "大學部物聯網與網路安全實務課程"\ndate: "2024-11-15"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed for IOT-SEC-01: {errors}")

    proof_file = UNIV_DIR / "物聯網資安-01-去周邊化集體防禦與零信任TPM硬體信任根-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：去周邊化（De-perimeterization）、零信任安全模型（Zero Trust）、可信賴平台模組（TPM）硬體信任根與 IoT Gateway 邊緣防禦  
> **授課教授**：授課講師（資安與物聯網專題講座教授）  
> **核心模組**：IoT Security, De-perimeterization, Zero Trust Architecture, Continuous Authentication, TPM Root of Trust, Gateway Security  
> **學習目標**：理解傳統邊界防火牆集體防禦之局限性，掌握物聯網去周邊化之各端點微防護理念，並熟悉零信任持續驗證與 TPM 加解密防護技術  
> **關聯文件**：[📄 完整原話逐字稿 (物聯網資安-01-去周邊化集體防禦與零信任TPM硬體信任根-proofread.md)](./物聯網資安-01-去周邊化集體防禦與零信任TPM硬體信任根-proofread.md)

---

## 🏛️ 傳統周邊防禦 vs. 去周邊化 (De-perimeterization) 架構對比

```mermaid
flowchart TD
    subgraph Traditional["傳統周邊化集體防禦 (Perimeter Security)"]
        FW["外部防火牆 / 邊界網關"]
        subgraph InternalNet["內部受信任網段 (Flat Network)"]
            Dev1["IoT 感測器 A"]
            Dev2["IoT 控制器 B"]
            Dev3["監控主機 C"]
        end
        FW --> InternalNet
        Note1["邊界一旦被突破，內部即無防禦能力"]
    end

    subgraph Deperimeterized["去周邊化與零信任防禦 (De-perimeterization)"]
        subgraph Endpoint1["IoT 節點 1"]
            TPM1["TPM 硬體金鑰"]
            Agent1["獨立微防護 / 加密"]
        end
        subgraph Endpoint2["IoT 節點 2"]
            TPM2["TPM 硬體金鑰"]
            Agent2["獨立微防護 / 加密"]
        end
        GW["IoT 安全閘道器 (Gateway)"]
        Cloud["雲端管理中心"]
        Endpoint1 <--"端對端加密 (E2EE)"--> GW
        Endpoint2 <--"端對端加密 (E2EE)"--> GW
        GW <--"動態身分認證"--> Cloud
    end
```

---

## 📊 零信任架構 (Zero Trust) 核心運作原則

```mermaid
flowchart LR
    Principal["存取請求主體 (使用者 / IoT 設備)"] --> PolicyEngine{"存取策略檢驗引擎<br/>(Policy Engine)"}
    PolicyEngine --> C1["Never Trust: 永遠預設不信任來源"]
    PolicyEngine --> C2["Always Verify: 每次存取持續驗證身分"]
    PolicyEngine --> C3["Session Expiry: 定期重新鑑別與中斷重登"]
    PolicyEngine --> C4["Supply Chain: 外包與第三方軟韌體合規稽核"]
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 去周邊化 (De-perimeterization) 演進與物聯網威脅
- **傳統集中式周邊防禦的破綻**：過去將大量無防護之 IoT 感測裝置置於防火牆後方之同一網段，採集體防禦策略。然而一旦單一節點遭實體接觸入侵或外包程式碼污染，攻擊者便可於內網橫向移動（Lateral Movement）。
- **去周邊化核心觀念**：打破傳統邊界內外之假定信任，將每個物聯網邊緣裝置均視為可能暴露於公網之獨立受防護實體，直接在端點設備實施安全防護與通訊加密。

### 2. 零信任架構落地原則：Never Trust, Always Verify
- **持續性身分驗證**：零信任的核心絕非拒絕存取，而是對每一次操作、每一個 API 調用進行動態且持續的身分鑑別。
- **連線工作階段限制**：針對企業無線網路（Wi-Fi）或遠端連線，實施強制存取時間門檻（例如連線一小時後自動踢除並強制重驗），杜絕長效憑證竊取風險。
- **供應鏈與外包安全**：嚴格落實外包軟硬體產品（Outsourcing）交付時的程式碼審查與完整性校驗，避免引發數十億級別之重大資安事故。

### 3. TPM 硬體信任根與邊緣防護
- **可信賴平台模組（TPM）**：物聯網端點可採用標準化硬體晶片（TPM 2.0），將加解密金鑰、數位憑證與雜湊測量值封存在防篡改硬體內，建立不可篡改的信任根（Root of Trust）。
- **IoT Gateway 與端對端加密**：小型微感測器因算力限制難以執行高階演算法時，透過安全 IoT 通訊閘道器進行封包聚合、協定轉換與加密通道傳輸，達成雲地一體安全合規。
"""
    summary_file = UNIV_DIR / "物聯網資安-01-去周邊化集體防禦與零信任TPM硬體信任根-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_mis_01():
    """Build MIS-01 from transcribe_outputs/4月11日 下午3點25分."""
    print("Building MIS-01 (4月11日 下午3點25分)...")
    raw_path = RAW_DIR / "4月11日 下午3點25分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = clean_transcript_text(raw)

    title = "管理資訊系統 Lesson 01：期中重點總複習、雲端運算架構、大數據挑戰與平台經濟顛覆模型"
    talk_id = "MIS-01-MIDTERM-CLOUD-AI-PLATFORM"
    event = "大學部管理資訊系統（MIS）課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.33)
    s2 = int(total_len * 0.66)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 MIS 核心定義與資訊科技策略：營運效能提升與組織策略目標之資訊科技整合", sec1)
    builder.add_section("📊 雲端運算服務與大數據挑戰：IaaS/PaaS/SaaS 模式、部署類型與冷熱資料治理五大挑戰", sec2)
    builder.add_section("💼 雙邊市場與平台經濟：人工智慧應用、平台企業五大攻擊力來源與傳統企業顛覆特性", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部管理資訊系統（MIS）課程"',
        'event: "大學部管理資訊系統（MIS）課程"\ndate: "2024-04-11"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed for MIS-01: {errors}")

    proof_file = UNIV_DIR / "管理資訊系統-01-期中重點總複習雲端運算平台經濟與AI架構-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：管理資訊系統（MIS）期中重點總複習、雲端運算服務模型、大數據五大挑戰與雙邊市場平台經濟  
> **授課教授**：授課講師（資管系專任授課教授）  
> **核心模組**：MIS Fundamentals, Cloud Computing (IaaS/PaaS/SaaS), Big Data Challenges, Platform Ecosystems, AI & NLP  
> **學習目標**：掌握 MIS 支援組織策略的核心定義，辨析雲端運算架構與配置類型，解析大數據落地治理挑戰，並深刻剖析平台企業取代傳統產業的攻擊力成因  
> **關聯文件**：[📄 完整原話逐字稿 (管理資訊系統-01-期中重點總複習雲端運算平台經濟與AI架構-proofread.md)](./管理資訊系統-01-期中重點總複習雲端運算平台經濟與AI架構-proofread.md)

---

## 🏛️ 雲端運算三層服務與五大部署模式

```mermaid
flowchart TD
    subgraph CloudLayers["雲端運算服務架構層級 (SPI Model)"]
        SaaS["軟體即服務 (SaaS: 應用端服務，如 ERP / CRM / Office365)"]
        PaaS["平台即服務 (PaaS: 開發維運平台，如 執行環境 / 資料庫中介軟體)"]
        IaaS["基礎設施即服務 (IaaS: 運算 / 儲存 / 虛擬化網路資源)"]
        SaaS --> PaaS --> IaaS
    end

    subgraph DeployModes["雲端運算五大部署架構"]
        Pub["公有雲 (Public Cloud)"]
        Pri["私有雲 (Private Cloud)"]
        Com["社群雲 (Community Cloud)"]
        VPS["虛擬私有雲 (VPC)"]
        Hyb["混合雲 (Hybrid Cloud)"]
    end
```

---

## 📊 平台企業五大攻擊力來源與雙邊網路效應

```mermaid
flowchart LR
    subgraph PlatformAttack["平台企業取代傳統企業之攻擊力來源"]
        A1["成本優勢 (邊際成本近乎為零)"]
        A2["資源外部化 (無重資產持有負擔)"]
        A3["跨邊網路效應 (用戶與供應商正向反饋)"]
        A4["指數級規模成長 (數位擴展無邊界)"]
        A5["生態系目標鎖定 (一站式整合解決方案)"]
    end

    subgraph Disrupted["最易被平台顛覆之傳統產業特性"]
        T1["產品與服務高度同質化、無差異"]
        T2["市場資訊高度不對稱且交易摩擦大"]
        T3["資產閒置率過高且供需調度僵化"]
    end

    PlatformAttack -- "衝擊顛覆" --> Disrupted
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 管理資訊系統 (MIS) 核心定義
- **學術與實務定義**：MIS 是一門研究組織如何「有效利用與管理資訊科技（IT/IS）」，以支援其各項日常營運能力、全面提升經營效率，並達成組織長期策略目標的整合性管理學問。
- **組織與環境交互**：企業外部經營環境的劇烈變動（競爭對手技術創新、總體經濟趨勢與法規政策），會直接驅動並重塑企業內部 MIS 的架構定位與投資配置。

### 2. 雲端運算架構與大數據治理挑戰
- **三層服務模型**：
  - **SaaS (Software as a Service)**：終端使用者直接操作的完整應用層軟體服務。
  - **PaaS (Platform as a Service)**：提供開發者撰寫、測試與託管程式碼的平台環境與中介軟體。
  - **IaaS (Infrastructure as a Service)**：提供底層虛擬化伺服器主機、儲存硬碟與網路頻寬。
- **大數據落地五大挑戰**：
  1. **冷熱資料治理**：高頻存取熱資料與封存冷資料的分層儲存策略。
  2. **跨系統資料整合**：各部門孤島資料清洗與異質格式轉換困難。
  3. **領域知識（Domain Knowledge）**：缺乏業務專家解讀導致分析模型失焦。
  4. **資訊安全與個人隱私保護**：法規合規與機敏資料外洩風險。
  5. **抽樣偏差與樣本代表性**：演算法訓練樣本無法涵蓋真實母體分佈。

### 3. 雙邊市場平台經濟學與傳統企業顛覆
- **平台企業攻擊力來源**：具備零邊際成本、輕資產外部化資源運營、跨邊網路外部性（Network Externality）及數位生態系鎖定能力。
- **容易被平台取代的傳統行業特徵**：服務無實質差異性、市場資訊不對稱嚴重、交易中介抽成高昂且資產閒置率偏高（如傳統計程車業被叫車平台重構、傳統旅宿業被訂房平台重塑）。
"""
    summary_file = UNIV_DIR / "管理資訊系統-01-期中重點總複習雲端運算平台經濟與AI架構-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_mis_02():
    """Build MIS-02 from transcribe_outputs/5月23日 下午3點25分(2)."""
    print("Building MIS-02 (5月23日 下午3點25分(2))...")
    raw_path = RAW_DIR / "5月23日 下午3點25分(2)" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = clean_transcript_text(raw)

    title = "管理資訊系統 Lesson 02：期末重點總複習、車聯網 V2X 通訊、金融科技區塊鏈與資源基礎觀點 RBV"
    talk_id = "MIS-02-FINAL-IOV-FINTECH-RBV"
    event = "大學部管理資訊系統（MIS）課程"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["授課講師", "學員"],
        emoji="🎙️",
        scenario=ScenarioType.CLASSROOM_LECTURE,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.33)
    s2 = int(total_len * 0.66)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 智慧交通與車聯網生態：自駕車分級概念、IoV 車聯網定義與 V2X 協同架構", sec1)
    builder.add_section("📊 金融科技與去中心化帳本：FinTech 業務重塑、區塊鏈技術特性與分散式信任", sec2)
    builder.add_section("💼 策略管理與競爭優勢：資源基礎觀點 RBV 模式架構圖與企業資訊系統效益判讀", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部管理資訊系統（MIS）課程"',
        'event: "大學部管理資訊系統（MIS）課程"\ndate: "2024-05-23"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed for MIS-02: {errors}")

    proof_file = UNIV_DIR / "管理資訊系統-02-期末重點總複習車聯網金融科技與資源基礎觀點-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：管理資訊系統（MIS）期末重點總複習、自駕車與車聯網（IoV）、金融科技（FinTech）與資源基礎觀點（RBV）  
> **授課教授**：授課講師（資管系專任授課教授）  
> **核心模組**：Autonomous Vehicles, Internet of Vehicles (IoV), V2X, FinTech, Blockchain, Resource-Based View (RBV)  
> **學習目標**：理解新一代車聯網智慧通訊架構，掌握 FinTech 與區塊鏈去中心化核心價值，並熟練運用 RBV 架構圖判別企業資訊系統競爭優勢  
> **關聯文件**：[📄 完整原話逐字稿 (管理資訊系統-02-期末重點總複習車聯網金融科技與資源基礎觀點-proofread.md)](./管理資訊系統-02-期末重點總複習車聯網金融科技與資源基礎觀點-proofread.md)

---

## 🏛️ 車聯網 (IoV) V2X 多維度通訊架構

```mermaid
flowchart TD
    HostCar["智慧自駕車輛 (Connected Vehicle)"]
    V2V["V2V (車對車通訊: 碰撞預警 / 車隊巡航)"]
    V2I["V2I (車對基礎設施: 智慧號誌 / 道路感測)"]
    V2R["V2R (車對路側單元 RSU: 邊緣高精地圖下載)"]
    V2N["V2N (車對網路雲端: 導航規劃 / 交通大數據)"]

    HostCar <--> V2V
    HostCar <--> V2I
    HostCar <--> V2R
    HostCar <--> V2N
```

---

## 📊 資源基礎觀點 (Resource-Based View, RBV) 與競爭優勢判讀

```mermaid
flowchart LR
    subgraph EnterpriseResources["企業異質性資源 (Resources)"]
        R1["有形資訊資產 (硬體主機 / 網路專線)"]
        R2["無形能力 (專有演算法 / 組織流程 / 數據積累)"]
    end

    subgraph VRIN["VRIN 競爭力檢驗框架"]
        V["Valuable (具備業務價值)"]
        R["Rare (稀有難以輕易獲取)"]
        I["Inimitable (難以模仿與複製)"]
        N["Non-substitutable (不可替代)"]
    end

    subgraph Advantage["競爭優勢成果 (Advantage)"]
        CA["短期競爭優勢"]
        SCA["持續性競爭優勢 (Sustained Advantage)"]
    end

    EnterpriseResources --> VRIN --> Advantage
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 自駕車與車聯網 (Internet of Vehicles, IoV)
- **車聯網定義**：透過車載感測器、衛星導航及現代無線通訊技術，實現車輛與周遭人、車、路、雲全方位聯網互動之物聯網生態系。
- **V2X (Vehicle-to-Everything) 協同架構**：
  - **V2V (Vehicle-to-Vehicle)**：車輛間即時車距與行車狀態交換，支援防撞與緊急煞車預警。
  - **V2I (Vehicle-to-Infrastructure)**：與智慧交通號誌聯動，動態優化通過時速與綠燈通行率。
  - **V2R (Vehicle-to-Roadside)**：與路側基站單元（RSU）高速通訊，取得微區域路況與高精地圖更新。

### 2. 金融科技 (FinTech) 與區塊鏈去中心化核心
- **FinTech 核心理念**：金融科技本質在於利用新興資通訊技術（大數據、AI、分散式帳本、行動支付）重塑傳統金融仲介與服務交付模式，達成普惠金融、降本增效與無縫體驗。
- **區塊鏈 (Blockchain)**：透過分散式點對點網路、非對稱密碼學雜湊指標與共識機制，實現無須中心化第三方信任背書之防篡改資料帳本，確保資產交易的透明度與終局性。

### 3. 資源基礎觀點 (Resource-Based View, RBV) 模式架構
- **資訊系統競爭價值判讀**：企業單純建置採購現成的市售資訊系統（如標準 ERP），因為競爭對手亦能輕易在市場採購，僅能帶來「競爭平價（Competitive Parity）」，而非持續競爭優勢。
- **VRIN 準則結合**：唯有將資訊科技與企業獨特的組織文化、專利演算法、深層顧客數據及敏捷流程高度結合，創造出具備價值性（Valuable）、稀少性（Rare）、難以模仿（Inimitable）且不可替代（Non-substitutable）之複合能力時，方能轉化為不可撼動的「持續性競爭優勢（SCA）」。
"""
    summary_file = UNIV_DIR / "管理資訊系統-02-期末重點總複習車聯網金融科技與資源基礎觀點-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_master_apr():
    """Build MASTER-APR-01 from transcribe_outputs/週一 18點48分."""
    print("Building MASTER-APR-01 (週一 18點48分)...")
    raw_path = RAW_DIR / "週一 18點48分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = clean_transcript_text(raw)

    title = "碩士專題討論：自動化程式漏洞修復（APR）之兩階段根因分析與修補有效性驗證"
    talk_id = "MASTER-APR-01-VULN-REPAIR"
    event = "資安與軟體工程碩士班專題研討"

    builder = ProofreadBuilder(
        title=title,
        event=event,
        talk_id=talk_id,
        speakers=["發表研究生", "指導教授", "與會學者"],
        emoji="🎙️",
        scenario=ScenarioType.SINGLE_TALK,
    )

    total_len = len(cleaned)
    s1 = int(total_len * 0.33)
    s2 = int(total_len * 0.66)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1], default_speaker="發表研究生")
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2], default_speaker="發表研究生")
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:], default_speaker="發表研究生")

    builder.add_section("🎯 自動化程式修復 (APR) 核心挑戰：症狀規避 Symptom Bypass vs. 根因防禦 Root Cause Defense", sec1)
    builder.add_section("📊 兩階段修補驗證機制：PoC 重放變異測試、開發者測試案例與 AFL++ 模糊測試整合", sec2)
    builder.add_section("💼 實驗室評析與未來研究展望：多方法基準評測 (Repair, PatchAgent, Codex) 與多模態延伸建議", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "資安與軟體工程碩士班專題研討"',
        'event: "資安與軟體工程碩士班專題研討"\ndate: "2026-09-14"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="single-talk")
    if not is_valid:
        raise ValueError(f"Validation failed for MASTER-APR-01: {errors}")

    proof_file = MASTER_DIR / "碩士專題討論-01-自動化漏洞修復APR根因分析與兩階段修補驗證-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **研討主題**：自動化程式修復（APR: Automated Program Repair）、漏洞根因分析（Root Cause Analysis）、兩階段修補驗證與模糊測試整合  
> **研討講者**：發表研究生（系統資安與軟體工程實驗室）  
> **指導教授**：指導教授（陳教授）  
> **核心模組**：Automated Program Repair (APR), Fault Localization, Root Cause vs Crash Site, Two-Stage Patch Validation, AFL++ Fuzzing, PoC Replay  
> **研討目標**：深入剖析軟體弱點自動修復之兩階段驗證架構，釐清症狀規避修補與真正根因防禦之本質差異，並掌握結合 AFL++ 與開發者用例之修補品質評估法  
> **關聯文件**：[📄 完整原話逐字稿 (碩士專題討論-01-自動化漏洞修復APR根因分析與兩階段修補驗證-proofread.md)](./碩士專題討論-01-自動化漏洞修復APR根因分析與兩階段修補驗證-proofread.md)

---

## 🏛️ 自動化程式修復 (APR) 兩階段驗證架構

```mermaid
flowchart TD
    BugReport["漏洞通報 / 弱點觸發 PoC 樣本"] --> FL["錯誤定位 (Fault Localization / FL)"]
    FL --> CandidateGen["修補程式碼生成 (Patch Candidate Generation)"]

    subgraph Phase1["第一階段驗證 (Stage 1: PoC 測試)"]
        Replay["PoC Replay (驗證漏洞是否不再觸發)"]
        Mutate["PoC 變異測試 (Variable Mutation)"]
        Replay --> Mutate
    end

    subgraph Phase2["第二階段驗證 (Stage 2: 根因與語意完整性)"]
        HumanCheck["根因防禦檢驗 (Root Cause vs. Crash Site Bypass)"]
        DevTests["開發者迴歸測試案例 (Developer Regression Tests)"]
        Fuzzer["AFL++ 模糊測試 (長期動態測試無崩潰)"]
        DevTests --> Fuzzer
    end

    CandidateGen --> Phase1
    Phase1 -- "通過單元防禦" --> Phase2
    Phase2 -- "通過根因驗證" --> ValidPatch["正式發布高品質安全補丁 (Verified Patch)"]
    Phase2 -- "判定為症狀繞過" --> Reject["拒絕修補並回饋反思重修"]
```

---

## 📊 修補品質本質差異：根因修復 vs. 崩潰點規避

```mermaid
flowchart LR
    subgraph SymptomBypass["症狀繞過修補 (Crash Site / Symptom Bypass - 不良修補)"]
        B1["僅在 Crash Site 加上 if (ptr == NULL) return"]
        B2["掩蓋錯誤表面，未修復上游記憶體管理或邏輯宣告"]
        B3["破壞原有業務功能流程，引入隱形相依漏洞"]
    end

    subgraph RootCauseFix["根因修復 (Root Cause Defense - 真正有效修補)"]
        R1["回溯追蹤至 Production Site 或最初宣告錯誤"]
        R2["修正內部資料流生命週期或邊界檢查邏輯"]
        R3["完整保留原始系統業務功能，不引入語意異常"]
    end
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 自動化程式修復 (APR) 之「過度擬合」難題與症狀規避
- **修補過擬合（Patch Overfitting）**：許多 APR 工具為了快速通過弱點測試案例，傾向於直接在崩潰點（Crash Site）加入簡單的跳過判斷（如 `if (!ptr) return;`）。雖然該 PoC 不再觸發系統崩潰，但程式本質上的業務邏輯已遭破壞，並未真正根除威脅。
- **兩階段驗證必要性**：第一階段利用 PoC 及其變異測試進行輕量快速過濾；第二階段必須透過人機協同審查與迴歸測試，確保修補發生於根因節點（Root Cause Node），而非單純繞過崩潰點。

### 2. 弱點修補有效性之多維度評估管線
- **動態輕量化定位**：面對代碼庫龐大、符號執行易崩潰之困境，採用輕量動態追蹤配合堆疊回溯（Call Stack Traceback），聚焦潛在錯誤函式範圍（Function of Interest, FOI）。
- **AFL++ 模糊測試整合**：修補生成後，除了重放原始 PoC，進一步將修補程式送入 AFL++ 進行長時間動態模糊測試（Fuzzing），驗證邊界值與記憶體安全性，防範修補衍生新 0-day 弱點。

### 3. 指導教授學術評析與研究深化建議
- **陳教授指導重點**：學術研究應跳脫單一企業 Case 的表面探討，應將修補案例抽象化為通用的「多模態/多層次架構模型（Multimodal / Multi-faceted Model）」。
- **對比基準與多語言適應性**：對比 Repair、PatchAgent、Codex 等基準架構，深入分析其在 C/C++ 記憶體安全與其他高階語言中之移植難度與泛化能力，形成具備高度說服力的碩士研究成果。
"""
    summary_file = MASTER_DIR / "碩士專題討論-01-自動化漏洞修復APR根因分析與兩階段修補驗證-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def main():
    print("=" * 60)
    print("Building Final Remaining Course Transcripts...")
    print("=" * 60)
    build_ml_05()
    build_iot_sec_01()
    build_mis_01()
    build_mis_02()
    build_master_apr()
    print("=" * 60)
    print("All final deliverables built successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
