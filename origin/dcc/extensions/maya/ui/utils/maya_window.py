import maya.OpenMayaUI as omui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)