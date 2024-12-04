@echo off
chcp 950 >nul
setlocal enabledelayedexpansion

:: �ˬd�O�_�w�ˤF Pandoc
where pandoc >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==============================================
    echo [���~] �������� Pandoc �{���C
    echo �Ыe���H�U���}�U���æw�� Pandoc�G
    echo https://github.com/jgm/pandoc/releases
    echo ==============================================
    echo.
    pause
    exit /b
)

echo �}�l�ഫ .md �ɮ׬� .pptx �ɮסA���M�Υ���ҪO�C
echo.

:: �j��B�z�Ҧ� .md �ɮ�
for %%f in (*.md) do (
    set "filename=%%~nf"
    echo ���b�ഫ�ɮסG"%%f" �� "!filename!.pptx"
    echo ����R�O�Gpandoc "%%f" -o "!filename!.pptx"
    pandoc "%%f" -o "!filename!.pptx"
    echo.
)

echo �Ҧ��ɮפw�ഫ�����I
pause
