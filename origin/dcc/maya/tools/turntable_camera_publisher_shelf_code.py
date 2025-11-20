import os
import importlib
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore
from origin.envars.origin_envars import ContextHandler
from origin.ui.publish import origin_publisher
importlib.reload(origin_publisher)


def clone_environment():
    from origin.dcc import context_env
    importlib.reload(context_env)

    NEW_CONTEXT = context_env.get_context_env()
    CLONED_CONTEXT = ContextHandler()
    CLONED_CONTEXT.load_session(NEW_CONTEXT)
    return CLONED_CONTEXT


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)

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

    target_root = "turntable_camera:cam1"
    context_window_parent = get_maya_main_window()

    origin_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

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