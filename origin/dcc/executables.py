import os
from pathlib import Path



def get_executable():
    dcc = os.getenv("DCC")
    batch_executables = {
        "maya": "mayapy.exe",
        "houdini": "houdini.exe",
        "blender": "blender.exe",
    }

    return batch_executables.get(dcc)


def set_executable():
    dcc_executable = get_executable()
    app_bin = Path(os.getenv("APP_BIN"))

    app_py_executable = app_bin / dcc_executable
    app_py_normalized = app_py_executable.as_posix()
    return app_py_normalized