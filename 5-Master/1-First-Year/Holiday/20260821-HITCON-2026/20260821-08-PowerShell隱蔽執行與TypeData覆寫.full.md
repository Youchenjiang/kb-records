---
title: "HITCON 2026 閃電秀：PowerShell 隱蔽執行與 TypeData 屬性覆寫奇技淫巧"
event: "20260821-HITCON 2026 台灣駭客年會"
date: "2026-08-21"
talk_id: "HITCON-2026-LT-08"
speakers: ["阿斯卡 (Aska)"]
type: "verbatim-narrative-transcript"
verbatim: true
scenario: "single-talk"
---

# 🎙️ 2026 閃電秀：PowerShell 隱蔽執行與 TypeData 屬性覆寫奇技淫巧

> **【排版與校對說明】**：本文件為 **100% 全篇原話逐字稿深度校對與角色對話標註版**。完整收錄講者現場演講原話、現場會眾互動與展示，**未做任何刪減、摘要或人工造假注入**；已依據專案校對手冊（`PROOFREAD_RULES.md`）地毯式修訂語音辨識錯字、專有名詞與標點符號，明確標註發言角色，並維持 150～300 字之自然語意分段。

---

## ⚡ 閃電秀 5：PowerShell 隱蔽執行與 TypeData 屬性覆寫奇技淫巧（阿斯卡）

**【大會主持人】**：第五位講者是阿斯卡，題目叫做《PowerShell》。PowerShell 到底做了什麼事情會讓講者忍不住下這個結論？螢幕有畫面了嗎？看起來還沒有。那阿斯卡對 PowerShell 有多生氣呢？就像現在螢幕一樣黑畫面，非常生氣！

現在設備調整需要一點時間，那我們只好來講個冷笑話撐場。說到剛才講的中二病，其實我小時候也有一個夢想：想要成為很厲害的魔法少女！希望大家也都有自己的夢想並實現它。好了，我撐不下去了，到底有沒有畫面？……好，畫面出來了！掌聲歡迎第五位講者阿斯卡！

**【阿斯卡】**：大家好，我相信用過 PowerShell 的人都覺得這是個很怪的東西。雖然現在跨平台都可以跑 PowerShell，但我相信大家在 Linux 或 macOS 上絕對不會想用 PowerShell。快速講一下 PowerShell 到底有哪些怪東西：首先它支援 Tab 補全、不分大小寫；支援直接載入 C# 程式碼調用 Windows API；還有很奇怪的內建變數，像是我很喜歡用的 $ExecutionContext，你可以一路往上爬並執行各種操作，甚至可以直接在裡面執行 Inline Assembly！它的跳脫字元不是常見的反斜線，而是用 Backtick（反引號 `）；參數名稱只要打前幾個字母就可以自動辨識縮短。

但這些都不夠怪，前幾個月我發現了一個更冷門、更隱蔽的機制——**PowerShell TypeData 屬性覆寫（Override）**！

PowerShell 允許透過 TypeData 自訂或覆寫 .NET 物件的屬性與成員 Getter。我們要怎麼 Forge（偽造）東西呢？例如：我們可以直接覆寫 System.IO.FileInfo 的屬性 Getter，將惡意 Payload 注入其中。當管理員在終端機鍵入常規的 `ls`（Get-ChildItem）列出目錄檔案時，背景便會自動觸發 Getter 內注入的程式碼！

另一招是利用 `System.Management.Automation.PSVariable` 偽造變數屬性，讓 `Get-Variable` 只顯示看似正常的數值以規避安全檢測。更絕的是在 `CodeProperty` 塞入成員，每次目錄進行 Enumerate 列舉時都會自動執行注入的程式碼。最關鍵的是——**這種手法完全不留下任何 PowerShell ScriptBlock 日誌**！因此 EDR 與 SIEM 監控根本抓不到！

你可能會想說為什麼要這樣做？因為在物件屬性裡塞一行執行代碼，日常維運根本不會有人察覺。公開的 PowerShell 資安研究中我也幾乎沒看過有人這樣用過。如果有人想用 `Get-Member` 去排查，但別忘了 `Get-Member` 本身的輸出也是可以被 Override 掉的！我的分享就到這邊，謝謝大家。

**【大會主持人】**：好，感謝第五位講者阿斯卡！

---

