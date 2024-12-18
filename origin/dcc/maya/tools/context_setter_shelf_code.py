import importlib
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore
from origin.envars.origin_envars import ContextHandler
from origin.dcc.maya.post_startup_maya import set_origin_maya

from origin.ui.context_manager_ui import context_manager_ui
importlib.reload(context_manager_ui)

from origin.dcc.maya import context_env
importlib.reload(context_env)

NEW_CONTEXT = context_env.CURRENT_SESSION.snapshot_session()
CLONED_CONTEXT = ContextHandler()
CLONED_CONTEXT.load_session(NEW_CONTEXT)


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


context_window_parent = get_maya_main_window()
qss_style_file = "C:\\Users\\arsithra\\PycharmProjects\\ORIGIN_BEDROCK\\origin\\ui\\style\\stylesheets\\dark_orange\\dark_orange_style.qss"
window = context_manager_ui.ContextManagerMainUI(parent=context_window_parent)

try:

    window.setGeometry(100, 100, 700, 300)  # Set position and size
    window.setWindowFlags(QtCore.Qt.Window)  # Ensure it's treated as a window

    window.central_widget.submit_pressed.connect(set_origin_maya)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        window.setStyleSheet(_style)

    window.show()


except Exception as e:
    print(f"Error occurred: {e}")