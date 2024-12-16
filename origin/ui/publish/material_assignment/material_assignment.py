from PySide2 import QtWidgets, QtCore


class MaterialSetsAssignments(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MaterialSetsAssignments, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def reinitialize(self, pub_options=None):
        pass

    def create_widgets(self):
        self.sets_lw = QtWidgets.QLabel("Material and Sets Assignments")
        self.list_sets = QtWidgets.QListWidget()
        self.recheck_btn = QtWidgets.QPushButton("Recheck")

    def create_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.sets_lw)
        self.main_layout.addWidget(self.list_sets)
        self.main_layout.addWidget(self.recheck_btn)

    def create_connections(self):
        pass

    def get_selected_options(self):
        return {"material_collections": {}}


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = MaterialSetsAssignments()

    test_dialog.show()
    sys.exit(app.exec_())
