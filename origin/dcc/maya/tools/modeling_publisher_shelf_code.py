import importlib
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore

from origin.ui.publish import origin_publisher

importlib.reload(origin_publisher)

from origin.dcc.maya import context_env

importlib.reload(context_env)

NEW_CONTEXT = context_env.CURRENT_SESSION.snapshot_session()
CLONED_CONTEXT = ContextHandler()
CLONED_CONTEXT.load_session(NEW_CONTEXT)


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)


if __name__ == "__main__":
    import sys

    context_window_parent = get_maya_main_window()
    qss_style_file = "C:\\Users\\arsithra\\PycharmProjects\\ORIGIN_BEDROCK\\origin\\ui\\style\\stylesheets\\dark_orange\\dark_orange_style.qss"

    target_root = "main|geo"

    if not cmds.objExists(target_root):
        raise Exception(f"Hierachy Imcomplete. {target_root} not found. Use Create Template!")

    elif not CLONED_CONTEXT.task_type == "modeling":
        raise Exception(f"Task missmatch. You are in {CLONED_CONTEXT.task_type} Task!")

    else:

        try:
            window = origin_publisher.OriginPublisher(context=CLONED_CONTEXT, publish_type="geometry",
                                                      parent=context_window_parent)
            window.setGeometry(100, 100, 700, 300)  # Set position and size
            window.setWindowFlags(QtCore.Qt.Window)  # Ensure it's treated as a window

            with open(qss_style_file, "r") as f:
                _style = f.read()
                window.setStyleSheet(_style)

            window.show()


        except Exception as e:
            print(f"Error occurred: {e}")