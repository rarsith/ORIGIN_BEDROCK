import os
import importlib
import maya.cmds as cmds
from PySide2 import QtCore
from origin.dcc.common.utils.context_from_envar import clone_environment
from origin.dcc.extensions.maya.ui.utils.maya_window import get_maya_main_window
from origin.ui.publish import origin_publisher
importlib.reload(origin_publisher)

#
# def strip_namespaces(target_namespaces: list):
#       # List all namespaces
#     for ns in target_namespaces:
#         if ns not in [':', 'UI']:  # Ignore root and default namespaces
#             cmds.namespace(set=ns)
#             objects = cmds.namespaceInfo(ns, listNamespaceContents=True, dagPath=True)
#             for obj in objects:
#                 new_name = obj.split(':')[-1]  # Take only the base name
#                 cmds.rename(obj, new_name)
#             cmds.namespace(set=':')
#             # cmds.namespace(removeNamespace=ns)
#
# strip_namespaces()


def publish():
    current_context = clone_environment()
    context_window_parent = get_maya_main_window()

    origin_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

    target_root = "turntable_camera:camera"
    if not cmds.objExists(target_root):
        raise Exception(f"Hierachy Imcomplete. {target_root} not found. Use Create Template!")

    # elif not current_context.task_type == "modeling":
    #     raise Exception(f"Task missmatch. You are in {current_context.task_type} Task!")

    else:
        window = origin_publisher.OriginPublisher(context=current_context, publish_type="turntable_camera", parent=context_window_parent)
        try:

            window.setGeometry(100, 100, 700, 300)
            window.setWindowFlags(QtCore.Qt.Window)

            with open(qss_style_file, "r") as f:
                _style = f.read()
                window.setStyleSheet(_style)

            window.show()

        except Exception as e:
            print(f"Error occurred: {e}")