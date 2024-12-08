@echo off
setlocal ENABLEDELAYEDEXPANSION

REM 列出當前路徑內的所有檔案
echo 以下是目前資料夾內的檔案：
set COUNTER=0
for %%f in (*.*) do (
    set /a COUNTER+=1
    echo !COUNTER! - %%f
    set FILE!COUNTER!=%%f
)
echo -------------------------------------------------------
set /p SELECT=請輸入序號來選擇主要程式檔案(例如1): 

REM 檢查輸入是否合法
if not defined FILE%SELECT% (
    echo 無效的序號，程式將結束。
    pause
    exit /b
)

REM 獲取主要程式檔案
set MAINPG=!FILE%SELECT%!
echo 已選擇主要程式檔案: %MAINPG%

REM 問使用者參數
set /p PARAM=請輸入要使用的參數(預設為?data=): 

REM 如果參數為空，使用預設值
if "%PARAM%"=="" (
    set PARAM=?data=
    echo 使用預設參數: %PARAM%
)

REM 問使用者是否需要加上前置網址
set /p URL=請貼上前置網址 (可跳過): 

echo.
echo 以下為即將生成的資料列：
echo [前置網址+主要程式+參數+原檔名],[檔名(無副檔名)]
echo -------------------------------------------------------
(
for %%f in (*.*) do (
    if /I "%%f" neq "%MAINPG%" if /I "%%f" neq "%~nx0" if /I "%%f" neq "output.csv" (
        REM 取得不含副檔名的檔名前綴
        set FNAME=%%~nf
        REM 如果使用者輸入了前置網址，則加上
        if not "%URL%"=="" (
            echo %URL%%MAINPG%%PARAM%%%f,!FNAME!
        ) else (
            echo %MAINPG%%PARAM%%%f,!FNAME!
        )
    )
)
)
echo -------------------------------------------------------

REM 詢問是否要輸出成CSV
set /p EXPORT=是否要輸出為csv檔? (Y/N): 

if /I "%EXPORT%"=="Y" (
    REM 輸出為csv檔，排除 output.csv 並加上前置網址（若有）
    (
    for %%f in (*.*) do (
        if /I "%%f" neq "%MAINPG%" if /I "%%f" neq "%~nx0" if /I "%%f" neq "output.csv" (
            set FNAME=%%~nf
            if not "%URL%"=="" (
                echo %URL%%MAINPG%%PARAM%%%f,!FNAME!
            ) else (
                echo %MAINPG%%PARAM%%%f,!FNAME!
            )
        )
    )
    )>output.csv
    echo 已生成 output.csv 檔案，內容已加上前置網址（若有）。
) else (
    echo 未輸出檔案，程式結束。
)

pause
