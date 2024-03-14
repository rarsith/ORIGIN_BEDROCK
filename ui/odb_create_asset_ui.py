import sys
from PySide2 import QtWidgets, QtCore
from envars.origin_envars import OriginEnvar
from o_database.entities.actions import Create
from o_database.schemas.actions import EntityDefaultSchemas
from database.entities.db_structures import DbAssetCategories


class CreateAssetUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateAssetUI, self).__init__(parent)

        self.setWindowTitle("Create Asset")

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.retrieve_data()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLabel()
        item_path = ".".join([OriginEnvar().show_name, OriginEnvar().origin_path_hierarchy])
        self.show_name_le.setText(item_path)

        self.category_cb = QtWidgets.QComboBox()
        self.category_cb.addItem("characters")
        self.category_cb.addItem("props")
        self.category_cb.addItem("environments")
        self.category_cb.addItem("shot")

        self.category_cb.setItemData(0, EntityDefaultSchemas().tasks.character_schema, role=QtCore.Qt.UserRole)
        self.category_cb.setItemData(1, EntityDefaultSchemas().tasks.prop_schema, role=QtCore.Qt.UserRole)
        self.category_cb.setItemData(2, EntityDefaultSchemas().tasks.environment_schema, role=QtCore.Qt.UserRole)
        self.category_cb.setItemData(3, EntityDefaultSchemas().tasks.shot_schema, role=QtCore.Qt.UserRole)



        self.asset_name_le = QtWidgets.QLineEdit()


        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Entry Path: ", self.show_name_le)
        form_layout.addRow("Entry Name:", self.asset_name_le)
        form_layout.addRow("Entry Category:", self.category_cb)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.category_cb.currentIndexChanged.connect(self.retrieve_data)
        self.category_cb.setCurrentIndex(0)

        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def retrieve_data(self):
        curr_index = self.category_cb.currentIndex()
        self.user_data = self.category_cb.itemData(curr_index, role=QtCore.Qt.UserRole)
        return self.user_data

    def db_commit(self):
        asset_name = self.asset_name_le.text()
        Create().asset(name=asset_name, task_schema=self.user_data)
        self.asset_name_le.clear()

    def get_asset_categories(self):
        assets_cat = DbAssetCategories().get_categories()
        return assets_cat


if __name__ == "__main__":
    db_path = ["assets", "characters"]
    OriginEnvar.show_name = "GREEN"
    OriginEnvar().origin_path_hierarchy = db_path


    OriginEnvar.entry_name = "circle"
    OriginEnvar.task_name = "rigging"

    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = CreateAssetUI()
    create_asset.show()
    sys.exit(app.exec_())