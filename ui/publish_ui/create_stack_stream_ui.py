import sys
from PySide2 import QtWidgets, QtCore
from envars.origin_envars import OriginEnvar
from o_database.entities.actions import Create, Add
from o_database.schemas.actions import EntityDefaultSchemas
from database.entities.db_structures import DbAssetCategories


class CreateStreamUI(QtWidgets.QDialog):

    def __init__(self, entity_id=None, parent=None):
        super(CreateStreamUI, self).__init__(parent)

        self.setWindowTitle("Create Asset")

        self.entity_id = entity_id

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLabel()
        item_path = ".".join([OriginEnvar().show_name, OriginEnvar().origin_path_hierarchy, OriginEnvar().entry_name])
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
        stream_name = self.stream_name_le.text()
        Add().entity(entity_id=self.entity_id).stack_stream = stream_name
        self.stream_name_le.clear()

    def get_asset_categories(self):
        assets_cat = DbAssetCategories().get_categories()
        return assets_cat


if __name__ == "__main__":
    db_path = ["assets", "characters"]
    OriginEnvar.show_name = "New_World"
    OriginEnvar().origin_path_hierarchy = db_path


    OriginEnvar.entry_name = "hulk"
    OriginEnvar.task_name = "modeling"

    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = CreateStreamUI()
    create_asset.show()
    sys.exit(app.exec_())