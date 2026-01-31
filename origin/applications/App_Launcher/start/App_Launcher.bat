rem python C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\origin\applications\App_Launcher\App_Laucher.py

@echo off
setlocal

set DCC=origin_standalone

REM === CONFIG ===
set APP_DIR=%ORIGIN_ROOT%\origin\applications\App_Launcher
set PYTHON_EXE=%ORIGIN_ROOT%\venv\Scripts\python.exe
set APP_SCRIPT=App_Launcher.py

set PYTHONPATH=%ORIGIN_ROOT%

REM === MOVE TO APP DIRECTORY ===
cd /d "%APP_DIR%"

REM === RUN APPLICATION ===
"%PYTHON_EXE%" "%APP_DIR%\%APP_SCRIPT%"

REM === KEEP WINDOW OPEN ===
echo.
echo Application exited with code %ERRORLEVEL%

endlocal


