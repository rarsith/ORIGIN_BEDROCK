import sys
from PySide2 import QtWidgets
from envars.envars import Envars
from database.entities.db_entities import DbAsset, DbProject
from database.entities.db_structures import DbAssetCategories


class CreateAssetUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateAssetUI, self).__init__(parent)

        self.setWindowTitle("Create Asset")

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLabel()
        self.show_name_le.setText("/".join([Envars().show_name, Envars().branch_name, Envars().category]) + "/")

        self.category_cb = QtWidgets.QComboBox()
        self.category_cb.addItems(self.get_asset_categories())
        self.asset_name_le = QtWidgets.QLineEdit()

        self.create_btn = QtWidgets.QPushButton("Create")
        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Entry Path: ", self.show_name_le)
        form_layout.addRow("Entry Name:", self.asset_name_le)

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
        asset_name = self.asset_name_le.text()
        DbAsset().create(name=asset_name)

        self.asset_name_le.clear()

    def get_asset_categories(self):
        assets_cat = DbAssetCategories().get_categories()
        return assets_cat


if __name__ == "__main__":
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "circle"
    Envars.task_name = "rigging"

    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = CreateAssetUI()
    create_asset.show()
    sys.exit(app.exec_())