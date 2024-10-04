from PySide2 import QtWidgets, QtGui, QtCore


class ThumbnailViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ThumbnailViewer, self).__init__(parent)

        self.create_widget()
        self.create_layout()

    def create_widget(self):
        # self.label_lb = QtWidgets.QLabel()
        self.label_icon = QtWidgets.QLabel()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.label_icon)

    def set_thumbnail(self, icon_path):
        self.label_icon.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap(icon_path).scaled(200, 128)
        self.label_icon.setPixmap(pixmap)

if __name__ == "__main__":
    import sys

    APP_CONFIG_FILE = r"/dcc/icons/movie_pic.png"

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = ThumbnailViewer()
    test_dialog.set_thumbnail(icon_path=APP_CONFIG_FILE)

    test_dialog.show()
    sys.exit(app.exec_())
