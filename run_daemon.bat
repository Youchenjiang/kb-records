@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ======================================================================
echo    自動語音轉錄守護程序 (Auto-Transcribe Daemon)
echo    - GPU 環境：recording-transcribe-gpu (Qwen3-ASR-1.7B)
echo    - 支援中斷接續、崩潰自動重啟、隊列自動移動 (Processed)
echo    - 按 Ctrl+C 即可中斷退出
echo ======================================================================
echo.

set CONDA_ENV=C:\MyAPP\Anaconda3\envs\recording-transcribe-gpu

if exist "%CONDA_ENV%\python.exe" (
    set PYTHON_EXEC=%CONDA_ENV%\python.exe
) else (
    set PYTHON_EXEC=python
)

:LOOP
echo [%DATE% %TIME%] 正在檢查並執行轉錄隊列...
"%PYTHON_EXEC%" scripts\auto_transcribe_daemon.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [%DATE% %TIME%] 轉錄程序退出 (Exit code: %ERRORLEVEL%)，5 秒後自動重啟接續...
    timeout /t 5 /nobreak >nul
    goto LOOP
)

echo.
echo [%DATE% %TIME%] 所有隊列音檔已轉錄完成！守護行程保持監聽...
timeout /t 15 /nobreak >nul
goto LOOP
