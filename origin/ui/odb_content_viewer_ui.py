from PySide2 import QtWidgets


class ContentViewWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(ContentViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        # self.setMaximumWidth(437)
        # self.setMinimumWidth(400)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Asset Name", "Category", "status", "health"])
        self.setShowGrid(True)
        self.setRowCount(20)
        self.setAlternatingRowColors(True)
        # header = self.shot_content_twd.verticalHeader()
        # header.hide()
        self.setColumnWidth(0, 135)
        self.setColumnWidth(1, 135)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 67)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 5)
