import sys
from node_graph import node_editor_wnd
# from PySide2.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = node_editor_wnd.NodeEditorWnd()
    sys.exit(app.exec_())