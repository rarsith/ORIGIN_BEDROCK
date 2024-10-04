import sys
from PySide2 import QtWidgets

from origin.envars.Xorigin_envars import ContextHandler
from o_database.entities.Xactions import Create
from o_database.entities.asset_class_dispacher import extract_asset_class


class CreateStreamUI(QtWidgets.QDialog):

    def __init__(self, context=None, parent=None):
        super(CreateStreamUI, self).__init__(parent)

        self.setWindowTitle("Create Asset")

        self.context_handler = ContextHandler()
        self.context_handler.load_session(context)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLabel()

        item_path = ".".join([self.context_handler.show_name,
                              self.context_handler.origin_path_hierarchy,
                              self.context_handler.entity_name,
                              self.context_handler.task_type]
                             )

        self.show_name_le.setText(item_path)

        self.stream_name_le = QtWidgets.QLineEdit()

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Entry Path: ", self.show_name_le)
        form_layout.addRow("Stream Name:", self.stream_name_le)

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
        context = self.context_handler.snapshot_session()
        asset_class = extract_asset_class(context=context)
        stream_name = self.stream_name_le.text()
        db_asset_id = Create(context=context).db_asset(parent=self.context_handler.entity_id,
                                                       name=stream_name)

        asset_class.add_stack_stream(data=db_asset_id.inserted_id)
        self.stream_name_le.clear()


if __name__ == "__main__":
    context_sample = {'show_name': 'New_State',
                      'project_publishes': 'New_State__PUBLISHES',
                      'project_work': 'New_State__WORK',
                      'project_control': 'New_State__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'red_hulk',
                      'entity_type': 'asset',
                      'entity_id': 'New_State.assets.chr.red_hulk',
                      'task_name': "modeling",
                      'task_type': "modeling"}

    app = QtWidgets.QApplication(sys.argv)
    create_asset = CreateStreamUI(context=context_sample)
    create_asset.show()
    sys.exit(app.exec_())
