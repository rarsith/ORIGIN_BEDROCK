import sys
import importlib
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore
from origin.envars.origin_envars import ContextHandler

from origin.ui.loaders_ui import loader_ui
importlib.reload(loader_ui)

from origin.dcc.maya import context_env
importlib.reload(context_env)

NEW_CONTEXT = context_env.CURRENT_SESSION.snapshot_session()
CLONED_CONTEXT = ContextHandler()
CLONED_CONTEXT.load_session(NEW_CONTEXT)
CLONED_CONTEXT.reset_to_entity()


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


context_window_parent = get_maya_main_window()
qss_style_file = "C:\\Users\\arsithra\\PycharmProjects\\ORIGIN_BEDROCK\\origin\\ui\\style\\stylesheets\\dark_orange\\dark_orange_style.qss"
window = loader_ui.LoaderMainUI(context=CLONED_CONTEXT, parent=context_window_parent)

try:

    window.setGeometry(100, 100, 700, 300)
    window.setWindowFlags(QtCore.Qt.Window)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        window.setStyleSheet(_style)

    # window.show()

except Exception as e:
    print(f"Error occurred: {e}")