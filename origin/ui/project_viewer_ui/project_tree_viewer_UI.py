from PySide2 import QtWidgets, QtCore, QtGui
from origin.ui.style.icons import OriginIcons
from origin.ui.style import buttons_styles as btns


class ProjectTreeViewerBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ProjectTreeViewerBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setHeaderHidden(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setSortingEnabled(True)


class ProjectsBoxBuild(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(ProjectsBoxBuild, self).__init__(parent)
        self.setObjectName("ProjectsBoxBuild")


class ProjectTreeViewerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ProjectTreeViewerUI, self).__init__(parent)
        self.setContentsMargins(2,2,2,2)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.create_project_btn = QtWidgets.QPushButton()
        self.create_project_btn.setIcon(OriginIcons().add_button_icon())
        self.create_project_btn.setFixedSize(32, 32)
        self.create_project_btn.setStyleSheet(btns.hover_orange)

        self.show_select_cb = ProjectsBoxBuild()
        self.project_tree_viewer_wdg = ProjectTreeViewerBuild()

    def create_layout(self):
        select_proj_layout = QtWidgets.QHBoxLayout()
        select_proj_layout.addWidget(self.show_select_cb)
        select_proj_layout.addWidget(self.create_project_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(select_proj_layout)
        main_layout.addWidget(self.project_tree_viewer_wdg)
        main_layout.setContentsMargins(0,0,0,0)



if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())
    test_dialog = ProjectTreeViewerUI()
    test_dialog.show()
    sys.exit(app.exec_())