from PySide2 import QtWidgets, QtCore, QtGui
from ui.style.icons import OriginIcons
from ui.style import buttons_styles as btns


class CustomDelegate(QtWidgets.QStyledItemDelegate):
    def sizeHint(self, option, index):
        size_hint = super().sizeHint(option, index)
        size_hint.setHeight(35)  # Set the desired row height here
        return size_hint

class TaskViewerBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(TaskViewerBuild, self).__init__(parent)

        # self.widget_width = 400
        self.widget_build()
        self.setItemDelegate(CustomDelegate())
        self.setObjectName("TaskViewerBuild")

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
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):

        self.task_viewer_wdg = TaskViewerBuild()
        self.add_btn = QtWidgets.QPushButton()
        self.add_btn.setIcon(OriginIcons().add_button_icon())
        self.add_btn.setFixedSize(32, 32)
        self.add_btn.setStyleSheet(btns.hover_orange)

        self.save_changes_btn = QtWidgets.QPushButton()
        self.save_changes_btn.setIcon(OriginIcons().save_button_icon())
        self.save_changes_btn.setFixedSize(32, 32)
        self.save_changes_btn.setStyleSheet(btns.hover_orange)

        self.export_btn = QtWidgets.QPushButton()
        self.export_btn.setIcon(OriginIcons().export_button_icon())
        self.export_btn.setFixedSize(32, 32)
        self.export_btn.setStyleSheet(btns.hover_orange)

        self.refresh_btn = QtWidgets.QPushButton()
        self.refresh_btn.setIcon(OriginIcons().refresh_button_icon())
        self.refresh_btn.setFixedSize(32, 32)
        self.refresh_btn.setStyleSheet(btns.hover_orange)

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addStretch()
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