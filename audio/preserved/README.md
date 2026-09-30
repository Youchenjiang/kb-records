# 🛡️ Preserved Audio Quarantine (非人聲／純音樂待遷移保留區)

本目錄專門存放 **非課程演講、非人聲研討、純音樂（如鋼琴曲、背景音樂）、或使用者指定保留** 之音訊檔案。

## ⚠️ 重要保護機制
1. **防止自動清除**：`python -m transcript_processor audio clean` 指令 **絕對不會清除本目錄檔案**。
2. **遷移專用**：本目錄檔案為暫存隔離，供使用者方便整批遷移至外部儲存空間或個人音樂媒體庫。
3. **隔離清冊**：每次透過 `audio preserve` 隔離音訊時，系統將自動於 [`MANIFEST.md`](./MANIFEST.md) 紀錄隔離檔案與原因。
