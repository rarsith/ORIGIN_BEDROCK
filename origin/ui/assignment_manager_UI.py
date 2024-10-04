from PySide2 import QtWidgets, QtCore, QtGui


class ProjectShotsBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ProjectShotsBuild, self).__init__(parent)
        self.setMinimumWidth(150)
        self.setMaximumWidth(160)

        self.widget_build()

    def widget_build(self):
        self.setHeaderHidden(True)

        self.expandAll()
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


class ProjectAssetsBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ProjectAssetsBuild, self).__init__(parent)
        self.setMinimumWidth(150)
        self.setMaximumWidth(160)

        self.widget_build()

    def widget_build(self):
        self.setHeaderHidden(True)

        self.expandAll()
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


class AssignmentsViewerBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(AssignmentsViewerBuild, self).__init__(parent)
        self.setMinimumWidth(500)


        self.widget_build()

    def widget_build(self):

        self.setColumnCount(2)
        self.setColumnWidth(0, 250)

        self.setHeaderLabels(["Slot Name", "Value"])
        self.setAlternatingRowColors(False)
        self.resizeColumnToContents(1)
        self.expandAll()
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setFocusPolicy(QtCore.Qt.NoFocus)


class AssignmentManagerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AssignmentManagerUI, self).__init__(parent)
        self.setMinimumHeight(750)
        self.setMinimumWidth(1000)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.existing_shots_lb = QtWidgets.QLabel("Existing Shots")
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.existing_shots_lb.setFont(my_font)
        self.existing_shots_lb.setStyleSheet("color: red")

        self.project_assets_lb = QtWidgets.QLabel("Assets To Assign")
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.project_assets_lb.setFont(my_font)
        self.project_assets_lb.setStyleSheet("color: red")

        self.assignments_lb = QtWidgets.QLabel("Assignments")
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.assignments_lb.setFont(my_font)
        self.assignments_lb.setStyleSheet("color: red")

        # self.assignment_tree_viewer_wdg = AssignmentManagerBuild()
        self.project_shots_viewer_wdg = ProjectShotsBuild()
        self.project_assets_viewer_wdg = ProjectAssetsBuild()
        self.assignment_tree_viewer_wdg = AssignmentsViewerBuild()

        self.move_to_right_btn = QtWidgets.QPushButton(">")
        self.move_to_right_btn.setMinimumHeight(150)
        self.move_to_right_btn.setMinimumWidth(20)
        self.move_to_right_btn.setMaximumWidth(20)

        self.collapse_all_btn = QtWidgets.QPushButton("-")
        self.expand_all_btn = QtWidgets.QPushButton("=")
        self.save_btn = QtWidgets.QPushButton("Commit")
        self.remove_btn = QtWidgets.QPushButton("Remove Selected")
        self.import_from_entity_btn = QtWidgets.QPushButton("Load Assignments From Entity...")
        self.apply_to_all_in_category_btn = QtWidgets.QPushButton("Assign To All In Seq...")
        self.apply_to_seq_btn = QtWidgets.QPushButton("Assign To Seq...")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

        self.info_box_wdg = QtWidgets.QLabel("...")

    def create_layout(self):

        collapse_exp_layout = QtWidgets.QHBoxLayout()
        collapse_exp_layout.addWidget(self.collapse_all_btn)
        collapse_exp_layout.addWidget(self.expand_all_btn)

        assignment_top_layout = QtWidgets.QHBoxLayout()
        assignment_top_layout.addWidget(self.assignments_lb)
        assignment_top_layout.addLayout(collapse_exp_layout)

        project_shots_layout = QtWidgets.QVBoxLayout()
        project_shots_layout.addWidget(self.existing_shots_lb)
        project_shots_layout.addWidget(self.project_shots_viewer_wdg)

        project_assets_layout = QtWidgets.QVBoxLayout()
        project_assets_layout.addWidget(self.project_assets_lb)
        project_assets_layout.addWidget(self.project_assets_viewer_wdg)

        assignment_viewer_layout = QtWidgets.QVBoxLayout()
        assignment_viewer_layout.addLayout(assignment_top_layout)
        assignment_viewer_layout.addWidget(self.assignment_tree_viewer_wdg)

        viewers_layout = QtWidgets.QHBoxLayout()
        viewers_layout.addLayout(project_shots_layout)
        viewers_layout.addSpacing(20)
        viewers_layout.addLayout(project_assets_layout)
        viewers_layout.addWidget(self.move_to_right_btn)
        viewers_layout.addLayout(assignment_viewer_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.import_from_entity_btn)
        main_layout.addLayout(viewers_layout)
        main_layout.addWidget(self.save_btn)
        main_layout.addWidget(self.remove_btn)
        main_layout.addWidget(self.refresh_btn)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.apply_to_all_in_category_btn)
        main_layout.addWidget(self.apply_to_seq_btn)
        main_layout.addWidget(self.info_box_wdg)



if __name__ == '__main__':
    import sys
    import pprint

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())
    test_dialog = AssignmentManagerUI()
    test_dialog.show()
    sys.exit(app.exec_())