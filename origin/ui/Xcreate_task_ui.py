import sys
from PySide2 import QtWidgets

from origin.envars.Xorigin_envars import ContextHandler
from o_database.entities.Xactions import Create
from o_database.entities.db_types import TaskTypes


class CreateTaskUI(QtWidgets.QDialog):

    def __init__(self, context, task_parent=None, parent=None):
        super(CreateTaskUI, self).__init__(parent)

        self.setWindowTitle("Create Task")

        self.context_handler = ContextHandler()
        self.context_handler.load_session(context)

        self.task_parent = task_parent

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLabel()

        if self.task_parent is not None:
            self.show_name_le.setText(self.task_parent)
        else:
            self.show_name_le.setText(self.context_handler.show_name)

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
        context = self.context_handler.snapshot_session()
        Create(context=context).task(name=task_name,
                                     parent=self.task_parent,
                                     task_type=self.task_type_cb.currentText())
        self.task_name_le.clear()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = CreateTaskUI()
    create_asset.show()
    sys.exit(app.exec_())