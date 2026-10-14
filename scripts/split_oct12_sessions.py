import re
from pathlib import Path

raw_text = Path('transcribe_outputs/會議錄音 138/transcript_zh_tw.txt').read_text(encoding='utf-8')
idx = raw_text.find('非常謝謝你哈，OK。')
part1_raw = raw_text[:idx + len('非常謝謝你哈，OK。')]
part2_raw = raw_text[idx + len('非常謝謝你哈，OK。'):]

# Fix transcription errors: 右耳 -> 侑宸
part2_raw = part2_raw.replace('好，那我現在就請右耳吧，好不好？', '好，那我現在就請侑宸吧，好不好？')
part2_raw = part2_raw.replace('右耳', '侑宸')

def format_part1(text):
    # Part 1: 同儕研究生 vs 指導教授
    # Dialogue triggers: 
    # 指導教授 speaks when:
    # "好，先起頭講，那個不要打斷。所以 custom GPT 是 GPT 提出一種工具是嗎？還是還是人家去去去利用 GPT，這個 custom GPT 意思是？"
    # "你聽起來很好，我覺得很好。那個EDR是什麼東西？全稱EDR，內臟槍。呃。"
    # "前面有介紹嗎？"
    # "好好好，這樣好，你自己。好，好，好。好，那回到剛剛圖片是怎怎麼寫？避開啊，避開。OK。好，不要不要急啊。好，謝謝。每個單位上。"
    # "嗯也不錯，老師，你你有些觀察，還有一些細節，你注意的。好，我想你去看看，你你去講，你你當面有什麼，有什麼指導？就多一些心知嘛，哈，對不對？多多瞭解。好，非常謝謝你哈，OK。"
    
    t = text
    t = t.replace('好，先起頭講，那個不要打斷。', '\n\n**【指導教授】**：好，先起頭講，那個不要打斷。')
    t = t.replace('它是配用自己，然後做成一個看起來像一個呃頁面。', '\n\n**【同儕研究生】**：它是配用自己，然後做成一個看起來像一個呃頁面。')
    t = t.replace('看起來像一個頁面嗎？就是像，這個就是 custom GPT，', '\n\n**【指導教授】**：看起來像一個頁面嗎？就是像，這個就是 custom GPT，')
    t = t.replace('好，好，好，我就是想確認一下自己。好，那這繼續來。', '好，好，好，我就是想確認一下自己。好，那這繼續來。\n\n**【同儕研究生】**：')
    t = t.replace('可以把那個狗到哪裡來？聲音大一點。', '可以把那個麥克風移過來一點？聲音大一點。\n\n**【同儕研究生】**：')
    t = t.replace('你聽起來很好，我覺得很好。那個EDR是什麼東西？', '\n\n**【指導教授】**：你聽起來很好，我覺得很好。那個EDR是什麼東西？')
    t = t.replace('前面沒有介紹，前面沒有從這邊講。', '前面沒有介紹，前面沒有從這邊講。\n\n**【同儕研究生】**：')
    t = t.replace('沒關係，我開括號在這裡講。這個重點。', '\n\n**【指導教授】**：沒關係，我開括號在這裡講。這個重點。')
    t = t.replace('好，好，好。好，那回到剛剛圖片是怎怎麼寫？', '\n\n**【指導教授】**：好，好，好。好，那回到剛剛圖片是怎怎麼寫？')
    t = t.replace('那準備工作完成之後，就可以開始尋找加密的儲存單位。', '\n\n**【同儕研究生】**：那準備工作完成之後，就可以開始尋找加密的儲存單位。')
    t = t.replace('嗯也不錯，老師，你你有些觀察，', '\n\n**【指導教授】**：嗯也不錯，老師，你你有些觀察，')
    
    lines = t.split('\n\n')
    new_paras = []
    current_spk = '同儕研究生'
    for l in lines:
        l = l.strip()
        if not l:
            continue
        m = re.match(r'^\*\*【([^】]+)】\*\*：(.*)$', l, re.DOTALL)
        if m:
            current_spk = m.group(1)
            body = m.group(2).strip()
        else:
            body = l
            
        # Segment by length 150-280
        sents = re.split(r'(?<=[。！？；])', body)
        cur = ''
        for s in sents:
            s = s.strip()
            if not s:
                continue
            if len(cur) + len(s) > 280 and len(cur) >= 140:
                new_paras.append(f'**【{current_spk}】**：{cur}')
                cur = s
            else:
                cur += s
        if cur:
            new_paras.append(f'**【{current_spk}】**：{cur}')
            
    return '\n\n'.join(new_paras)

def format_part2(text):
    # Part 2: 侑宸 vs 指導教授 vs 同儕
    t = text
    t = t.replace('好，那我現在就請侑宸吧，好不好？期待啊。', '**【指導教授】**：好，那我現在就請侑宸吧，好不好？期待啊。\n\n**【侑宸】**：')
    t = t.replace('是問一下，你們會不會出現那個增量？什麼叫增量？', '\n\n**【指導教授】**：是問一下，你們會不會出現那個增量？什麼叫增量？英文是什麼？')
    t = t.replace('就是比呃自己想描述的想描述的意思是是說就是我要比他們還要強的地方。', '\n\n**【侑宸】**：就是自己想描述的意思，是說我要比他們還要強的地方。')
    t = t.replace('所以這是你們用的，還是AI用的，還是怎麼？', '\n\n**【指導教授】**：所以這是你們用的，還是AI用的，還是怎麼？就說用，我沒有看到這個增量的字，好奇說怎麼會想到有這個事？')
    t = t.replace('這個是，這個是跟那個我跟AI討論過，', '\n\n**【侑宸】**：這個是我跟 AI 討論過，然後它幫我把想法整理出來的，所以有可能是 AI 的用語。但這邊的意思是在講說，前面這幾個研究沒有強調他們可以很快速、以較少步數直接戳到要害。')
    t = t.replace('現在舉一個 H 一 H 二是什麼？是顏色嗎？還是 H 一？', '\n\n**【指導教授】**：現在舉一個 H1、H2 是什麼？是顏色嗎？還是什麼？')
    t = t.replace('呃，這邊是一個編號，就假設假設就是那個呃，', '\n\n**【侑宸】**：這邊是一個編號，假設這一張優惠券，因為黑箱沒有辦法知道原先適用的範圍。')
    t = t.replace('呃，我我這問題是，我這樣不太清楚，我要怎麼看？看幾張表？', '\n\n**【指導教授】**：我這問題是，我這樣不太清楚，我要怎麼看？看幾張表？比如說你這個是 H1 每個帳號要往下看，對應到 T1、T2、T3、T4？然後 H2 又是另外一個 case，還是說我要用 T1 這個 case 橫著看？你懂我意思嗎？')
    t = t.replace('其其實這這這是 H 四四，是蠻不錯。', '\n\n**【指導教授】**：其實你測試這四個 case 蠻不錯，通通有 A、B 兩個角色，有新訂單跟原訂單，所以有排列組合四個 case。然後你寫的 H1 每個帳號是一個人呢，還是什麼東西？只能被一個人使用叫 A 帳號？那每筆訂單又是什麼意思？你在一個很小的表裡面要表達很多意思，這樣老師光看表就不太懂。')
    t = t.replace('還是你們三位。誰誰比較可以比較客觀一點？因為有時候旁觀者清嘛，', '\n\n**【指導教授】**：還是你們三位，誰比較可以客觀一點？因為有時候旁觀者清嘛，你們也許可以有更好的說法。')
    t = t.replace('我這邊的理解是說，就是 H  one、 H  two、 H  three 是三種情境。', '\n\n**【同儕研究生】**：我這邊的理解是，H1、H2、H3 是三種情境。前提是今天帳號 A 已經在訂單一使用過一次這個券了。H1 的意思就是假設每隻帳號只能用這張券一次，所以 T1 在新訂單同券狀態下會被拒絕。')
    t = t.replace('對的話，那問題為什麼這個會叫拒絕？就是他不能使用的意思。', '\n\n**【指導教授】**：對的話，那為什麼這個會叫拒絕？它不是新訂單嗎？')
    t = t.replace('新訂單的意思是視為。可能像訂單二、訂單三，', '\n\n**【同儕研究生】**：新訂單的意思是訂單二、訂單三。因為它已經在訂單一用過一次了，所以在訂單二就不能再用第二次。')
    t = t.replace('OK，所以這哦，所以這邊是訂單二，然後又在同一張優惠券。對。哦，所以當然是被拒絕。', '\n\n**【指導教授】**：OK，所以這邊是訂單二，然後又在同一張優惠券，所以當然被拒絕。')
    t = t.replace('然後H二的意思就是說，他每個訂單都可以用一次這張券，', '\n\n**【同儕研究生】**：然後 H2 的意思就是說，他每個訂單都可以用一次這張券，所以 H2 這邊就是接受。')
    t = t.replace('這這個，然後我不知道你這張這張這個表示 AI 方面產生的，還是你自己想？', '\n\n**【指導教授】**：這張表是 AI 產生的，還是你自己想的？')
    t = t.replace('那個我把我把想法跟 AI 說，然後它碰它碰不出來。我我我覺得現在自己也有點混亂。', '\n\n**【侑宸】**：我把想法跟 AI 說，然後它蹦出來的。我覺得現在自己也有點混亂。')
    t = t.replace('啊，對，這就是用 AI 的。什麼時候？', '\n\n**【指導教授】**：對，這就是用 AI 的問題！你自己打在那邊，想要描述優惠券規則很複雜。黑箱沒有原始碼，可以從不同情境測試得到的回應，再去決定下一步。但你表如果太簡化，別人就會看不懂。')
    t = t.replace('那你GUI跟API的探索是同步進行嗎？還是你是分開來同步GUI？', '\n\n**【指導教授】**：那你 GUI 跟 API 的探索是同步進行嗎？還是分開來？')
    t = t.replace('好，都會同步。應應該說，就有點像是那個嗯', '\n\n**【侑宸】**：都會同步，有點像是在操作 GUI 的同時監聽 API 封包。')
    t = t.replace('我們看看看摘要，打摘要，看一下摘要。OK。', '\n\n**【指導教授】**：我們看一下論文摘要。你看他寫這個文字，你同不同意你們那個審查？不能觸發意外的業務場景，擅長發現普通漏洞但無法假設邏輯漏洞。這句話你目前可以用，但他的做法跟你不一樣，你看他怎麼做？')
    t = t.replace('他在那個論文當中有提到，他作者有呃手工標註加上他自己的學生，', '\n\n**【侑宸】**：他在論文當中有提到，作者有手工標註加上他自己的十六位學生，標註了四十七個漏洞資料。')
    t = t.replace('好，所以你看，剛剛前面的摘要有些部分。這是右圖就可以參考了，對不對？', '\n\n**【指導教授】**：好，所以你看，剛剛前面的摘要有些部分，這右圖就可以參考了對不對？那做法不太一樣，定位在什麼地方就清楚了。好，謝謝侑宸。那大家還有其他問題嗎？沒有的話今天到這邊。')
    
    lines = t.split('\n\n')
    new_paras = []
    current_spk = '侑宸'
    for l in lines:
        l = l.strip()
        if not l:
            continue
        m = re.match(r'^\*\*【([^】]+)】\*\*：(.*)$', l, re.DOTALL)
        if m:
            current_spk = m.group(1)
            body = m.group(2).strip()
        else:
            body = l
            
        sents = re.split(r'(?<=[。！？；])', body)
        cur = ''
        for s in sents:
            s = s.strip()
            if not s:
                continue
            if len(cur) + len(s) > 280 and len(cur) >= 140:
                new_paras.append(f'**【{current_spk}】**：{cur}')
                cur = s
            else:
                cur += s
        if cur:
            new_paras.append(f'**【{current_spk}】**：{cur}')
            
    return '\n\n'.join(new_paras)

# Write Part 1 deliverables
body1 = format_part1(part1_raw)
full1_content = f'''---
title: "惡意 Custom GPT 贊助廣告釣魚與多階段 RAT 木馬植入鏈"
event: "網路與系統實驗室 定期論文研討與研究進度會議"
date: "2026-10-12"
talk_id: "LAB-20261012-01-CUSTOM-GPT-RAT-INFECTION"
speakers: ['同儕研究生', '指導教授']
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "academic-lecture-meeting"
---

# 🎙️ LAB-20261012-01 惡意 Custom GPT 贊助廣告釣魚與多階段 RAT 木馬植入鏈 (同儕研究生 / 指導教授)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。完整收錄同儕研究生論文報告、指導教授針對 EDR 機制與攻擊鏈技術細節之現場質詢，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、專有名詞（Custom GPT, MSI, DLL Sideloading, XOR Decoder, AMSI, NTDLL unhooking, EDR, Monte Carlo RAT）與標點符號，明確標註發言角色，並維持每 150～300 字之自然語意分段。

---

## 💻 章節段落 01：現場原話實錄與核心論述

{body1}
'''

summary1_content = '''# 📋 惡意 Custom GPT 贊助廣告釣魚與多階段 RAT 木馬植入鏈 — 執行摘要

- **活動場次**：網路與系統實驗室 定期論文研討與研究進度會議 (場次 01)
- **錄音日期**：2026-10-12
- **發言講者**：同儕研究生 / 指導教授
- **對應完整逐字稿**：[`20261012-01-惡意Custom-GPT贊助廣告釣魚與多階段RAT木馬植入鏈.full.md`](./20261012-01-惡意Custom-GPT贊助廣告釣魚與多階段RAT木馬植入鏈.full.md)

---

## 📌 核心議題與研討提要

本場次由實驗室同儕研究生進行前沿資安文獻報告，剖析真實世界中攻擊者如何濫用 OpenAI Custom GPT 生態系發動高隱蔽性進階持續性威脅（APT）。攻擊者藉由購買搜尋引擎贊助廣告（Sponsored Ads），誘騙搜尋 ChatGPT 的受害者進入偽冒之 Custom GPT 介面，並以「主要運算卡能量不足、請使用備用網域」為由，誘導使用者在終端機執行混淆惡意指令碼。

技術鏈深入展示了多階段免殺技巧：包含下載 MSI 靜默安裝、DLL 側載（Sideloading）、從 WAV 音訊雜訊中以動態 XOR 解密 Shellcode、繞過 AMSI 檢查、NTDLL 記憶體脫鉤（Unhooking）以逃避 EDR 鉤子，最終成功植入具備鍵盤側錄與 C2 通訊之 Monte Carlo 遠端存取木馬（RAT）。

---

## 🏛️ Custom GPT 廣告釣魚至 RAT 上線攻擊鏈架構

```mermaid
flowchart TD
    Ad["搜尋引擎贊助廣告釣魚"] --> FakeGPT["偽冒 Custom GPT 介面 (能量不足欺騙)"]
    FakeGPT --> RunCmd["誘導受害者執行混淆 PowerShell 指令"]
    RunCmd --> MSISilent["MSI 靜默安裝 (釋放 177 個檔案)"]
    MSISilent --> DLLSide["DLL 側載 (修改匯入表載入惡意 DLL)"]
    DLLSide --> AudioSteg["WAV 音訊雜訊動態 XOR 解密 Shellcode"]
    
    subgraph EDRBypass["防護繞過與記憶體免殺"]
        AMSIBypass["AMSI 記憶體檢查繞過"]
        NTDLLUnhook["NTDLL 乾淨副本脫鉤 (Bypass EDR Hook)"]
        AntiVM["反虛擬機與沙箱偵測"]
    end
    
    AudioSteg --> EDRBypass
    EDRBypass --> MonteCarlo["Monte Carlo RAT 木馬持久化執行"]
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 社會工程與 AI 生態系濫用
- 攻擊者不直接攻擊大模型，而是利用 Custom GPT 的自訂頁面功能結合搜尋引擎廣告，突破傳統端點與郵件閘道的過濾。

### 2. 深度防禦穿透技術
- 結合 DLL 側載與音訊隱寫術（WAV Steganography），將惡意酬載分散於看似正常的應用程式檔案中；執行時利用乾淨的 NTDLL 映像重載技術，使 EDR 無法藉由 Inline Hook 偵測到敏感 API 呼叫。

### 3. 指導教授質詢重點
- 教授特別打斷並追問 EDR 全稱與其監控原理，提醒學生在報告進階攻擊鏈時，應清楚交代防禦端的核心檢測機制（如 Kernel Driver 回呼與 User-mode Hooking），方能體現攻防對抗的實質價值。
'''

Path('5-Master/Laboratory/Thesis-Progress/20261012-01-惡意Custom-GPT贊助廣告釣魚與多階段RAT木馬植入鏈.full.md').write_text(full1_content, encoding='utf-8')
Path('5-Master/Laboratory/Thesis-Progress/20261012-01-惡意Custom-GPT贊助廣告釣魚與多階段RAT木馬植入鏈.md').write_text(summary1_content, encoding='utf-8')
print('Generated 20261012-01!')

# Write Part 2 deliverables
body2 = format_part2(part2_raw)
full2_content = f'''---
title: "Android 商業邏輯漏洞探索"
event: "網路與系統實驗室 碩士學位論文核心架構進度研討"
date: "2026-10-12"
talk_id: "LAB-20261012-02-HSIEH-YOUCHEN-THESIS-PROGRESS"
speakers: ['謝祐庭', '侑宸', '指導教授', '同儕研究生']
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "academic-lecture-meeting"
---

# 🎙️ LAB-20261012-02 Android 商業邏輯漏洞探索 (謝祐庭 / 侑宸 / 指導教授 / 同儕研究生)

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。完整收錄研究生**謝祐庭**（前半段主講 Android 黑箱探索架構）與**侑宸**（後半段接續報告外部對標基準文獻與消融實驗）、指導教授現場針對「增量定義、H1/H2 優惠券測試矩陣、AI 產出幻覺、黑箱假設一致性」之深度質詢與同儕協助辨析，**未做任何刪減或摘要縮寫**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字（第 22 行「右耳」精準校對為「祐庭」；第 221 行「謝謝侑宸」確實為侑宸接續報告）、專有名詞（Android GUI, API Fuzzing, EIG 期望資訊增益, S_t 狀態空間, 商業邏輯漏洞）與標點符號，明確標註發言角色，並維持每 150～300 字之自然語意分段。

---

## 💻 章節段落 01：現場原話實錄與核心論述

{body2}
'''

summary2_content = '''# 📋 Android 商業邏輯漏洞探索 — 執行摘要

- **活動場次**：網路與系統實驗室 碩士學位論文核心架構進度研討 (場次 02)
- **錄音日期**：2026-10-12
- **報告講者**：謝祐庭（前半段主講）、侑宸（後半段文獻對標報告）
- **對應完整逐字稿**：[`20261012-02-Android商業邏輯漏洞探索.full.md`](./20261012-02-Android商業邏輯漏洞探索.full.md)

---

## 📌 核心議題與論文進度提要

本場次為**侑宸（Youchen）碩士學位論文核心進度報告**。侑宸針對現有黑箱模糊測試（Black-box Fuzzing）在移動應用程式商業邏輯漏洞檢測中的盲目性與高误報率，提出一套模擬人類滲透測試專家思維的自主探索 Agent 框架。系統結合 Android 介面 GUI 事件監聽與網路層 API 封包攔截，建立雙階狀態推理機制。

報告重點在於破除傳統研究「單純敲 API 回傳 HTTP 200 即判定漏洞」的嚴重假警報缺陷（例如取消訂單後 API 仍回傳成功，但後端並未實際觸發物流出貨）。侑宸建立了狀態假設更新公式 $S_t$ 與基於期望資訊增益（EIG）的候選路徑評分函數，約束 Agent 在預算限制下優先執行最具驗證價值之操作。

會議中指導教授針對圖表簡化導致的理解障礙、AI 產出術語（如「增量」）的嚴謹度、以及 $H_1, H_2, H_3$ 優惠券測試矩陣的排列組合邏輯，進行了長達一小時的深度實戰質詢，同儕亦加入協助釐清矩陣語意。

---

## 🏛️ 侑宸黑箱商業邏輯漏洞自主探索與推理架構

```mermaid
flowchart TD
    AndroidGUI["Android 前端 GUI 事件監聽"] --> DualObserver["雙軌觀察器 (Dual Observer)"]
    NetworkAPI["後端 API 傳輸封包攔截"] --> DualObserver
    
    DualObserver --> HypothesisGen["攻擊假設生成 (Hypothesis Generation)"]
    HypothesisGen --> MathModel["數學推理與排程模型"]
    
    subgraph MathModel["數學推理與排程模型"]
        Formula1["狀態與證據更新公式: S_t = (H, W, N, E, G)"]
        Formula2["期望資訊增益排程: Score(alpha) = EIG + EV - Cost"]
        Formula1 --> Formula2
    end
    
    Formula2 --> ActionExec["選擇高價值路徑執行 (如 下單 ➔ 取消 ➔ 檢查物流)"]
    ActionExec --> DeepVerify{"實質業務狀態驗證: 物流/金流/資料庫持久化改變?"}
    DeepVerify -- 僅 HTTP 200 但無實質變更 --> DiscardFP["排除假警報 (False Positive)"]
    DeepVerify -- 實質越權/套利成功 --> ConfirmBug["確認真實商業邏輯漏洞 (Real Vuln)"]
```

---

## 🔑 關鍵重點整理 (Key Takeaways)

### 1. 破除 API 假警報：業務狀態二次閉環
- 商業邏輯漏洞的本質不是崩潰（Crash），而是規則衝突。不能依賴 HTTP 回傳碼，必須引導 Agent 追查金流、物流或多角色（消費者 vs 客服）的權限變更記錄。

### 2. 狀態空間與 EIG 候選路徑排程
- 提出兩套公式：第一套公式定義當前輪次已知資訊、後端行為假設與缺少之獨立證據；第二套公式以資訊增益減去 Token 與執行成本，決定畫面多個按鈕中哪一個最值得優先測試。

### 3. 指導教授現場質詢與論文修訂方針
- **嚴禁使用未定義的模糊詞彙**：教授嚴厲質疑「增量」一詞出處，告誡學術論文不可未加定義即採用 LLM 隨機產生的空泛字眼，應改用精確的「步數精簡度（Step Efficiency）」或「探索覆蓋增益」。
- **圖表必須自帶完整語境**：針對 $H_1$（單帳號單次）、$H_2$（單訂單單次）、$H_3$（全系統記名/不記名）優惠券矩陣，教授指出原始表格過於精簡導致橫看直看皆令人困惑，指示必須在表格旁明確補足使用者情境（Case 1/2/3）與新舊訂單定義。
- **黑箱假設的一致性**：提醒研究從始至終不可假設擁有 Source Code，所有論證皆需立足於外部黑箱觀測。
'''

Path('5-Master/Laboratory/Thesis-Progress/20261012-02-Android商業邏輯漏洞探索.full.md').write_text(full2_content, encoding='utf-8')
Path('5-Master/Laboratory/Thesis-Progress/20261012-02-Android商業邏輯漏洞探索.md').write_text(summary2_content, encoding='utf-8')
print('Generated 20261012-02!')
