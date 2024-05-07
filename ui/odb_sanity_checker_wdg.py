from PySide2 import QtWidgets, QtCore, QtGui


class SanityChecker(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(SanityChecker, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
