#!/usr/bin/env bash
# Git pre-commit hook enforcing PROOFREAD_RULES.md, session atomicity, speaker turns, and catalog sync

echo "================================================================"
echo "🔍 [Pre-Commit] 正在執行提交前自動守門測試與規則檢查..."
echo "================================================================"

# 1. 執行核心格式、主題原子性、講者多樣性與侑宸實體防護測試
echo "▶ 步驟 1/2: 執行主題拆分、講者輪次與逐字稿規範測試 (pytest)..."
python -m pytest tests/test_session_atomicity_and_speaker_turn.py tests/test_proofread_linter.py -q
PYTEST_EXIT=$?

if [ $PYTEST_EXIT -ne 0 ]; then
    echo -e "\033[31m❌ [Pre-Commit 阻斷] 測試失敗！\033[0m"
    echo -e "\033[31m   檢測到偽單一講者壓平、多主題未拆分、侑宸實體錯字或摘要套版問題，已中止提交！\033[0m"
    echo "   請修正違規檔案後再重新嘗試 git commit。"
    exit 1
fi

# 2. 執行全庫配對、音檔生命週期與 CATALOG 雙語目錄自檢
echo "▶ 步驟 2/2: 執行全庫 1:1 配對、音檔生命週期與目錄同步檢查 (self_check)..."
python scripts/self_check.py
SELF_CHECK_EXIT=$?

if [ $SELF_CHECK_EXIT -ne 0 ]; then
    echo -e "\033[31m❌ [Pre-Commit 阻斷] 全庫整體驗證失敗！\033[0m"
    echo -e "\033[31m   檢測到孤兒檔案、破損連結或目錄未同步，已中止提交！\033[0m"
    exit 1
fi

echo -e "\033[32m✅ [Pre-Commit 通過] 所有測試與規範檢查全數通過，准予提交！\033[0m"
echo "================================================================"
exit 0
