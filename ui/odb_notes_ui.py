from PySide2 import QtWidgets


class NotesWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(NotesWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Label"))
        layout.addWidget(QtWidgets.QPushButton("Button"))
        layout.addWidget(QtWidgets.QCheckBox("Check Box"))
        layout.addWidget(QtWidgets.QLineEdit())
