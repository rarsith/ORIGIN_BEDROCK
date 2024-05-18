from PySide2 import QtWidgets, QtCore, QtGui


class ProjectTreeViewerBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ProjectTreeViewerBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setHeaderHidden(True)
        # self.expandAll()
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setFocusPolicy(QtCore.Qt.NoFocus)


class ProjectsBoxBuild(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ProjectsBoxBuild, self).__init__(parent)


class ProjectTreeViewerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ProjectTreeViewerUI, self).__init__(parent)
        # self.setMinimumWidth(200)
        # self.setMaximumWidth(220)
        self.setContentsMargins(2,2,2,2)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.create_project_btn = QtWidgets.QPushButton("New Project")
        self.create_project_btn.setFixedWidth(70)
        # self.create_project_btn.setMinimumWidth(50)
        # self.create_project_btn.setMaximumWidth(200)


        self.show_select_cb = ProjectsBoxBuild()
        self.project_tree_viewer_wdg = ProjectTreeViewerBuild()

    def create_layout(self):
        select_proj_layout = QtWidgets.QHBoxLayout()
        select_proj_layout.addWidget(self.show_select_cb)
        select_proj_layout.addWidget(self.create_project_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(select_proj_layout)
        main_layout.addWidget(self.project_tree_viewer_wdg)



if __name__ == '__main__':
    import sys
    import pprint

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())
    test_dialog = ProjectTreeViewerUI()
    test_dialog.show()
    sys.exit(app.exec_())