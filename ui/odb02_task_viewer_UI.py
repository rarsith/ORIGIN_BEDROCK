from PySide2 import QtWidgets, QtCore, QtGui


class CustomDelegate(QtWidgets.QStyledItemDelegate):
    def sizeHint(self, option, index):
        size_hint = super().sizeHint(option, index)
        size_hint.setHeight(25)  # Set the desired row height here
        return size_hint

class TaskViewerBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(TaskViewerBuild, self).__init__(parent)

        # self.widget_width = 400
        self.widget_build()
        self.setItemDelegate(CustomDelegate())

    def widget_build(self):
        self.setColumnCount(11)
        width = 950

        # self.setHeaderHidden(True)
        header = self.header()
        header.setStretchLastSection(True)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        # self.setColumnCount(2)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setHeaderLabels(['Name',
                              'Type',
                              'Status',
                              'Bid',
                              'Used',
                              '+/-',
                              'Start',
                              'End',
                              'Prio',
                              'Artist',
                              'Description',
                              ])

        # self.widget_columns_names = ["Task", "Task Type"]
        # self.setColumnCount(len(self.widget_columns_names))
        # self.setHeaderLabels(self.widget_columns_names)

        self.setColumnWidth(0, round(width * 0.1))
        self.setColumnWidth(1, round(width * 0.11))
        self.setColumnWidth(2, round(width * 0.15))
        self.setColumnWidth(3, round(width * 0.03))
        self.setColumnWidth(4, round(width * 0.03))
        self.setColumnWidth(5, round(width * 0.03))
        self.setColumnWidth(6, round(width * 0.09))
        self.setColumnWidth(7, round(width * 0.09))
        self.setColumnWidth(8, round(width * 0.08))
        self.setColumnWidth(9, round(width * 0.09))
        self.setColumnWidth(10, round(width * 0.1))

        self.setUniformRowHeights(True)



class TaskViewerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TaskViewerUI, self).__init__(parent)
        # self.setMinimumWidth(800)
        # self.setMaximumWidth(170)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.task_viewer_wdg = TaskViewerBuild()
        self.add_btn = QtWidgets.QPushButton("New Task")
        self.save_changes_btn = QtWidgets.QPushButton("Save Changes")
        self.export_btn = QtWidgets.QPushButton("Export")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        # self.add_btn.setFixedSize(30, 20)

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.add_btn)
        top_layout.addWidget(self.save_changes_btn)
        top_layout.addWidget(self.export_btn)
        top_layout.addWidget(self.refresh_btn)

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