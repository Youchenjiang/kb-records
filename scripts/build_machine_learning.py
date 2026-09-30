#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Machine Learning & Deep Learning course deliverables (ML-01, ML-02, ML-03, ML-04):
- Proofread verbatim transcription with speaker attributions
- Structured summary notes with Mermaid diagrams
"""

from pathlib import Path
import re
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_undergrad_courses import clean_text, segment_into_dialogue_paragraphs
from transcript_processor.structurer import ProofreadBuilder, ScenarioType, validate_transcript_structure

OUT_DIR = REPO_ROOT / "4-University" / "2024-UndergraduateCourses"
OUT_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR = REPO_ROOT / "transcribe_outputs"


def fix_ml_typos(text: str) -> str:
    """Fix common ASR homophone misrecognitions in Machine Learning lectures."""
    replacements = [
        ("底區間去", "決策樹 (Decision Tree)"),
        ("底區間", "決策樹"),
        ("路子裡面", "Root 根節點裡面"),
        ("爭議", "增益 (Information Gain)"),
        ("方選", "函數 (Function)"),
        ("Mann Cole", "Jiawei Han (Data Mining 教材)"),
        ("credit card ready", "Credit Rating (信用評等)"),
        ("Jury Voting", "Majority Voting (多數決投票)"),
        ("PSVT", "PSVT (陣發性心室上心搏過速)"),
        ("main component", "主要元件 (Main Component)"),
        ("hidden layer", "隱藏層 (Hidden Layer)"),
        ("input layer", "輸入層 (Input Layer)"),
        ("output layer", "輸出層 (Output Layer)"),
        ("feature extraction", "特徵萃取 (Feature Extraction)"),
        ("feature layer", "特徵層 (Feature Layer)"),
        ("特徵特徵工程", "特徵工程 (Feature Engineering)"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return clean_text(text)


def build_ml_01():
    print("Building ML-01 (週一 09點08分)...")
    raw_path = RAW_DIR / "週一 09點08分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_ml_typos(raw)

    title = "機器學習實務 Lesson 01：監督式學習分類問題定義、決策樹演算法 ID3 與資訊增益"
    talk_id = "ML-01-DECISION-TREE-ID3"
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

    builder.add_section("🎯 分類問題定義：資料表記錄、特徵屬性與類別標籤 Class Label", sec1)
    builder.add_section("📊 決策樹建構流程：資料切分、資訊熵 Entropy 與資訊增益 Information Gain", sec2)
    builder.add_section("💼 終止條件判定：純度檢驗、多數決投票 Majority Voting 與過擬合防範", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部機器學習與深度學習課程"',
        'event: "大學部機器學習與深度學習課程"\ndate: "2026-03-02"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "機器學習-01-監督式學習分類與決策樹演算法ID3-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：機器學習監督式分類模型、決策樹（Decision Tree）、資訊熵（Entropy）與資訊增益（Information Gain）  
> **授課教授**：授課講師（資訊工程授課教授）  
> **核心模組**：Classification, Decision Tree, Entropy, Information Gain, ID3 Algorithm, Majority Voting  
> **學習目標**：理解監督式學習資料表示法，掌握 ID3 決策樹之節點屬性切分數學原理與停止分裂準則  
> **關聯文件**：[📄 完整原話逐字稿 (機器學習-01-監督式學習分類與決策樹演算法ID3-proofread.md)](./機器學習-01-監督式學習分類與決策樹演算法ID3-proofread.md)

---

## 🏛️ 決策樹 (Decision Tree) 遞迴分裂架構

```mermaid
flowchart TD
    Root["根節點 (Root Node: 全部資料集 D)"]
    AttrSelect{"計算資訊增益 (Information Gain)<br/>挑選最大增益屬性 A"}
    Branch1["子分支 1 (屬性值 = v1)"]
    Branch2["子分支 2 (屬性值 = v2)"]
    Branch3["子分支 3 (屬性值 = v3)"]
    Leaf1["葉節點 (Class: Yes)"]
    Leaf2["葉節點 (Class: No)"]
    StopCheck{"是否達到純度 100%<br/>或無剩餘屬性?"}

    Root --> AttrSelect
    AttrSelect --> Branch1
    AttrSelect --> Branch2
    AttrSelect --> Branch3
    Branch1 --> Leaf1
    Branch2 --> StopCheck
    StopCheck -- "純度達成" --> Leaf2
    StopCheck -- "未達純度但無屬性" --> Vote["多數決投票 (Majority Voting)"]
```

---

## 📊 決策樹建構與資料切分評估指標

```mermaid
flowchart LR
    subgraph Entropy_Box["資訊熵 (Entropy)"]
        E1["度量資料集之混亂度/不純度"]
        E2["數值愈高，代表類別分佈愈均勻混亂"]
    end

    subgraph Gain_Box["資訊增益 (Information Gain)"]
        G1["母節點熵值 - 切分後子節點加權熵值"]
        G2["增益愈大，代表切分後純度提升愈顯著"]
    end

    Entropy_Box --> Gain_Box
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 監督式分類問題的數學定義
- **資料集表徵**：由 $N$ 筆記錄（Records）組成，每筆記錄包含一組特徵屬性向量 $\mathbf{x} = (x_1, x_2, \dots, x_d)$ 與一個已知的類別標籤（Class Label）$y \in \{C_1, C_2, \dots, C_k\}$。
- **目標**：從訓練資料集中學習出映射函數 $f(\mathbf{x}) \to y$，使模型對未見過的測試資料具備準確泛化預測能力。

### 2. 資訊熵 (Entropy) 與資訊增益 (Information Gain) 公式
- **資訊熵（Entropy）**：
  $$Entropy(D) = - \sum_{i=1}^{k} p_i \log_2(p_i)$$
  其中 $p_i$ 為資料集 $D$ 中屬於類別 $C_i$ 之機率樣本比例。若所有樣本均屬同一類別，則 $Entropy(D) = 0$（完全純淨）。
- **資訊增益（Information Gain, ID3 演算法核心）**：
  $$Gain(D, A) = Entropy(D) - \sum_{v \in Values(A)} \frac{|D_v|}{|D|} Entropy(D_v)$$
  ID3 演算法於每個節點遍歷所有可用屬性 $A$，選取能帶來最大 $Gain(D, A)$ 之屬性作為當前切分條件。

### 3. 決策樹遞迴停止條件
- **完全純淨**：當前節點的所有樣本均屬於同一類別標籤，直接生成葉節點（Leaf Node）。
- **屬性耗盡**：所有特徵屬性皆已被切分使用完畢，但樣本類別仍不純。此時採行**多數決投票（Majority Voting）**，將節點標註為出現頻率最高之類別。
- **空子節點**：某個屬性取值在訓練集中無任何對應樣本，將父節點的多數類別賦予該葉節點。
"""
    summary_file = OUT_DIR / "機器學習-01-監督式學習分類與決策樹演算法ID3-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_ml_02():
    print("Building ML-02 (週一 10點23分)...")
    raw_path = RAW_DIR / "週一 10點23分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_ml_typos(raw)

    title = "機器學習實務 Lesson 02：單純貝氏分類器 Naive Bayes 與支援向量機 SVM 原理"
    talk_id = "ML-02-NAIVE-BAYES-SVM"
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
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 決策樹切分機制複習與連續型屬性處理策略", sec1)
    builder.add_section("📊 單純貝氏分類器：貝氏定理、先驗機率與條件機率獨立性假設", sec2)
    builder.add_section("💼 最大後驗機率 MAP 推論與支援向量機 SVM 最大超平面概念", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部機器學習與深度學習課程"',
        'event: "大學部機器學習與深度學習課程"\ndate: "2026-03-02"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "機器學習-02-貝氏分類器與支援向量機SVM原理-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：貝氏定理、單純貝氏分類器（Naive Bayes Classifier）、最大後驗機率（MAP）與 SVM 最大邊界超平面  
> **授課教授**：授課講師（資訊工程授課教授）  
> **核心模組**：Bayes Theorem, Prior & Posterior Probability, Likelihood, Naive Bayes, Conditional Independence, SVM  
> **學習目標**：精熟貝氏機率模型推論架構，理解特徵條件獨立性簡化假設，並建立支援向量機最大間距（Margin）之幾何概念  
> **關聯文件**：[📄 完整原話逐字稿 (機器學習-02-貝氏分類器與支援向量機SVM原理-proofread.md)](./機器學習-02-貝氏分類器與支援向量機SVM原理-proofread.md)

---

## 🏛️ 貝氏定理機率推論架構 (Bayesian Inference)

```mermaid
flowchart TD
    Prior["先驗機率 P(H)<br/>無任何特徵觀察時，假設 H 發生的初始機率"]
    Likelihood["概似度 P(X|H)<br/>若假設 H 成立，觀察到特徵向量 X 的條件機率"]
    Evidence["邊際機率 P(X)<br/>所有假設下觀察到 X 的總機率 (正規化常數)"]
    Posterior["後驗機率 P(H|X)<br/>給定觀察特徵 X 後，假設 H 成立的更新機率"]

    Prior --> Posterior
    Likelihood --> Posterior
    Evidence --> Posterior
```

---

## ⚖️ 支援向量機 (SVM) 最大邊界超平面 (Maximum Margin Hyperplane)

```mermaid
flowchart LR
    subgraph DataSpace["二維/高維特徵空間"]
        PosClass["正樣本點 (+1)"]
        NegClass["負樣本點 (-1)"]
        Hyperplane["決策超平面: w^T x + b = 0"]
        MarginPos["邊界線: w^T x + b = +1"]
        MarginNeg["邊界線: w^T x + b = -1"]
        SV["支援向量 (Support Vectors: 壓在邊界上的關鍵樣本)"]
    end

    PosClass --> MarginPos
    NegClass --> MarginNeg
    MarginPos <--> Hyperplane
    Hyperplane <--> MarginNeg
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 貝氏定理數學推導與組成成分
- **基本公式**：
  $$P(H|X) = \frac{P(X|H) P(H)}{P(X)}$$
  - **後驗機率 $P(H|X)$**：在已知特徵樣本 $X$ 發生的條件下，假設 $H$ 成立的機率。
  - **先驗機率 $P(H)$**：領域知識或訓練集中假設 $H$ 出現的基礎頻率。
  - **概似度（Likelihood）$P(X|H)$**：假設 $H$ 為真時，產生特徵樣本 $X$ 的機率。
  - **證據（Evidence）$P(X)$**：$\sum_{h} P(X|h)P(h)$，作為常數正規化因子。

### 2. 單純貝氏分類器 (Naive Bayes) 的關鍵假設
- **條件獨立性假設（Conditional Independence Assumption）**：
  假設給定類別標籤 $C$ 後，各個特徵屬性 $x_1, x_2, \dots, x_d$ 相互獨立：
  $$P(X|C) = P(x_1, x_2, \dots, x_d | C) = \prod_{i=1}^{d} P(x_i | C)$$
- **最大後驗機率分類決策（MAP Decision Rule）**：
  $$\hat{y} = \arg\max_{c \in \mathcal{C}} P(C=c) \prod_{i=1}^{d} P(x_i | C=c)$$
  此假設大幅降低了計算複雜度，避免了維度災難（Curse of Dimensionality）。

### 3. 支援向量機 (SVM) 核心理念
- **最大間距超平面（Maximum Margin Hyperplane）**：在所有可完全分開正負樣本的超平面中，尋找使得支援向量（Support Vectors）與超平面距離最大化的最佳決策邊界。
- **強韌性**：僅由少數壓在邊界上的支援向量決定分類超平面，對遠離邊界的雜訊資料具備高度容錯性。
"""
    summary_file = OUT_DIR / "機器學習-02-貝氏分類器與支援向量機SVM原理-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_ml_03():
    print("Building ML-03 (週一 10點12分)...")
    raw_path = RAW_DIR / "週一 10點12分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_ml_typos(raw)

    title = "機器學習實務 Lesson 03：深度學習導論、多層感知機 MLP 與神經網路架構設計"
    talk_id = "ML-03-DEEP-LEARNING-MLP"
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
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 深度學習演進史：從傳統特徵工程邁向端到端表示學習", sec1)
    builder.add_section("📊 生物神經元與人工類神經網路：電位傳導、激勵函數與醫學訊號診斷案例", sec2)
    builder.add_section("💼 多層架構設計：隱藏層節點數決定準則、GPU 平行運算與經驗法則", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部機器學習與深度學習課程"',
        'event: "大學部機器學習與深度學習課程"\ndate: "2026-03-09"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "機器學習-03-深度學習導論與多層感知機類神經網路-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：深度學習（Deep Learning）、多層感知機（MLP）、人工神經網路拓撲結構與 GPU 平行運算  
> **授課教授**：授課講師（資訊工程授課教授）  
> **核心模組**：Deep Learning, Artificial Neural Networks, MLP, Hidden Layers, GPU Parallel Computing, Medical AI  
> **學習目標**：理解人工類神經網路如何模擬生物電位訊號傳導，掌握輸入層、隱藏層與輸出層之架構設計與算力需求  
> **關聯文件**：[📄 完整原話逐字稿 (機器學習-03-深度學習導論與多層感知機類神經網路-proofread.md)](./機器學習-03-深度學習導論與多層感知機類神經網路-proofread.md)

---

## 🏛️ 多層感知機 (Multi-Layer Perceptron, MLP) 拓撲架構

```mermaid
flowchart LR
    subgraph InputLayer["輸入層 (Input Layer)"]
        x1["特徵 x1"]
        x2["特徵 x2"]
        xd["特徵 xd"]
    end

    subgraph HiddenLayer1["隱藏層 1 (Feature Extraction)"]
        h11["神經元 h1,1"]
        h12["神經元 h1,2"]
        h1m["神經元 h1,m"]
    end

    subgraph HiddenLayer2["隱藏層 2 (High-Level Representation)"]
        h21["神經元 h2,1"]
        h22["神經元 h2,2"]
    end

    subgraph OutputLayer["輸出層 (Output Layer)"]
        y1["預測輸出 y (Softmax / Sigmoid)"]
    end

    InputLayer --> HiddenLayer1
    HiddenLayer1 --> HiddenLayer2
    HiddenLayer2 --> OutputLayer
```

---

## ⚡ 傳統機器學習 vs. 深度學習之特徵工程演進

```mermaid
flowchart TD
    subgraph Traditional["傳統機器學習 (Traditional ML)"]
        Data1["原始資料 (Raw Data)"] --> FE["人工特徵工程 (Manual Feature Engineering)"]
        FE --> Model1["淺層分類器 (SVM / Decision Tree)"]
        Model1 --> Output1["分類結果"]
    end

    subgraph Deep["端到端深度學習 (Deep Learning)"]
        Data2["原始資料 (Raw Data)"] --> DeepNN["深層類神經網路 (端到端階層式自動萃取)"]
        DeepNN --> Output2["分類結果"]
    end
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 生物神經元至人工神經元之數學抽象
- **突觸權重與偏壓**：神經元接收前一層訊號 $x_i$，與權重 $w_i$ 相乘並加上偏壓 $b$：
  $$z = \sum_{i=1}^{d} w_i x_i + b = \mathbf{w}^T \mathbf{x} + b$$
- **激勵函數（Activation Function）**：引入非線性變換 $\sigma(z)$（如 ReLU、Sigmoid、Tanh），打破線性組合之侷限，賦予網路逼近任意複雜非線性函數的能力（萬能逼近定理 Universal Approximation Theorem）。

### 2. 隱藏層（Hidden Layers）層數與節點數設計原則
- **特徵抽象階層化**：淺層神經元負責捕捉低階局部特徵（如影像邊緣、訊號頻率脈衝）；深層神經元組合低階特徵以形成高階語義概念。
- **超參數經驗法則**：層數過少可能導致欠擬合（Underfitting）；層數過深且節點過多則易引發過擬合（Overfitting）與梯度消失（Vanishing Gradient），需仰賴經驗法則配合交叉驗證決定。

### 3. GPU 平行加速對於深度學習之關鍵推動
- **矩陣乘法並行性**：類神經網路前向傳遞與反向傳播本質上為高維矩陣乘法運算，GPU 具備成千上萬個核心，可提供極高吞吐量的平行運算能力，將數十小時的訓練時間縮短至數十分鐘。
"""
    summary_file = OUT_DIR / "機器學習-03-深度學習導論與多層感知機類神經網路-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


def build_ml_04():
    print("Building ML-04 (週一 11點05分)...")
    raw_path = RAW_DIR / "週一 11點05分" / "transcript_zh_tw.txt"
    raw = raw_path.read_text(encoding="utf-8")
    cleaned = fix_ml_typos(raw)

    title = "機器學習實務 Lesson 04：特徵萃取、損失函數與梯度下降法模型最佳化"
    talk_id = "ML-04-LOSS-GRADIENT-DESCENT"
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
    s1 = int(total_len * 0.35)
    s2 = int(total_len * 0.70)

    sec1 = segment_into_dialogue_paragraphs(cleaned[:s1])
    sec2 = segment_into_dialogue_paragraphs(cleaned[s1:s2])
    sec3 = segment_into_dialogue_paragraphs(cleaned[s2:])

    builder.add_section("🎯 深度網路之特徵萃取：各層特徵表示與隱藏層內部映射", sec1)
    builder.add_section("📊 損失函數 Loss Function 定義與非線性最佳化求解目標", sec2)
    builder.add_section("💼 梯度下降法 Gradient Descent：學習率設定、收斂方向與課堂點名總結", sec3)

    rendered = builder.render()
    rendered = rendered.replace(
        'event: "大學部機器學習與深度學習課程"',
        'event: "大學部機器學習與深度學習課程"\ndate: "2026-03-09"'
    )

    is_valid, errors = validate_transcript_structure(rendered, scenario="classroom-lecture")
    if not is_valid:
        raise ValueError(f"Validation failed: {errors}")

    proof_file = OUT_DIR / "機器學習-04-特徵萃取與梯度下降損失函數最佳化-proofread.md"
    proof_file.write_text(rendered, encoding="utf-8")
    print(f"  [OK] Saved {proof_file.name}")

    summary_content = f"# 🛡️ {talk_id} {title}\n\n" + """
> **課程主題**：特徵萃取機制、損失函數（Loss Function）、最佳化求解與梯度下降演算法（Gradient Descent）  
> **授課教授**：授課講師（資訊工程授課教授）  
> **核心模組**：Feature Representation, Loss Function, Convex Optimization, Gradient Descent, Learning Rate  
> **學習目標**：掌握損失函數度量預測誤差之機制，精熟梯度下降法沿著斜率反方向更新權重 $W$ 尋找全域/局部最佳解  
> **關聯文件**：[📄 完整原話逐字稿 (機器學習-04-特徵萃取與梯度下降損失函數最佳化-proofread.md)](./機器學習-04-特徵萃取與梯度下降損失函數最佳化-proofread.md)

---

## 🏛️ 損失函數曲面與梯度下降最佳化迭代流程

```mermaid
flowchart TD
    InitW["隨機初始化模型權重 W (Initial Weights)"]
    Forward["前向傳遞 (Forward Pass)<br/>計算模型預測輸出 y_hat"]
    ComputeLoss["計算損失函數 L(W)<br/>(度量 y_hat 與真實標籤 y 之落差)"]
    ComputeGrad["計算損失函數對權重之梯度<br/>nabla_W L(W)"]
    CheckConv{"是否達到收斂條件<br/>或達到最大代數 (Epochs)?"}
    UpdateW["沿負梯度方向更新權重<br/>W <- W - eta * nabla_W L(W)"]
    FinalModel["完成訓練：產出最佳權重 W*"]

    InitW --> Forward
    Forward --> ComputeLoss
    ComputeLoss --> ComputeGrad
    ComputeGrad --> CheckConv
    CheckConv -- "未收斂" --> UpdateW
    UpdateW --> Forward
    CheckConv -- "已收斂" --> FinalModel
```

---

## 📉 學習率 (Learning Rate, eta) 大小之收斂特性比較

```mermaid
flowchart LR
    subgraph SmallEta["學習率過小 (Too Small)"]
        S1["收斂速度極其緩慢"]
        S2["耗費大量運算資源"]
        S3["易陷入局部極小點或鞍點"]
    end

    subgraph OptimalEta["學習率適中 (Optimal)"]
        O1["平滑穩定下降"]
        O2["高效收斂至最佳解 W*"]
    end

    subgraph LargeEta["學習率過大 (Too Large)"]
        L1["在谷底兩側劇烈震盪"]
        L2["數值發散 (Overshooting / Exploding)"]
    end
```

---

## 🎯 核心重點整理 (Key Takeaways)

### 1. 損失函數 (Loss Function) 的核心職責
- **度量差距**：損失函數 $L(W)$ 衡量神經網路當前預測結果 $\hat{y}$ 與真實世界地面真相（Ground Truth）$y$ 之間的誤差。
- **常見型式**：
  - **均方誤差（Mean Squared Error, MSE）**（用於迴歸）：
    $$L_{MSE}(W) = \frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2$$
  - **交叉熵損失（Cross-Entropy Loss）**（用於多類別分類）：
    $$L_{CE}(W) = - \sum_{i=1}^{N} \sum_{c=1}^{K} y_{i,c} \log(\hat{y}_{i,c})$$

### 2. 梯度下降演算法更新規則
- **核心更新公式**：
  $$W^{(t+1)} = W^{(t)} - \eta \nabla_W L(W^{(t)})$$
  其中 $\nabla_W L(W) = \frac{\partial L}{\partial W}$ 為損失函數的一階偏導數（斜率向量），$\eta > 0$ 為學習率（Learning Rate）。
- **物理意涵**：負梯度方向為函數值局部下降最快的方向。模型沿著負梯度方向一步步滾落至誤差曲面的低谷。

### 3. 特徵萃取（Feature Extraction）的深層轉換本質
- 隱藏層的實質任務是將原本在低維或非線性不可分的原始資料空間，經過逐層非線性映射，變換至高維度特徵空間，使得最終的輸出層能夠以最簡單的線性超平面將資料完美分類。
"""
    summary_file = OUT_DIR / "機器學習-04-特徵萃取與梯度下降損失函數最佳化-summary.md"
    summary_file.write_text(summary_content, encoding="utf-8")
    print(f"  [OK] Saved {summary_file.name}")


if __name__ == "__main__":
    build_ml_01()
    build_ml_02()
    build_ml_03()
    build_ml_04()
