import importlib
import os

import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore
from origin.envars.origin_envars import ContextHandler

from origin.ui.publish import origin_publisher
importlib.reload(origin_publisher)


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


def rigging_publish():
    current_context = clone_environment()

    origin_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

    target_root = "main|rig"
    context_window_parent = get_maya_main_window()

    if not cmds.objExists(target_root):
        raise Exception(f"Hierachy Imcomplete. {target_root} not found. Use Create Template!")

    elif not current_context.task_type == "rigging":
        raise Exception(f"Task missmatch. You are in {current_context.task_type} Task!")

    else:
        window = origin_publisher.OriginPublisher(context=current_context, publish_type="animation_rig", parent=context_window_parent)
        try:
            window.setGeometry(100, 100, 700, 300)  # Set position and size
            window.setWindowFlags(QtCore.Qt.Window)  # Ensure it's treated as a window

            with open(qss_style_file, "r") as f:
                _style = f.read()
                window.setStyleSheet(_style)

            window.show()

        except Exception as e:
            print(f"Error occurred: {e}")
