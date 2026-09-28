# 🎙️ 音訊檔案工作目錄與生命週期管理

本目錄為本專案存放錄音媒體檔案（`.aac`, `.mp3`, `.m4a`, `.wav` 等）的工作區。
**所有二進位音訊檔案均已被 `.gitignore` 全局排除，不會納入 Git 版本控制，以維持儲存庫精簡。**

---

## 🗂️ 目錄架構

```text
audio/
├── pending/       # 📥 待處理音檔（未轉錄 / 辨識中，暫時保留勿刪）
└── processed/     # 📦 已處理音檔（雙版本產物已交付完成，確認無誤後可隨時刪除釋放空間）
```

---

## 🔄 音檔生命週期與標準工作流

1. **置入錄音**：
   * 將新取得的會議或演講錄音放入 `audio/pending/`。
   * 此時音檔處於「待辨識」狀態，請勿刪除。

2. **ASR 轉錄與校對**：
   * 執行 ASR 模型（如 Qwen3-ASR 或 Whisper）進行音訊切片轉錄。
   * 產出初步文字稿，並依照 `PROOFREAD_RULES.md` 進行逐字稿校對與摘要生成。

3. **轉移至已處理（歸檔 / 可刪除）**：
   * 當對應的雙交付產物（`proofread.md` 與 `summary.md`）完成並驗證通過後，將音檔自 `audio/pending/` 移至 `audio/processed/`。
   * 可透過專案內建指令操作：
     ```bash
     python -m transcript_processor audio finish "錄音檔名.aac"
     ```

4. **磁碟空間清理**：
   * 當確認轉錄與校對皆完整無缺，需要釋放硬碟空間時，可安全清空 `audio/processed/`：
     ```bash
     python -m transcript_processor audio clean --yes
     # 或使用 PowerShell
     Remove-Item audio/processed/*.aac
     ```
