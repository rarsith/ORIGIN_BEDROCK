import importlib
import os

import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore
from origin.envars.origin_envars import ContextHandler
from origin.dcc.maya.post_startup_maya import set_origin_maya
from origin.dcc.maya.startup_maya import set_current_working_directory

from origin.ui.context_manager_ui import context_manager_ui
importlib.reload(context_manager_ui)


def clone_environment():
    from origin.dcc.maya import context_env
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)
    return CLONED_CONTEXT


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


def context_setter():
    current_context = clone_environment()
    context_window_parent = get_maya_main_window()

    origin_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

    window = context_manager_ui.ContextManagerMainUI(parent=context_window_parent)

    try:

        window.setGeometry(100, 100, 700, 300)  # Set position and size
        window.setWindowFlags(QtCore.Qt.Window)  # Ensure it's treated as a window

        window.central_widget.submit_pressed.connect(set_origin_maya)
        window.central_widget.submit_pressed.connect(set_current_working_directory)

        with open(qss_style_file, "r") as f:
            _style = f.read()
            window.setStyleSheet(_style)

        window.show()

    except Exception as e:
        print(f"Error occurred: {e}")