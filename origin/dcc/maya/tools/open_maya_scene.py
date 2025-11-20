import importlib
import os
import maya.cmds as cmds

from PySide2.QtWidgets import QFileDialog, QWidget
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler


def clone_environment():
    from origin.dcc import context_env
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)
    return CLONED_CONTEXT


def open_path():
    cloned_env = clone_environment()
    path_ops = OriginOSPathHandler(context=cloned_env)
    work_path_elements = path_ops.work_base_path(as_path=False, abs_path=False)
    work_path_elements.append(path_ops.branch_user_scene_files)
    save_path = path_ops.compose_path(path_elements=work_path_elements, relative=False)
    normalized_path = os.path.normpath(save_path)
    unix_path = normalized_path.replace(os.sep, '/')
    return unix_path


def custom_save_as_dialog(start_directory):
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QWidget)
    file_path, _ = QFileDialog.getSaveFileName(maya_main_window, "Save As", start_directory)
    return file_path


def custom_open_scene_dialog(start_directory):
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    maya_main_window = wrapInstance(int(maya_main_window_ptr), QWidget)

    file_path, _ = QFileDialog.getOpenFileName(
        parent=maya_main_window,
        caption="Open Maya Scene",
        dir=start_directory,
        filter="Maya Files (*.ma *.mb);;All Files (*.*)"
    )

    cmds.file(file_path, open=True, force=True)


def initiate_open_file_dialog():
    open_file_path = open_path()
    custom_open_scene_dialog(start_directory=open_file_path)
