import sys
import json
from PySide2 import QtWidgets

from origin.database.entities.actions import Create


class AddAppUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(AddAppUI, self).__init__(parent)

        self.setWindowTitle("Add Application")

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.app_name_le = QtWidgets.QLineEdit()
        self.app_version_le = QtWidgets.QLineEdit()
        self.exec_path_le = QtWidgets.QLineEdit()
        self.icon_path_le = QtWidgets.QLineEdit()

        self.envars_pt = QtWidgets.QPlainTextEdit()

        self.create_btn = QtWidgets.QPushButton("Add")
        self.create_and_close_btn = QtWidgets.QPushButton("Add and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("App Name: ", self.app_name_le)
        form_layout.addRow("Icon Path:", self.icon_path_le)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.create_btn.clicked.connect(self.add_entry)
        self.create_and_close_btn.clicked.connect(self.add_entry_and_close)
        self.cancel_btn.clicked.connect(self.close)


    def add_entry(self):
        get_name = self.app_name_le.text()
        get_icon_path = self.icon_path_le.text()

        Create().application_entry(app_name=get_name, app_icon=get_icon_path)

        self.app_name_le.clear()
        self.icon_path_le.clear()

    def add_entry_and_close(self):
        self.add_entry()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass

    APP_CONFIG_FILE = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\origin\ui\origin_globals_ui\settings\applications004.json"

    create_asset = AddAppUI()
    create_asset.show()
    sys.exit(app.exec_())