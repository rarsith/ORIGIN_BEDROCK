@echo off

rem \---- Codebase Root
set "ORIGIN_ROOT=C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK"

rem \---- Blender Installation
set "BLENDER_ROOT=D:\Program Files\Blender Foundation\Blender 4.3\"

rem \---- Put Blender on the PATH
set "PATH=%PATH%;%BLENDER_ROOT%"

rem \---- Python paths
set PYTHONPATH=%ORIGIN_ROOT%;%PYTHONPATH%

rem \---- PROJECTS_ROOT
set "ORIGIN_PROJECTS_ROOT=D:\___MY_APP_PROJECTS___\Origin_Projects"

rem \---- SET_DCC
set "DCC=blender"

"%BLENDER_ROOT%\\blender.exe" --python "C:/Users/arsithra/PycharmProjects/ORIGIN_BEDROCK/origin/dcc/blender/startup_blender.py"
