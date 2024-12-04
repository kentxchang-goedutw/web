@echo off
chcp 950 >nul
setlocal enabledelayedexpansion

:: 檢查是否安裝了 Pandoc
where pandoc >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==============================================
    echo [錯誤] 未偵測到 Pandoc 程式。
    echo 請前往以下網址下載並安裝 Pandoc：
    echo https://github.com/jgm/pandoc/releases
    echo ==============================================
    echo.
    pause
    exit /b
)

echo 開始轉換 .md 檔案為 .pptx 檔案，不套用任何模板。
echo.

:: 迴圈處理所有 .md 檔案
for %%f in (*.md) do (
    set "filename=%%~nf"
    echo 正在轉換檔案："%%f" 為 "!filename!.pptx"
    echo 執行命令：pandoc "%%f" -o "!filename!.pptx"
    pandoc "%%f" -o "!filename!.pptx"
    echo.
)

echo 所有檔案已轉換完成！
pause
