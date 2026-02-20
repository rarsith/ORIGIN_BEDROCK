import importlib
import os

from PySide2.QtWidgets import QFileDialog, QWidget
import maya.OpenMayaUI as omui
import maya.cmds as cmds
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


def saving_path():
    cloned_env = clone_environment()
    path_ops = OriginOSPathHandler(context=cloned_env)
    unix_path = path_ops.get_user_scene_files()
    return unix_path


def custom_save_as(start_dir):
    path = cmds.fileDialog2(fileMode=0,
                            startingDirectory = start_dir,
                            caption="Save Scene As (Custom)")

    if not path:
        return

    cmds.file(rename=path[0])
    cmds.file(save=True)


def initiate_save_as_dialog():
    save_path = saving_path()
    custom_save_as(start_dir=save_path)
