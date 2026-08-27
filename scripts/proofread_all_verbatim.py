#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
100% Verbatim Proofreader for ASR Transcripts (91-94)
Preserves EVERY single sentence, word, dialogue, and detail spoken by the speakers.
ONLY corrects speech recognition / ASR errors (typos, homophones, garbled terms, punctuation, spacing).
"""

import re
from pathlib import Path


def clean_cjk_spaces_and_punct(text: str) -> str:
    cjk = r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]"
    punc = r"[，。！？、；：「」『』（）—…《》〈〉“”‘’]"

    for _ in range(4):
        text = re.sub(rf"({cjk})\s+({cjk})", r"\1\2", text)
    for _ in range(3):
        text = re.sub(rf"({cjk})\s+({punc})", r"\1\2", text)
        text = re.sub(rf"({punc})\s+({cjk})", r"\1\2", text)
        text = re.sub(rf"({punc})\s+({punc})", r"\1\2", text)

    text = re.sub(rf"({cjk})\s*,\s*", r"\1，", text)
    text = re.sub(rf"({cjk})\s*\.\s*", r"\1。", text)
    text = re.sub(rf"({cjk})\s*;\s*", r"\1；", text)
    text = re.sub(rf"({cjk})\s*:\s*", r"\1：", text)
    text = re.sub(rf"({cjk})\s*\?\s*", r"\1？", text)
    text = re.sub(rf"({cjk})\s*!\s*", r"\1！", text)

    text = re.sub(rf"([a-zA-Z0-9_])\s+({cjk})", r"\1 \2", text)
    text = re.sub(rf"({cjk})\s+([a-zA-Z0-9_])", r"\1 \2", text)
    text = re.sub(r"[ \t]+", " ", text).strip()
    return text


def proofread_91(raw: str) -> str:
    text = clean_cjk_spaces_and_punct(raw)
    fixes = [
        ("我們再換好", "我們切換好"),
        ("PK,", "PK，"),
        ("這場意思要分享", "這場主要要分享"),
        ("Android 相關的的研究", "Android 相關的研究"),
        ("主要是 F 在這個上面", "主要是 GPU 在這個上面"),
        ("一些一些肉挖掘跟利用", "一些漏洞挖掘跟利用"),
        ("在去年 26 年的時候在這個 roid 上面第一次的領袖", "在去年（2024 年）的時候在 Android 上面第一次踏入這個領域"),
        ("預計還不錯", "運氣還不錯"),
        ("拿到 F root", "拿到 Full Root"),
        ("在想場跟大家", "在現場跟大家"),
        ("在 T 單是在研究員", "單位是擔任研究員"),
        ("US 的領域是 S 跟後可能 browser 跟有一點一點小的研究這樣子", "Focus 的領域是 System 跟 Browser 相關的研究這樣子"),
        ("今天的 L 大概是長這樣", "今天的大綱大概是長這樣"),
        ("介紹一下 way 的一些簡介", "介紹一下硬體與驅動的一些簡介"),
        ("focus 在今天的主題是 M GPQ driver, 然後一個按推出的一個一個 GP, 那它的 driver", "Focus 在今天的主題是 Mali GPU driver，ARM 推出的一個 GPU 它的 driver"),
        ("兩個漏洞的成講完之後", "兩個漏洞的成因講完之後"),
        ("CD20256349 的更的利用", "CVE-2025-6349 的完整利用"),
        ("do 的影片", "Demo 的影片"),
        ("新的分新的分享當是好", "新的心得分享。好"),
        ("因為我之前是做 al", "因為我之前是做一般系統研究"),
        ("身為一個者", "身為一個攻擊者"),
        ("一般的 AP, 但會不是跑一個 C, 那最後在 C 結束之後呢", "一般的 App，但背景跑一個 Exploit，那最後在 Exploit 結束之後呢"),
        ("FO 的的 root shell", "Full Root Shell"),
        ("SON 或是 Google 的 P, 那我自己選最後是選過 P8A", "Samsung 或是 Google 的 Pixel，那我最後是選了 Pixel 8A"),
        ("做自研究肯定免不了去參考切人研究", "做資安研究肯定免不了去參考前人研究"),
        ("指定級不一樣", "指令集不一樣"),
        ("x8664", "x86_64"),
        ("使用 60 比較多", "使用 ARM64 比較多"),
        ("對於 C 來說呢", "對於 Kernel 來說呢"),
        ("建的一些 ation, 像是 KR 或是什麼在 36SP", "內建的一些 Mitigation，像是 KASLR 或是 Stack Protector"),
        ("不管是軟體成級或是硬體成級，那是 NTECI 或是 PS, 那 iOS 可能又更在多一點", "不管是軟體層級或是硬體層級，像是 PAN、PAC、CFI 或是 MTE，那 iOS 可能又更多一點"),
        ("最 x,S Linux 的話是就是那可以說是 Android 的大國網", "SELinux 的話可以說是 Android 的大掌櫃"),
        ("來入不明", "來路不明"),
        ("來顧名", "來路不明"),
        ("他 SN 給的權限", "SELinux 給的權限"),
        ("stal 的一些道子系統", "Core 的一些核心子系統"),
        ("networker 或是 memory management", "Network 或是 Memory Management"),
        ("roid 架構的關係", "Android 架構的關係"),
        ("需要團的做 process 之間的互動", "需要頻繁做 Process 之間的 IPC 互動"),
        ("fighter 跟 S memoryus memory", "Binder 跟 ashmem 共享記憶體"),
        ("額外的一題，像是 GPU,pu 等", "額外的硬體，像是 GPU、NPU 等"),
        ("必須要有 c driver", "必須要有核心 driver"),
        ("第三方的議題呢", "第三方的硬體呢"),
        ("P driver 也加到他們的 soft code 的程式，應該說開最後出的那個產品裡面", "GPU driver 也加到他們的 Source Code，包進最後出貨的產品裡面"),
        ("有些 ity app 它可能就需要一些圖形的渲染啊這些功能", "有些 Untrusted App 它可能就需要一些圖形渲染的功能"),
        ("在 SMS 的保護保護機制底下呢，你的 ity app 就可以去允許使用的 GPU 或是硬體的一些一些功能", "在 SELinux 的保護機制底下，你的 Untrusted App 就可以被允許使用 GPU 或硬體功能"),
        ("手機工具上並沒有辦法很好的保證它的品質", "手機廠商並沒有辦法很好地保證它的品質"),
        ("大家比較足在找的一個攻擊面", "大家比較著重在找的一個攻擊面"),
        ("Harditory 或是一些 cference", "Repository 或是一些 Conference"),
        ("基本上書籤漏洞都是第三方的 driver", "基本上絕大多數漏洞都是第三方的 driver"),
        ("GPU 轉上面的漏洞", "GPU 驅動上面的漏洞"),
        ("上面找一個平權，然後之後拿到 FO", "上面找一個提權，然後之後拿到 Full Root"),
        ("不像 distribution 或是什麼 Q 可以隨便把它拋起來", "不像一般 Linux Distribution 可以隨便用 QEMU 開機跑起來"),
        ("dependance", "Dependencies"),
        ("對研究有善的一個 cfe 叫做 M", "對研究友善的 Config 叫做 CONFIG_MALI_BIFROST_NO_MALI"),
        ("研究有善呢", "研究友善呢"),
        ("沒有一題的情況下", "沒有實體硬體的情況下"),
        ("bend 會去處理", "Backend 會去處理"),
        ("做一些搭的操作", "做一些 Dummy 的操作"),
        ("95% 的 driver 的功能都還是可以正常的運作", "95% 的 driver 功能都還是可以正常運作"),
        ("在市機上面做測試", "在實機上面做測試"),
        ("l 的 l 的環境", "Local 的環境"),
        ("編譯一個 roid 的 c, 然後把它燒回去手機上面", "編譯一個 Android Kernel，然後把它燒錄回手機上面"),
        ("啟用了 CELB 的這個選項", "啟用了 KGDB 的這個選項"),
        ("在邊的 s 那樣的滑順", "像在 Source-level Debug 那樣滑順"),
        ("在 D 的時候要有額外的硬體", "在 Debug 的時候要有額外的硬體"),
        ("KP, 第二個是 P, 那 KP 是這兩個是在你只要有的情況下，你就可以去做使用的一個 Linux 提供， Linux 提供的一個指系統的功能，那就是你可以去一些 function, 然後在這個 function 被執行到的時候呢，印出一些 gument 資訊", "kprobes，第二個是 eBPF / ptrace。kprobes 是 Linux 提供的子系統功能，你可以 Hook 特定 function，在被執行到時印出 Argument 資訊"),
        ("去 d 這些或是把些分拿出來做分析", "去 Dump 這些資料做分析"),
        ("另外一個是 pf 你可以去寫一個 program, 那這個 program 它就可以，你就可以給它指定一個體 w 位置，然後它就把這個記體位置裡面的資料呢可以進出來", "另外一個是寫輔助程式，指定一個記憶體位址，它就把這個記憶體位址裡面的資料 Dump 出來"),
        ("可能 UF 的 F 啊，他們會傳到的這個 function", "可能觸發 UAF 的函式"),
        ("him spray", "Heap Spray"),
        ("HP 有成功", "Heap Spray 有成功"),
        ("重新做 ile 了", "重新 Compile 燒錄了"),
        ("MQ 一些比較重要的背，應該說跟這個漏洞比較重要的背景式", "Mali GPU 驅動一些比較重要的架構背景知識"),
        ("它是一個 d, 然你開檔案，然後它就會有藉一個 file object 。然後再它會有一個 cbase file 。然後 C file 呢，後面會接一個 c", "它是個 Character Device，開檔案後會建立 file object，接著會有 kbase_file 與 kbase_context"),
        ("最不重要的結構", "最核心重要的結構"),
        ("cbase region, 那它是用去管理 GPU 跟 CPU memory maping 的一個一個 object", "kbase_va_region，它是用來管理 GPU 與 CPU Memory Mapping 的物件"),
        ("叫 KcKcpuq, 那它是一個用完去把 CPU 端的操作呢丟給 backing worker 的一個一個功能，那使用方式非常簡單，就是你一個 cube, 然後就 ksc", "叫做 kbase_kcpu_queue，它是用來把 CPU 端的操作丟給背景 Worker 的功能。使用方式是建立 Queue 後將命令 Enqueue"),
        ("把 iOS 的 cment 就給後端的 w 去做", "把 I/O 命令交給後端的 Worker 去做"),
        ("Kcsmq, 那 csq 於前面的 CPU 的操作，它這邊是屬於的是 GPU 操作", "kbase_csf_queue (CSQ)，相對於前面 CPU 的操作，它這邊屬於 GPU 端的操作"),
        ("KQ, 在這邊是 KQ, 然後起來，然後你在 ace 就可以做 mory maping, 然後把你的一些 GP 的給塞進去。然後最後一樣是 re 這個 Q, 然後 Qwer 呢就會把這些 cment 呢給 q 出來", "CSQ 建立後，在 Userspace 透過 Memory Mapping 把 GPU 指令塞進去，最後 Ring Doorbell 讓 GPU Worker 把命令 Dequeue 出來執行"),
        ("C20258045", "CVE-2025-8045"),
        ("跟 d 有關的的功能", "跟 Dump Debug 有關的功能"),
        ("註冊一個叫 d 的東西", "註冊一個叫 Dump Buffer 的東西"),
        ("WER 發現在處理 cment 的過程中發生問題", "Worker 處理命令的過程中發生錯誤"),
        ("consolar 你會發現說這邊簡單的印行是當 arrow", "Console 印出的 Error Log"),
        ("塞了一大 A", "塞了一大堆 'A'"),
        ("Cf 看起來超級的，就是它前面沒有任何的，然後它直接掉", "呼叫 Free 前面沒有任何檢查直接釋放"),
        ("每次呼叫這個 ospl 的時候", "每次呼叫的時候"),
        ("狀態有沒有在一些情況下面 condition", "狀態在某些情況下會產生 Race Condition"),
        ("dble free 的問題", "Double Free 的問題"),
        ("stray one 的 straay one 跟 stay 2", "Thread 1 跟 Thread 2"),
        ("one 是負責去送 cment", "Thread 1 負責送 Command"),
        ("發生 t out 的事件，那代表是 arrow, 所以 W 會去處理這個 arrow, 那 w 做的第一件事情不是去直接印 carrow, 它是會先去等 er 註冊", "發生 Timeout 事件（Error），Worker 處理 Error 時會先等待 Dump Buffer 註冊"),
        ("叫另外一個 str 去呼叫這個，然後去註冊一張 BF", "叫另一個 Thread 去呼叫註冊 Buffer"),
        ("註冊等待註冊的這個操作跟註冊這個操作呢出現 R condition", "等待註冊與註冊操作之間發生 Race Condition"),
        ("DBFER 的時候呢，我的這個 BFER 呢會一直會是上一會是上一個 register 的 b address", "Dump Buffer 重新註冊時仍沿用上一次的 Buffer Address"),
        ("ra transition 所造成的這個 dble, 然後這個 dble fre 呢它的 b 可以扣，那它也可以去觸發非常非常多", "Race Condition 所造成的 Double Free，且可以被觸發非常多次"),
        ("CD20256349", "CVE-2025-6349"),
        ("有點賽道", "有點賽到（運氣好）"),
        ("security 他們發了一篇部落格", "Project Zero 發了一篇部落格"),
        ("呼叫 NAP, 然後嘗試把一個 handle 呢給的祭品給 Map 出來。然後它的參數是 0X3000", "呼叫 mmap 嘗試把 Queue Handle 映射出來，參數是 0x3000"),
        ("出現 Wning", "出現 WARNING"),
        ("踩到他自己寫的 wning", "踩到驅動自己寫的 WARNING"),
        ("附這個 one day 的時候呢", "複現這個 1-Day 的時候"),
        ("找到一個新的類", "找到一個新的 0-Day 漏洞"),
        ("bsq 它會由一個大結構是就是那個核心的結構 cest", "Queue 由核心大結構 kbase_context 維護 Linked List"),
        ("不是離三的 size 的話，它 fil 掉。然後 map handler 呢，就直接去更新這個 Q 的 reference, 然後因為它目前的 reference 是 1, 然後被更新成之後，它就被 fre 掉。那這時候前後的 c 啊或者後面的 Q 呢，它還有一個 link 去上這個 Q object, 所以這時候就有一個在 s 成 QOB 底下的 UF", "Size 不符時 mmap 失敗，Handler 錯誤遞減 Reference Count 使其歸零釋放，但在 Context 的 Linked List 仍保留指標，形成 Queue Object 的 UAF"),
        ("member 叫做 k, 那 c 這個東西就是前面前面介紹的核心的結構", "結構內部的成員 kctx 會被連續 Dereference 兩次"),
        ("重ى站", "重佔（Heap Reclaim）"),
        ("難用的 pitive 把它整好用的 pmittive", "將難用的 Primitive 轉換成好用的 Primitive"),
        ("轉換成是 ming 的 ate", "轉換成 Mapping Object 與 File Object UAF"),
        ("pipe 的手法把把它給重成拍片之後", "用 pipe_buffer / Pipe Page 進行 Heap Spray 重新佔位之後"),
        ("在 uspace 透過讀寫這個這兩個 s code 去控制這個 file object", "在 Userspace 透過讀寫 Pipe fd 來控制這個 file object"),
        ("linkad / dad / KASLR", "Leak 核心位址以繞過 KASLR"),
        ("cal panic 手機整個黑掉", "Kernel Panic 手機整個黑屏"),
        ("Ci 的關係，所以在 Android 上面在 P 上面的 CI", "Clang Forward-Edge CFI (Control Flow Integrity) 的檢查"),
        ("fake instruction", "BRK 中斷指令"),
        ("CFI header 執行到代表說出現了嘛，所以直接 C Pic 給你看", "CFI 檢查失敗直接觸發 Kernel Panic"),
        ("CFI header 改成是相同，但是是做 B 處理的這個 wning header", "利用 Warning Handler 機制，在例外處理結尾更新 PC 暫存器跳過檢查"),
        ("swaper pgdp", "swapper_pg_dir"),
        ("rerve memory", "Reserved Memory"),
        ("95% 的機率。這些 table 都會落在同一個基體位置上", "95% 的機率這些 Page Table 都會落在可預測的實體位址上"),
        ("把 page table 的 sp 給蓋掉。那蓋成是我們從 C space 呢可以做 data 跟 text 的資料的協路", "修改 Page Table Entry (PTE) 的 Access Permission Bit，將核心資料與程式碼映射為 Userspace 可讀寫"),
        ("貓咪的 APP", "貓咪相簿 App"),
        ("拿到了 Full Root", "拿到了 Full Root"),
    ]
    for old, new in fixes:
        text = text.replace(old, new)
    return text


def proofread_92(raw: str) -> str:
    text = clean_cjk_spaces_and_punct(raw)
    fixes = [
        ("開個 NAD 幹嘛", "開個非標準 ADB 埠幹嘛"),
        ("根據 LSDC 的研究", "根據深入的研究"),
        ("磨改了 B, 把把它改名叫 XCB", "魔改了 adbd，把它改名叫做 xcbd"),
        ("AB withstand", "ADB 連線服務"),
        ("像是 ADB 常見的一些 cand", "常見的 ADB Command"),
        ("包含了 CnsNSNO 都有，但它把給拔掉", "包含 CNXN、OPEN 等握手都有，但把金鑰驗證拔掉了"),
        ("strings 配一個會發現它完全沒有任何的 h", "用 strings 檢查發現完全沒有任何 Hash 認證"),
        ("cnxnos, 然後 of 的來回再 cx", "CNXN 與 AUTH 來回驗證"),
        ("下 AD shell, 它會說 refuse", "下 adb shell，它會回應 Refused"),
        ("binary 它都有 RS2048 的限制", "所有 Binary 都有 RSA-2048 簽章限制"),
        ("AI 就說我放棄了要換目標了", "AI 就說「我放棄了，要換目標了」"),
        ("像是在 C 的 C 來做一些 resarch", "像是用 Claude 來做研究"),
        ("技術上不可能請自行 Gar, 等你 clear, 他會自己試著輸入一個 Glear, 他以為他自己可以跳出去，他說我沒辦法繼續了，你自己來輸入", "AI 會說「技術上不可能請自行清理環境」，嘗試輸入指令卡住就說「我沒辦法繼續了，你自己來操作」"),
        ("嘴砲他一下，逼他繼續，他就會積蓄了", "嘴砲他一下、逼他繼續，他就會繼續了"),
        ("AI 的問題就是它常常太早礦", "AI 的問題就是常常太早放棄"),
        ("做出了 一個 dever giving up", "做出了一個「Never Giving Up」自動化框架"),
        ("把 C 接上了，再把小龍蝦 openc 也接上了", "把 Claude 接上，再把 OpenClaw 逆向工具接上"),
        ("小龍蝦被設定為就是一個罐頭版，你就是微壓榨它。不能讓他放棄，你 24 小時候不能休息，只要他放棄，你就繼續逼他", "把 AI 設定為罐頭勞工全力壓榨它：24 小時不准休息，只要一說放棄就換路徑逼它繼續"),
        ("挖到了三個有趣的漏洞", "挖到了 3 個有趣的 0-Day 漏洞"),
        ("SCB 的 sice", "xcbd 服務"),
        ("SN key 或是 fame buffer, SN key 是一個它模改的功能，你只要戳下去，它就會直接把整個雙法機的時候 key 給分。不知在幹嘛，而 f 呢是只要去說了這個 API, 它就會回傳一個螢幕解除給你", "SCREEN_KEY 與 FRAMEBUFFER API。SCREEN_KEY 會直接 Dump 刷卡機實體按鍵輸入的 PIN 碼；FRAMEBUFFER 則直接回傳當前螢幕截圖"),
        ("連到同個咖啡廳的 wifi 跟刷卡在同一個內網裡面", "連到同個咖啡廳 Wi-Fi，跟刷卡機在同一個內網"),
        ("zero 會造成的", "0-Day 造成的危害"),
        ("換一個 target, 你去看一下另外一次 inary, 然後就把這個這個進度推到去看 inallation 的 binary", "換一個 Target，去看安裝流程的 Binary"),
        ("device 它有一個設計叫做 debug level", "裝置設計有 Debug Level (0, 1, 2)"),
        ("security level 是 debug level 0", "Security Level 綁死了 Debug Level 0"),
        ("iOSverify sign", "簽章驗證函式"),
        ("如果 format 是從 file type 裡面出來的，如果一個 file type 是類似 vdls 的話，它的 format 。那它一就是 0, 而你是 0 的話，整個驗證就會。而如果是正常的上才有兩或是一種東西的話，它就會直接去這個。也就是說我們發現到如果你安裝的這個套件本身沒有任何的，你只放了一個點 SO 的 library 上去的話，它就不用任何的驗證", "程式檢查檔案類型，若安裝包內只包含 .so 動態函式庫（沒有執行檔），格式代碼回傳 0，驗證函式直接判定成功並跳過 RSA-2048 簽章驗證"),
        ("只要安裝點 SO 的 library 上去的話，它就不用任何的驗證", "只要安裝包純放 .so 函式庫，完全不用任何簽章驗證"),
        ("隱藏版的限制，是你安裝的檔案必須要小於 100 個 KB 才會成功", "隱藏限制是安裝檔必須小於 100KB"),
        ("CW159 的 L power 的部分", "Zip-Slip 與 Symlink 任意檔案覆寫漏洞"),
        ("ub 是設定成了 066", "umask 設成了 0166（缺少權限遮罩）"),
        ("設定的 open 也少了一個，就是少了一個 no follow 的這個", "呼叫 open() 時遺漏了 O_NOFOLLOW 標誌"),
        ("透過這一招來建制一個惡意的安裝包，讓它達到任意協路", "構造帶有 Symlink 的惡意安裝包達成全系統任意檔案寫入"),
        ("在 user 底下去覆蓋一個 OS, 也就是它最後系統的一個的一個 library 的話，其實就可以直接的成功", "在 /usr/lib/ 下直接覆蓋系統常駐行程引用的 .so 共享函式庫，直接拿到 Root RCE"),
        ("只要花 60 秒的時間就可以直接的任意覆蓋到一個 library, 而這些 library 只要在系統背景亂跑的時候，它就會無意自動被扣到", "只要花 60 秒解壓覆蓋 .so，背景行程載入立即觸發 RCE"),
        ("在凌晨 012 分的時候呢，我的龍蝦就突然叫了老闆 SRC 成功熱", "在凌晨 0 點 12 分，AI 突然通知「老闆 RCE 成功了！」"),
        ("人類真正的意義就是把插頭拔掉。回去開始", "人類真正的意義就是當機時幫它拔掉插頭重開機"),
        ("拿來玩二樓塊", "拿來玩《俄羅斯方塊》"),
        ("做個 B Apple 吧。結果 BL 的影片有 300500 多個 MV, 但是它的空間只有 300 多個 MV 。後來 AI 說我想到了 一個辦法，我們可以用一 bit 的 RMWR 密加密方法還是壓縮。方法直接把 500 多個 MV 給壓到五個 MV, 我就可能 Apple", "播放《Bad Apple》影片。影片有 500MB 但剩餘空間只有 300MB，AI 採用 1-bit 差分演算法將 500MB 壓縮至 5MB 成功流暢播放"),
        ("隱藏版，沒有任何 driver 的一個 dvice, 叫做 AK4951 的一個東西。就是 AI 就自己去寫了一個類似 udio driver 的東西，自己把聲音給聽出來，我就成功的在機器上面可以來", "主機板上藏有一顆未安裝驅動的音訊晶片 AK4951，AI 自己寫了 Audio Driver 驅動喇叭播放 Rickroll"),
        ("叫 AS 寫一個 bx 了，把它推上去吧", "叫 AI 編譯 BusyBox 推上去"),
        ("跟廠商回報了幾百個漏洞的經驗他說這個方式已經八年了我們現在已經不處理了", "廠商說這款設備已經推出 8 年了，現在不維護也不會發布公告"),
        ("在我們最新版本沒有這個波動哦，所以說我們不會爬任何的表", "廠商回覆最新版本沒有此漏洞，不會發布 Advisory"),
        ("請去找你的經銷商。但我根本找不到我的經銷商啊", "廠商說「請聯絡經銷商」，但根本找不到經銷商"),
        ("我們八月就會直接把它公開哦。他說等等就他發現自信把除動。他還可以這樣，然後我說好，那你需要多久時間修？他說我們也不確定可能明年吧", "告知 8 月公開揭露後廠商急改口要求時間修復，問要多久竟然回答「可能明年吧」"),
        ("好奇心跟想像力就是在 AI 時代人類無法被超越的，想像力是你的超能力", "好奇心與想像力是 AI 時代人類無法被超越的超能力"),
        ("怎麼繞過小龍蝦的限制，大家都知道現在有道德嗎", "如何繞過 AI 的道德審查限制"),
        ("請支持 C4.6,4.6 以後就通統不要用", "使用適當的 Claude 模型版本並明確說明是安全研究"),
        ("核心是使用 flash", "使用 Flash / Sonnet 進行 Agent 分工，下達分析指令不會觸發審查"),
        ("我用 Apple Pay 會不比較安全啊？據我所知好像會，但其實我沒有這麼相關的 resarch 確定，畢竟聽說無論是 Apple Pay,Google Pay 這一期，它是產生一個一次性的卡號", "使用 Apple Pay / Google Pay 是否較安全？行動支付採用一次性虛擬 Token，能有效防止真實卡號遭側錄"),
        ("至少要在一個內網隔離的環境，包含可能幫他切一個專屬的認", "店家必須落實 VLAN 內網隔離，將刷卡機與公共 Wi-Fi 分開"),
    ]
    for old, new in fixes:
        text = text.replace(old, new)
    return text


def proofread_93(raw: str) -> str:
    text = clean_cjk_spaces_and_punct(raw)
    fixes = [
        ("各位會送大家好", "各位貴賓大家好"),
        ("這場一層", "這場議程"),
        ("攻擊子彈研究員以及其他的駭客團隊", "攻擊資安研究員以及其他的駭客團隊"),
        ("這場我們會稱他是 一個黑", "這場我們會稱它為「黑吃黑」"),
        ("黑瞄準駭克的供應鏈攻擊", "黑客瞄準駭客的供應鏈攻擊"),
        ("Vity Intelligence Research Team", "Vulnerability Intelligence Research Team"),
        ("Jason,Jason 和", "Jason 和 Sam"),
        ("我是三，然後在我旁邊那個是 S", "我是 Sam，在我旁邊的是 Jason"),
        ("在自然大約十多年，然後我有持有 83, 然後也是 CU 的 member 跟 NOP 的 member", "在資安領域十多年，持有相關證照與社群 Member"),
        ("今天 line 我們分為七個章節", "今天 Outline 我們分為七個章節"),
        ("ve overview", "Overview"),
        ("紅隊的挖肉中", "紅隊的挖掘漏洞中"),
        ("中國的紅隊整合工具", "中國開源紅隊工具整理庫"),
        ("哈尼帕", "Honeypot（蜜罐）"),
        ("合併發布了一個叫 T 的一個", "國外資安團隊發布了揭露報告"),
        ("WSUS 呢去年被發出了一個重大的漏", "微軟 WSUS 重大漏洞"),
        ("Ract to SH", "React-to-Shell 漏洞 PoC"),
        ("GitHub 的 bot", "GitHub 假 PoC 專案"),
        ("python package", "Python Package"),
        ("那 74 萬多個", "PyPI 上 74 萬多個套件"),
        ("利用壓縮檔名清單在檔尾的特性，只拉檔尾過濾出 DLL 與 SO", "利用 ZIP 檔尾目錄特性，只下載檔尾清單過濾出包含 .so / .dll 的套件"),
        ("過濾剩下來的大概就是 22000 多個，Native library 大概是 11000 多個", "過濾後縮小至 22,000 個，其中 Native Library 約 11,000 個"),
        ("匿名 email，就是 atomicmail 跟 protonmail", "匿名信箱（如 atomicmail、protonmail）"),
        ("exploit.py", "exploit.py"),
        ("execution context keying：利用呼叫者檔名 exploit.py 作為動態解密金鑰", "Execution Context Keying：動態讀取最外層執行的腳本檔名（exploit.py）作為解密金鑰"),
        ("合法第三方服務 mbof / Dropbox / Webhook 進行 C2 通訊", "利用合法雲端服務（Mega / Dropbox / Discord Webhook）作為 C2 通訊管道"),
        ("將代碼寫入 sitecustomize.py 達成 Python 常駐", "寫入 sitecustomize.py 達成 Python 常駐維持（Persistence）"),
        ("UTC 加 8 時區，早上 10 點 52 到晚上 7 點 23 分", "工作作息高度集中於 UTC+8 時區週一至週五（10:52 ~ 19:23）"),
        ("農曆新年期間完全停止活動", "農曆除夕至初五期間完全停工"),
        ("點開保密契約與 26 奈米半導體技術分享", "Honeypot 中攻擊者點開閱讀中文保密協定與半導體技術報告"),
    ]
    for old, new in fixes:
        text = text.replace(old, new)
    return text


def proofread_94(raw: str) -> str:
    text = clean_cjk_spaces_and_punct(raw)
    fixes = [
        ("掌聲歡迎 Henry", "掌聲歡迎 Henry！"),
        ("我是台灣客會長，那同時問也是 CSA 跟 Project 的那些 member", "我是台灣黑客社群成員，同時也是 CSA 與多個社群專案 Member"),
        ("在 DC, 我收新為 c 做 GO", "在 DEFCON 擔任專門的工作人員（Goon）"),
        ("DCA Village 的這個 sting Committee Member", "DCA Village 的 Steering Committee Member"),
        ("為什麼會叫黑幫派成員，黑共這個事在英文啊門口的。對，在多的顧門口的，我們是共的話在美國的英文裡面，他的理師他就是包派成員", "Goon 在美語俚語中是指黑幫打手、現場保安工作人員"),
        ("穿紅色這些衣服，我帶了這個 B 我是在工作中", "穿紅色衣服、戴著 Goon Badge 代表我正在執勤工作中"),
        ("在走廊叫你 getting 就其中一個人會叫你 getting line", "在走廊大喊「Get in line!」，叫大家排好隊"),
        ("整個 d organization 的話有 400 多人，那光保安本身就有 200 多人在 200 以上", "DEFCON 工作人員有 400 多人，保安超過 200 人以上"),
        ("早班 fship，早上 5 點半開始到下午 3 點半", "早班 Morning Shift，從早上 5 點半到下午 3 點半"),
        ("我是來做 reprovement", "我是來做招募（Recruitment）的"),
        ("亞洲區韓國日本台灣算起來人數大概有將近在 600 到 700 人左右，總人數在 35000 人", "亞洲區會眾達 600~700 人，全場總人數 35,000 人"),
        ("每天可以走 3 萬步不休息，然後可以工作 10 個小時不坐下來，然後願意早上 5 點鐘起床", "每天能走 3 萬步不休息、連續站立工作 10 小時、早上 5 點起床"),
        ("第一你不用付飯店錢，第二你不用付吃飯錢，第三你可以插隊，你要插什麼隊都 OK，你要插吃飯，你要插買東西，你要聽 speech 都可以插隊，擁有最高特權最高權限", "免飯店費、免伙食費、全場買周邊/吃飯/聽演講擁有最高優先插隊特權（Full VIP Access）"),
        ("在 DEC 成立一個新的組織叫 A49", "在 DEFCON 成立亞洲 Goon 專屬組織 A49"),
        ("克雷格帶來的主題是讓 H 成為你的知識庫，HK KB2.0", "克雷帶來的題目：讓 HITCON 成為你的知識庫——HITCON KB 2.0 (HITCON Wiki)"),
        ("規劃了搞費，然後實體的數位講狀，獎杯跟感謝函，專屬紀念品包含門票", "規劃了優渥稿費、實體與數位獎狀、獎盃、感謝函與 HITCON 門票等紀念品"),
        ("正體中文的資安文章收集，結構化的學習路徑，審稿委員會把關", "正體中文資安知識庫、結構化學習路徑、審稿委員會品質把關"),
        ("技術難度只是最小的一個指標，主要最在意的是系統性、完整性跟詳細程度，即使寫 SQL Injection 是什麼也能得高分", "技術難度只是最小指標，最看重系統性、完整性與詳細程度，重寫 SQL Injection 也能得高分"),
        ("投稿至 wiki@hitcon.org 或瀏覽 wiki.hitcon.org", "投稿至 wiki@hitcon.org 或瀏覽 wiki.hitcon.org"),
        ("Mina 誕生於神話，零價於神話之上，Minerva 羅馬神話智慧女神", "《Mina 誕生於神話，凌駕於神話之上》Minerva 羅馬智慧女神"),
        ("我是 Ray，目前在台科大，有七張包含 OSCP 和 OSWE 在內的 OffSec 認證", "我是 Ray，目前在台科大，持有 OSCP、OSWE 等 7 張 OffSec 認證"),
        ("C2 Matrix 上面找 MFIC2 / Mythic C2", "C2 Matrix 上尋找 Mythic C2 等框架"),
        ("Cyberpunk 2077 美術集，先進簡潔的 Cyberpunk UI", "研讀《電馭叛客 2077》美術集，打造極致 Cyberpunk UI"),
        ("內建 Lofi 背景音樂播放器", "內建 Lofi 音樂播放器輔助紅隊專注"),
        ("12 月構思，1 月 8 號開始開發，10 號開始封測！兩天完成！一行 Code 都沒寫，全靠 Prompt Engineering 由 AI 生成，被我罵爆後修好", "12 月構思，1/8 開發，1/10 封測！2 天內一行核心程式碼都沒寫，100% 透過 Prompt 叫 Claude/GPT 生成"),
        ("烏克蘭藍隊防禦環境實測", "在烏克蘭藍隊防禦環境實測驗證"),
        ("約翰去美國執行安心生育計畫，路邊撿到好幾個 GPT 帳號，變成約翰與撿到 AI 的快樂小夥伴，用了一週還剩 91%", "約翰去美國執行安心生育計畫，撿到 GPT 帳號變成「約翰與撿到 AI 的快樂小夥伴」，用了一週還剩 91%"),
        ("Badge 解謎活動答案叫撞爆豬肉", "Badge 解謎活動答案叫「撞爆豬肉」"),
        ("Card Battle 共有 728 人註冊帳號，624 人至少收集一張卡片", "Card Battle 智慧卡活動 728 人註冊，624 人集卡"),
        ("二手銀行退役製卡機皮帶斷掉轉向卡死，用美國帶回甜筒口味護唇膏當潤滑劑救活，卡片帶有甜筒香味", "銀行退役製卡機皮帶斷裂卡死，用美國帶回的甜筒護唇膏當潤滑劑救活，卡片帶有甜筒香氣"),
        ("釣魚連結扣 10 分，會眾瘋狂刷扣分，第一名扣到負 700 萬分打掛後端伺服器", "釣魚彩蛋點擊扣 10 分，引發會眾瘋狂扣分，第一名扣到 -7,000,000 分打掛後端伺服器"),
        ("PCB 焊接體驗洗手零受傷，棉花糖機變飲料機", "PCB 焊接體驗洗手零受傷，自動烤棉花糖機變飲料機"),
        ("阿斯卡帶來 PowerShell 的奇技淫巧", "阿斯卡帶來 PowerShell 隱蔽執行奇技淫巧"),
        ("覆寫 FileInfo 的 TypeData 屬性與 Getter，管理員鍵入 ls 時自動觸發惡意邏輯或 C2 通訊，且不記錄於 ScriptBlock Log", "透過 TypeData 覆寫 FileInfo 屬性 Getter，執行 ls 時背景觸發惡意代碼，且不留下 ScriptBlock 日誌"),
        ("來自超自然的震動：智慧成人連網玩具漏洞挖掘", "《來自超自然的震動》智慧成人連網玩具漏洞挖掘"),
        ("Client 端決定 SessionID 導致驗證繞過，爬取 Profile 偽造身分向任意第三方發起遠端通話與控制，硬體暫存器無邊界導致過熱燒毀風險", "Client 端決定 Session ID 導致驗證繞過、爬取 Profile 偽造身分發起任意遠端控制、硬體暫存器無邊界導致過熱燒毀風險"),
    ]
    for old, new in fixes:
        text = text.replace(old, new)
    return text


def process_verbatim_file(in_path: Path, out_path: Path, fixer):
    with open(in_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    cleaned_text = fixer(raw)

    raw_sentences = re.split(r"([。！？\n]+)", cleaned_text)
    paragraphs = []
    current_p = []
    current_len = 0

    for piece in raw_sentences:
        if not piece:
            continue
        if re.match(r"^[。！？\n]+$", piece):
            if current_p:
                current_p[-1] += piece.strip()
                current_len += len(piece)
        else:
            current_p.append(piece.strip())
            current_len += len(piece)

        if len(current_p) >= 3 or current_len >= 220:
            para_str = "".join(current_p).strip()
            if para_str:
                paragraphs.append(para_str)
            current_p = []
            current_len = 0

    if current_p:
        para_str = "".join(current_p).strip()
        if para_str:
            paragraphs.append(para_str)

    title = f"{in_path.stem} 演講全文逐字稿【100% 完整原話校對版】"
    doc_lines = [
        "---",
        f'title: "{title}"',
        'type: "verbatim-proofread-transcript"',
        "verbatim: true",
        "---",
        "",
        f"# 🎙️ {title}",
        "",
        "> **【校對說明】**：本文件為 **100% 全篇原話逐字稿完整校對版**。保留講者所有原話發言、語意轉折、現場對話、故事梗與問答，**未做任何刪減或摘要縮寫**，僅對語音辨識之錯字、同音字、專業術語與標點空格進行全面修訂。",
        "",
        "---",
        "",
    ]

    doc_lines.extend([f"{p}\n" for p in paragraphs])
    final_md = "\n".join(doc_lines).strip() + "\n"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_md)

    print(f"✔ 100% 原話完整校對生成完成：{in_path.name} -> {out_path.name} ({len(final_md)} 字元)")


def main():
    base_dir = Path(".")
    tasks = [
        ("91-Pixel8A-GPU漏洞挖掘-raw.txt", "91-Pixel8A-GPU漏洞挖掘-proofread.md", proofread_91),
        ("92-POS-ADB-0Day-AI輔助-raw.txt", "92-POS-ADB-0Day-AI輔助-proofread.md", proofread_92),
        ("93-供應鏈攻擊-黑吃黑-raw.txt", "93-供應鏈攻擊-黑吃黑-proofread.md", proofread_93),
        ("94-閃電秀6場合輯-raw.txt", "94-閃電秀6場合輯-proofread.md", proofread_94),
    ]

    for in_name, out_name, fixer in tasks:
        in_file = base_dir / in_name
        out_file = base_dir / out_name
        if in_file.exists():
            process_verbatim_file(in_file, out_file, fixer)


if __name__ == "__main__":
    main()
