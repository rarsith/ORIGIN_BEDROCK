import sys
from PySide2 import QtWidgets
from envars.envars import Envars
from PySide2 import QtGui
from database.entities.db_entities import DbProject
from database.entities.db_structures import DbProjectBranch


class CreateShowBranchUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateShowBranchUI, self).__init__(parent)

        self.setWindowTitle("Create Show Category")
        # self.setMinimumSize(550, 650)
        # self.setMaximumSize(550, 650)

        # self.setMinimumHeight(900)
        # self.setMaximumHeight(900)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItems(self.get_shows())
        self.show_name_cb.setCurrentText(Envars().show_name)

        self.category_name_le = QtWidgets.QLineEdit()

        default_branch_types = ['build', 'shots', 'lib_asset', 'ref_asset' ]
        self.branch_type_cb = QtWidgets.QComboBox()
        self.branch_type_cb.addItems(default_branch_types)

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name: ", self.show_name_cb)
        form_layout.addRow("Show Branch Name:", self.category_name_le)
        form_layout.addRow("Show Branch Type:", self.branch_type_cb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.show_name_cb.activated.connect(self.comboBox_shows)
        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        DbProjectBranch.add_branch(name=self.category_name_le.text(), branch_type=self.branch_type_cb.currentText())
        self.category_name_le.clear()

    def get_shows(self):
        shows = DbProject().get_all()
        return shows


if __name__ == "__main__":

    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "circle"
    Envars.task_name = "rigging"

    app = QtWidgets.QApplication(sys.argv)

    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))

    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(45,45,45))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(208, 208, 208))



    create_shot = CreateShowBranchUI()
    create_shot.show()

    sys.exit(app.exec_())
