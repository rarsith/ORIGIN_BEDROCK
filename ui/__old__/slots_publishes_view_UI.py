import sys
from PySide2 import QtWidgets, QtCore


class SlotsPublishesViewBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(SlotsPublishesViewBuild, self).__init__(parent)
        self.widget_build()

    def widget_build(self):
        self.setColumnCount(11)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 120)
        self.setColumnWidth(2, 50)
        self.setColumnWidth(3, 50)
        self.setColumnWidth(4, 100)
        self.setColumnWidth(5, 50)
        self.setColumnWidth(6, 50)
        self.setColumnWidth(7, 60)
        self.setColumnWidth(8, 40)
        self.setColumnWidth(9, 0)
        self.setColumnWidth(10, 0)
        self.setMinimumWidth(610)
        self.setSortingEnabled(True)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 20)

        # self.setAlternatingRowColors(True)
        self.setHorizontalHeaderLabels(['Preview',
                                        'Slot Name',
                                        'Version',
                                        'Task',
                                        'Status',
                                        'Origin',
                                        'User',
                                        'Date',
                                        'Time'

                                        ])


class SlotsPublishesViewUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SlotsPublishesViewUI, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.filtering()

    def create_widgets(self):
        self.searchbar_le = QtWidgets.QLineEdit()
        self.slot_publish_view_tw = SlotsPublishesViewBuild()
        self.searchbar_le.setPlaceholderText("Search")

    def create_layout(self):
        slot_view_layout = QtWidgets.QVBoxLayout()
        slot_view_layout.addWidget(self.searchbar_le)
        slot_view_layout.addWidget(self.slot_publish_view_tw)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(slot_view_layout)

    def filtering(self):
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns.
        # self.proxy_model.setSourceModel(self.slot_publish_view_tw)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = SlotsPublishesViewUI()
    test_dialog.show()
    sys.exit(app.exec_())