import sys
from PySide2 import QtWidgets
from database.entities.db_entities import DbProject


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

        self.initial_folders_lwd = QtWidgets.QTableWidget()
        self.initial_folders_lwd.setColumnCount(4)
        self.initial_folders_lwd.setHorizontalHeaderLabels(["Branch Name", "Type", "R", "A", "S"])
        self.initial_folders_lwd.setShowGrid(False)
        self.initial_folders_lwd.setAlternatingRowColors(True)
        header = self.initial_folders_lwd.verticalHeader()
        header.hide()
        self.initial_folders_lwd.setColumnWidth(0, 200)
        self.initial_folders_lwd.setColumnWidth(1, 163)
        self.initial_folders_lwd.setColumnWidth(2, 20)
        self.initial_folders_lwd.setColumnWidth(3, 20)
        self.initial_folders_lwd.setColumnWidth(4, 20)

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
        DbProject().create(name=self.show_name_le.text())
        self.show_name_le.clear()
        self.show_code_le.clear()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    create_shot = CreateShowUI()
    create_shot.show()

    sys.exit(app.exec_())
