from PySide2 import QtWidgets, QtCore, QtGui


class TaskViewerBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(TaskViewerBuild, self).__init__(parent)

        # self.widget_width = 400
        self.widget_build()

    def widget_build(self):
        self.setHeaderHidden(True)
        # header = self.header()
        # header.setStretchLastSection(False)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        # self.setColumnCount(2)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # self.widget_columns_names = ["Task", "Task Type"]
        # self.setColumnCount(len(self.widget_columns_names))
        # self.setHeaderLabels(self.widget_columns_names)

        # self.setColumnWidth(0, round(self.widget_width * 0.02))

class TaskViewerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TaskViewerUI, self).__init__(parent)
        self.setMinimumWidth(100)
        # self.setMaximumWidth(170)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.task_viewer_wdg = TaskViewerBuild()
        self.add_btn = QtWidgets.QPushButton("New Task")
        # self.add_btn.setFixedSize(30, 20)

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.add_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.task_viewer_wdg)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())
    test_dialog = TaskViewerUI()
    test_dialog.show()
    sys.exit(app.exec_())