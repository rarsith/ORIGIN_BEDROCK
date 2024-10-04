from PySide2 import QtWidgets


class BundleViewWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(BundleViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):

        self.setColumnCount(9)
        self.setRowCount(50)
        self.setColumnWidth(0, 30)
        self.setColumnWidth(1, 60)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 20)
        self.setAlternatingRowColors(False)
        # self.setMinimumWidth(850)
        self.setHorizontalHeaderLabels(['', '',
                                        'task01',
                                        'task02',
                                        'task03',
                                        'task04',
                                        'task05',
                                        'task06',
                                        'task07'])
