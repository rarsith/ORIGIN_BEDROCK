::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCqDJHWL90M8FwtGQw6HP3+pOoUF6+D6/ee3sEIXUeEra7P06J2pCc4syGDAR7kO/UZVisILBRVkdxGkYBwIpnxLsW2LCNOOshbeQ0uG6FgMFHd9gGresz8pYcpXjJNThG63/0Kf
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSjk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCqDJHWL90M8FwtGQw6HP3+pOoUF6+D6/ee3sEIXUeEra7P06J2pCc4syGDAR7kO/UZVisILBRVkfBulUgAmoGlLuCqAL8L8
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off


set BATCH_PATH=%~dp0

cd /d %BATCH_PATH%..\.. 

set ORIGIN_ROOT=%CD%

echo ORIGIN_ROOT is set to: %ORIGIN_ROOT%

cd /d %ORIGIN_ROOT%

set PYTHONPATH=%PYTHONPATH%;%ORIGIN_ROOT%

call %ORIGIN_ROOT%\.venv\Scripts\activate.bat
python %ORIGIN_ROOT%\origin\sys_tray\origin_tray.py

REM deactivate



REM "E:\Local_projects\PycharmProjects\ORIGIN_BEDROCK\.venv\Scripts\python.exe" "E:\Local_projects\PycharmProjects\ORIGIN_BEDROCK\origin\sys_tray\origin_tray.py"