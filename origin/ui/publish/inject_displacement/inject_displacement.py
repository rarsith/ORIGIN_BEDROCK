from PySide2 import QtWidgets, QtCore


class InjectDisplacement(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(InjectDisplacement, self).__init__(parent)
        self.setWindowTitle("Inject Displacement")

        self.displacement_file = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.inject_displacement_lb = QtWidgets.QLabel("Add Displacement Map Set")
        self.displ_le = QtWidgets.QLineEdit()
        self.displ_le.setPlaceholderText("Select Displacement Maps")
        self.browse_btn = QtWidgets.QPushButton("Browse")

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.displ_le)
        top_layout.addWidget(self.browse_btn)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.inject_displacement_lb)
        self.main_layout.addLayout(top_layout)
        self.main_layout.addStretch()

    def create_connections(self):
        self.browse_btn.clicked.connect(self.open_system_file_explorer)

    def open_system_file_explorer(self):
        import os
        get_origin_root = os.getenv("ORIGIN_PROJECTS_ROOT")
        self.displacement_file, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File", get_origin_root)
        self.displ_le.setText(self.displacement_file[0])

    def get_selected_options(self):
        return {"inject_textures_path": self.displacement_file}


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = InjectDisplacement()

    test_dialog.show()
    sys.exit(app.exec_())
