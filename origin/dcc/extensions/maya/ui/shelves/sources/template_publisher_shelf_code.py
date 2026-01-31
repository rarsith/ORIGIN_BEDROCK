import importlib
import os

import maya.cmds as cmds
from PySide2 import QtCore

from origin.dcc.common.utils.context_from_envar import clone_environment
from origin.dcc.extensions.maya.ui.utils.maya_window import get_maya_main_window

from origin.ui.publish import origin_publisher
importlib.reload(origin_publisher)


def start_publish():
    current_context = clone_environment()
    context_window_parent = get_maya_main_window()

    origin_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

    target_root = "main|template"
    if not cmds.objExists(target_root):
        raise Exception(f"Hierachy Imcomplete. {target_root} not found. Use Create Template :)!")

    elif not current_context.task_type == "template":
        raise Exception(f"Task missmatch. You are in {current_context.task_type} Task!")

    else:
        window = origin_publisher.OriginPublisher(context=current_context, publish_type="template", parent=context_window_parent)
        try:
            window.setGeometry(100, 100, 700, 300)  # Set position and size
            window.setWindowFlags(QtCore.Qt.Window)  # Ensure it's treated as a window

            with open(qss_style_file, "r") as f:
                _style = f.read()
                window.setStyleSheet(_style)

            window.show()

        except Exception as e:
            print(f"Error occurred: {e}")
