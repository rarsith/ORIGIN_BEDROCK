from PySide2 import QtWidgets, QtCore


class QcGhost(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(QcGhost, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def reinitialize(self, pub_options=None):
        pass

    def create_widgets(self):
        self.qc_lb = QtWidgets.QLabel("Publish OC")
        self.recheck_btn = QtWidgets.QPushButton("Recheck")

    def create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.qc_lb)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.recheck_btn)

    def create_connections(self):
        pass

    def get_selected_options(self):
        return {"db_asset_qc": "OK"}


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = QcGhost()

    test_dialog.show()
    sys.exit(app.exec_())
