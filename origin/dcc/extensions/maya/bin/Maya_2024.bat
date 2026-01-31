@echo off


rem \---- SET_DCC
set "DCC=maya"

rem \---- Maya Installation
set "APP=D:\Program Files\Autodesk\Maya2024"

rem \---- Maya Executable
set "APP_BIN=%APP%\bin"

set "USD_INSTALL_DIR=%APP%\USD"

set "PATH=%USD_INSTALL_DIR%\bin;%APP_BIN%;%PATH%"

rem \---- Python paths
set "PYTHONPATH=%ORIGIN_ROOT%;%USD_INSTALL_DIR%\lib\python;%ORIGIN_ROOT%\origin\dcc\extensions\%DCC%;%PYTHONPATH%"

rem ---- Construct the Python command string
set "PY_CMD=import os; exec(open(os.path.join(os.getenv('ORIGIN_ROOT'), 'origin/dcc/extensions/%DCC%/bin/startup/startup_maya.py')).read())"

"%APP_BIN%\maya.exe" -command "python(\"%PY_CMD%\")"
