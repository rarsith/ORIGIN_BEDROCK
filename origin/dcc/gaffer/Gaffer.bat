@echo off

rem \---- SET_DCC
set "DCC=gaffer"

rem \---- Gaffer Installation
set "APP=D:\__REPOSITORIES\Installs\gaffer\gaffer-1.6.5.0-windows"


rem \---- Maya Executable
set "APP_BIN=%APP%\bin"

set "GAFFER_STARTUP_PATHS=%ORIGIN_ROOT%\origin\dcc\%DCC%\startup;%GAFFER_STARTUP_PATHS%"
set "GAFFER_APP_PATHS=%ORIGIN_ROOT%\origin\dcc\%DCC%\extensions;%GAFFER_APP_PATHS%"
set "PYTHONPATH=%ORIGIN_ROOT%;%PYTHONPATH%"

"%APP_BIN%\gaffer.cmd"

