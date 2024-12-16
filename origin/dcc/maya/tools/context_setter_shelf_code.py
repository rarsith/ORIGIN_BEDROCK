import importlib
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore
from origin.dcc.maya.context_env import CURRENT_SESSION

from origin.ui.context_manager_ui import context_manager_ui

importlib.reload(context_manager_ui)


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


if __name__ == "__main__":
    import sys

    context_window_parent = get_maya_main_window()
    qss_style_file = "C:\\Users\\arsithra\\PycharmProjects\\ORIGIN_BEDROCK\\origin\\ui\\style\\stylesheets\\dark_orange\\dark_orange_style.qss"

    try:
        window = context_manager_ui.ContextManagerMainUI(parent=context_window_parent)
        window.setGeometry(100, 100, 700, 300)  # Set position and size
        window.setWindowFlags(QtCore.Qt.Window)  # Ensure it's treated as a window

        with open(qss_style_file, "r") as f:
            _style = f.read()
            window.setStyleSheet(_style)

        window.show()


    except Exception as e:
        print(f"Error occurred: {e}")