import os
from pathlib import Path


def get_executable(options):
    dcc = options['dcc']
    batch_executables = {
        "maya": "mayapy.exe",
        "houdini": "houdini.exe",
        "blender": "blender.exe",
        "gaffer": "gaffer.cmd"
    }

    return batch_executables.get(dcc)


def set_executable(options):
    dcc_executable = get_executable(options)
    app_bin = Path(options['app_bin'])

    app_py_executable = app_bin / dcc_executable
    app_py_normalized = app_py_executable.as_posix()
    return app_py_normalized