import sys
from PySide2 import QtWidgets
from origin.envars.Xorigin_envars import ContextHandler
from o_database.entities.Xactions import Create


class CreateShowUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateShowUI, self).__init__(parent)

        self.setWindowTitle("Create Show")
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLineEdit()
        self.show_code_le = QtWidgets.QLineEdit()
        self.show_type_cb = QtWidgets.QComboBox()
        self.show_type_cb.addItems(["vfx","commercial"])

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Enter Show Name:", self.show_name_le)
        form_layout.addRow("Enter Show Code:", self.show_code_le)
        form_layout.addRow("Select Show Type:", self.show_type_cb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        context_handler = ContextHandler()
        context_handler.show_name = self.show_name_le.text()
        context = context_handler.snapshot_session()
        Create(context=context).project(name=self.show_name_le.text(),
                                        project_type=self.show_type_cb.currentText(),
                                        project_code=self.show_code_le.text())
        self.show_name_le.clear()
        self.show_code_le.clear()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    create_shot = CreateShowUI()
    create_shot.show()

    sys.exit(app.exec_())
