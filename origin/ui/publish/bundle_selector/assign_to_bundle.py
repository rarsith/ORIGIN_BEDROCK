from PySide2 import QtWidgets, QtCore


class BundleSelector(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BundleSelector, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.window_title_lb = QtWidgets.QLabel("Bundle Selector")
        self.existing_bundles_lw = QtWidgets.QListWidget()
        self.selected_bundle_lw = QtWidgets.QListWidget()

    def create_layout(self):
        bundle_layout = QtWidgets.QHBoxLayout()
        bundle_layout.addWidget(self.existing_bundles_lw)
        bundle_layout.addWidget(self.selected_bundle_lw)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.window_title_lb)
        self.main_layout.addLayout(bundle_layout)

    def create_connections(self):
        pass

    def get_checked(self):
        pass

    def get_selected_options(self):
        return {"bundle_stream_id": ""}


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = BundleSelector()

    test_dialog.show()
    sys.exit(app.exec_())
