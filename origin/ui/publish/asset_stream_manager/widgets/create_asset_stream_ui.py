import sys
from PySide2 import QtWidgets

from origin.envars.origin_envars import ContextHandler
from origin.database.entities.actions import Create
from origin.database.dispachers.entity_class_dispatcher import extract_asset_class


class CreateStreamUI(QtWidgets.QDialog):

    def __init__(self, context: ContextHandler, parent=None):
        super(CreateStreamUI, self).__init__(parent)

        self.setWindowTitle("Create Asset Stream")

        self.context_handler = context

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLabel()

        item_path = ".".join([self.context_handler.show_name,
                              self.context_handler.origin_path_hierarchy,
                              self.context_handler.entity_name,
                              ]
                             )

        self.show_name_le.setText(item_path)

        self.stream_name_le = QtWidgets.QLineEdit()
        self.stream_name_le.setText(self.context_handler.entity_name)

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
        asset_class = extract_asset_class(context=self.context_handler)

        stream_name = self.stream_name_le.text()
        stream_db_asset_id = Create(context=self.context_handler).db_asset_stream(parent=self.context_handler.entity_id,
                                                                           name=stream_name)

        stream_stack_db_asset = Create(context=self.context_handler).asset_stack(parent_id=stream_db_asset_id)
        asset_class.operations().add_stack_stream(data=stream_db_asset_id)

        stream_breakdown = Create(context=self.context_handler).asset_breakdown(parent_id=stream_stack_db_asset)

        self.stream_name_le.clear()


if __name__ == "__main__":
    from origin.ui.tests.manual_cotext import test_ui

    test_ui(main_widget=CreateStreamUI)
