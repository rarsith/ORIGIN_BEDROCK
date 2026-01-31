@echo off

rem \---- SET_DCC
set "DCC=gaffer"

rem "%ORIGIN_ROOT%\venv\Scripts\python.exe" "%ORIGIN_ROOT%\origin\dcc\%DCC%\startup_gaffer.py"

IF ERRORLEVEL 1 (
    echo Preflight failed. Aborting Gaffer launch.
    pause
    exit /b 1
)

rem \---- Gaffer Installation
set "APP=D:\__REPOSITORIES\Installs\gaffer\gaffer-1.6.10.0-windows"


rem \---- Maya Executable
set "APP_BIN=%APP%\bin"

set "GAFFER_STARTUP_PATHS=%ORIGIN_ROOT%\origin\dcc\extensions\%DCC%\startup;%GAFFER_STARTUP_PATHS%"
set "GAFFER_APP_PATHS=%ORIGIN_ROOT%\origin\dcc\%DCC%\extensions;%GAFFER_APP_PATHS%"
set "PYTHONPATH=%ORIGIN_ROOT%;%ORIGIN_ROOT%\origin\python_shared;%PYTHONPATH%"

"%APP_BIN%\gaffer.cmd"

