@echo off
setlocal ENABLEDELAYEDEXPANSION

REM �C�X��e���|�����Ҧ��ɮ�
echo �H�U�O�ثe��Ƨ������ɮסG
set COUNTER=0
for %%f in (*.*) do (
    set /a COUNTER+=1
    echo !COUNTER! - %%f
    set FILE!COUNTER!=%%f
)
echo -------------------------------------------------------
set /p SELECT=�п�J�Ǹ��ӿ�ܥD�n�{���ɮ�(�Ҧp1): 

REM �ˬd��J�O�_�X�k
if not defined FILE%SELECT% (
    echo �L�Ī��Ǹ��A�{���N�����C
    pause
    exit /b
)

REM ����D�n�{���ɮ�
set MAINPG=!FILE%SELECT%!
echo �w��ܥD�n�{���ɮ�: %MAINPG%

REM �ݨϥΪ̰Ѽ�
set /p PARAM=�п�J�n�ϥΪ��Ѽ�(�w�]��?data=): 

REM �p�G�ѼƬ��šA�ϥιw�]��
if "%PARAM%"=="" (
    set PARAM=?data=
    echo �ϥιw�]�Ѽ�: %PARAM%
)

REM �ݨϥΪ̬O�_�ݭn�[�W�e�m���}
set /p URL=�жK�W�e�m���} (�i���L): 

echo.
echo �H�U���Y�N�ͦ�����ƦC�G
echo [�e�m���}+�D�n�{��+�Ѽ�+���ɦW],[�ɦW(�L���ɦW)]
echo -------------------------------------------------------
(
for %%f in (*.*) do (
    if /I "%%f" neq "%MAINPG%" if /I "%%f" neq "%~nx0" if /I "%%f" neq "output.csv" (
        REM ���o���t���ɦW���ɦW�e��
        set FNAME=%%~nf
        REM �p�G�ϥΪ̿�J�F�e�m���}�A�h�[�W
        if not "%URL%"=="" (
            echo %URL%%MAINPG%%PARAM%%%f,!FNAME!
        ) else (
            echo %MAINPG%%PARAM%%%f,!FNAME!
        )
    )
)
)
echo -------------------------------------------------------

REM �߰ݬO�_�n��X��CSV
set /p EXPORT=�O�_�n��X��csv��? (Y/N): 

if /I "%EXPORT%"=="Y" (
    REM ��X��csv�ɡA�ư� output.csv �å[�W�e�m���}�]�Y���^
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
    echo �w�ͦ� output.csv �ɮסA���e�w�[�W�e�m���}�]�Y���^�C
) else (
    echo ����X�ɮסA�{�������C
)

pause
