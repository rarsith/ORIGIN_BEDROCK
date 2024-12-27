import sys
from PySide2 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setWindowTitle("Test Window")
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())