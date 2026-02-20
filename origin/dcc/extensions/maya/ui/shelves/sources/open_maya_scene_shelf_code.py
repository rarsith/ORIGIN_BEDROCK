import importlib
import os
import maya.cmds as cmds

from PySide2.QtWidgets import QFileDialog, QWidget
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler


def clone_environment():
    from origin.dcc.common.utils import context_env
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)
    return CLONED_CONTEXT


def open_path():
    cloned_env = clone_environment()
    path_ops = OriginOSPathHandler(context=cloned_env)
    unix_path = path_ops.get_user_scene_files()
    return unix_path


def custom_open(start_dir):
    path = cmds.fileDialog2(fileMode=1,
                            startingDirectory = start_dir,
                            caption="Open Scene (Custom)")

    if not path:
        return

    path = path[0]

    if cmds.file(q=True, modified=True):
        result = cmds.confirmDialog(
            title="Unsaved Changes",
            message="Save changes before opening?",
            button=["Save", "Don't Save", "Cancel"],
            defaultButton="Save",
            cancelButton="Cancel"
        )

        if result == "Cancel":
            return
        elif result == "Save":
            cmds.file(save=True)

    cmds.file(path, o=True, force=True)


def initiate_open_file_dialog():
    open_file_path = open_path()
    custom_open(start_dir=open_file_path)
