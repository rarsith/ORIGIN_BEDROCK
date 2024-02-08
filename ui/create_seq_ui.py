import sys
from PySide2 import QtWidgets
from envars.envars import Envars
from database.entities.db_structures import DbAssetCategories
from database.entities.db_entities import DbProject
from database.db_types import TaskTypes


class CreateSeqUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateSeqUI, self).__init__(parent)

        self.setWindowTitle("Create Seq")
        # self.setMinimumSize(550, 650)
        # self.setMaximumSize(550, 650)
        #
        # self.setMinimumHeight(900)
        # self.setMaximumHeight(900)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_lb = QtWidgets.QLabel()
        self.show_name_lb.setText(DbProject.current())
        self.seq_name_le = QtWidgets.QLineEdit()
        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name: ", self.show_name_lb)
        form_layout.addRow("Seq Name:", self.seq_name_le)
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

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        DbAssetCategories.add_category(name=self.seq_name_le.text(), tasks_type=TaskTypes.shots())
        self.seq_name_le.clear()





if __name__ == "__main__":
    # from envars.envars import Envars

    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "DDR"
    Envars.entry_name = "circle"
    Envars.task_name = "rigging"


    app = QtWidgets.QApplication(sys.argv)
    try:
        create_shot.close()
        create_shot.deleteLater()
    except:
        pass
    create_shot = CreateSeqUI()
    create_shot.show()
    sys.exit(app.exec_())