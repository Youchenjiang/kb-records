# PowerShell Auto-Transcribe Daemon Runner
$ErrorActionPreference = "Continue"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   自動語音轉錄守護程序 (Auto-Transcribe Daemon)" -ForegroundColor Cyan
Write-Host "   - GPU 環境：recording-transcribe-gpu (Qwen3-ASR-1.7B)" -ForegroundColor Cyan
Write-Host "   - 支援中斷接續、崩潰自動重啟、隊列自動移動 (Processed)" -ForegroundColor Cyan
Write-Host "   - 按 Ctrl+C 即可中斷退出" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$condaPython = "C:\MyAPP\Anaconda3\envs\recording-transcribe-gpu\python.exe"
if (Test-Path $condaPython) {
    $pythonExec = $condaPython
} else {
    $pythonExec = "python"
}

while ($true) {
    $timeStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timeStr] 正在檢查並執行轉錄隊列..." -ForegroundColor Green
    
    & $pythonExec "scripts\auto_transcribe_daemon.py"
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        $timeStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host ""
        Write-Host "[$timeStr] 轉錄程序退出 (Exit code: $exitCode)，5 秒後自動重啟接續..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    } else {
        $timeStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host ""
        Write-Host "[$timeStr] 所有隊列音檔已轉錄完成！守護行程保持監聽..." -ForegroundColor Green
        Start-Sleep -Seconds 15
    }
}
