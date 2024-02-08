from PySide2 import QtWidgets, QtCore, QtGui


class ProjectTreeViewerBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ProjectTreeViewerBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setHeaderHidden(True)
        self.expandAll()
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


class ProjectsBoxBuild(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ProjectsBoxBuild, self).__init__(parent)


class ProjectTreeViewerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ProjectTreeViewerUI, self).__init__(parent)
        self.setMinimumWidth(150)
        self.setMaximumWidth(160)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.show_select_cb = ProjectsBoxBuild()
        self.project_tree_viewer_wdg = ProjectTreeViewerBuild()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.show_select_cb)
        main_layout.addWidget(self.project_tree_viewer_wdg)


if __name__ == '__main__':
    import sys
    import pprint

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())
    test_dialog = ProjectTreeViewerUI()
    test_dialog.show()
    sys.exit(app.exec_())