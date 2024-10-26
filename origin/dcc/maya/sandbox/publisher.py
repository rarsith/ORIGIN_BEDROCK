import importlib
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore
from origin.dcc.maya.context_env import CURRENT_SESSION

from origin.ui.publish import origin_publisher
importlib.reload(origin_publisher)

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QMainWindow)
    
if __name__ == "__main__":
    import sys

    # curr_stream = "lidar_pop"

    context_window_parent = get_maya_main_window()
    
    try:
        window = origin_publisher.OriginPublisher(context=CURRENT_SESSION, parent=context_window_parent)
        window.setGeometry(100, 100, 700, 300)  # Set position and size
        window.setWindowFlags(QtCore.Qt.Window)  # Ensure it's treated as a window
        window.show()
        print("Showing window...")
        
    except Exception as e:
        print(f"Error occurred: {e}")