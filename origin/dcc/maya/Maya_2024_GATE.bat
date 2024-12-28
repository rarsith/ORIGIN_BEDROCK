@echo off

rem \---- Codebase Root
rem set "ORIGIN_ROOT=E:\Local_projects\PycharmProjects\ORIGIN_BEDROCK"

rem \---- Maya Installation
set "MAYA=E:\programs\Autodesk\Maya2024"

rem \---- Maya Executable
set "MAYABIN=%MAYA%\bin"

set "USD_INSTALL_DIR=%MAYA%\USD"

set "PATH=%USD_INSTALL_DIR%\bin;%MAYABIN%;%PATH%"

rem \---- Python paths
set "PYTHONPATH=%ORIGIN_ROOT%;%USD_INSTALL_DIR%\lib\python;%ORIGIN_ROOT%\origin\dcc\maya;%PYMONGO_SITE%;%PYTHONPATH%"


rem \---- SET_DCC
set "DCC=maya"

rem ---- Construct the Python command string
set "PY_CMD=import os; exec(open(os.path.join(os.getenv('ORIGIN_ROOT'), 'origin/dcc/maya/startup_maya.py')).read())"

"%MAYABIN%\maya.exe" -command "python(\"%PY_CMD%\")"

