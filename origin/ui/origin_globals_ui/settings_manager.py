import sys
from PySide2 import QtWidgets, QtCore

class AppManager(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AppManager, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        pass

    def create_layout(self):
        pass

    def create_connections(self):
        pass

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = AppManager()
    test_dialog.show()
    sys.exit(app.exec_())
