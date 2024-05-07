import sys
from PySide2 import QtWidgets
from envars.origin_envars import OriginEnvar
# from envars.dc_origin_envars import OriginEnvar
from o_database.entities.actions import Create
from o_database.entities.types import TaskTypes


class CreateTaskUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateTaskUI, self).__init__(parent)

        self.setWindowTitle("Create Task")

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLabel()
        item_path = ".".join([OriginEnvar().show_name, OriginEnvar().origin_path_hierarchy, OriginEnvar().entry_name])
        self.show_name_le.setText(item_path)

        self.task_type_cb = QtWidgets.QComboBox()
        self.task_type_cb.addItems(TaskTypes().all_types())

        self.task_name_le = QtWidgets.QLineEdit()


        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Entry Path: ", self.show_name_le)
        form_layout.addRow("Task Name:", self.task_name_le)
        form_layout.addRow("Task Type:", self.task_type_cb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.task_type_cb.setCurrentIndex(0)

        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        task_name = self.task_name_le.text()
        Create().task(name=task_name, task_type=self.task_type_cb.currentText())
        self.task_name_le.clear()


if __name__ == "__main__":
    db_path = ["test_entities"]
    OriginEnvar.show_name = "NEWERA"
    OriginEnvar().origin_path_hierarchy = db_path


    OriginEnvar.entry_name = "entity_one"
    OriginEnvar.task_name = "rigging"

    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = CreateTaskUI()
    create_asset.show()
    sys.exit(app.exec_())