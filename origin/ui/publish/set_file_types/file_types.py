from PySide2 import QtWidgets, QtCore


class FileTypes(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(FileTypes, self).__init__(parent)
        self.setWindowTitle("Geometry Miscellaneous")

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def reinitialize(self, pub_options=None):
        pass

    def create_widgets(self):
        self.qc_lb = QtWidgets.QLabel("Select File Types to export")
        self.alembic_rbtn = QtWidgets.QCheckBox("abc")
        self.alembic_rbtn.setChecked(True)

        self.usd_rbtn = QtWidgets.QCheckBox("usd")
        self.usd_rbtn.setChecked(True)

        self.obj_rbtn = QtWidgets.QCheckBox("obj")
        self.obj_rbtn.setChecked(True)

        self.bake_AO_rbtn = QtWidgets.QCheckBox("Bake Ambient Occlusion")
        self.bake_CRV_rbtn = QtWidgets.QCheckBox("Bake Curvature Map")

    def create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.qc_lb)
        self.main_layout.addWidget(self.alembic_rbtn)
        self.main_layout.addWidget(self.usd_rbtn)
        self.main_layout.addWidget(self.obj_rbtn)
        self.main_layout.addWidget(self.bake_AO_rbtn)
        self.main_layout.addWidget(self.bake_CRV_rbtn)
        self.main_layout.addStretch(1)

    def create_connections(self):
        pass

    def get_checked(self):
        get_checked_widgets = []
        for idx in range(self.main_layout.count()):
            widget = self.main_layout.itemAt(idx).widget()

            if isinstance(widget, QtWidgets.QCheckBox):
                if widget.isChecked():
                    get_checked_widgets.append(widget)
        return get_checked_widgets

    def get_selected_options(self):
        checked_widgets = self.get_checked()
        wdg_names = [name.text() for name in checked_widgets]
        return {"user_file_formats": wdg_names, "persistent_file_formats": ["master"]}


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = FileTypes()

    test_dialog.show()
    sys.exit(app.exec_())
