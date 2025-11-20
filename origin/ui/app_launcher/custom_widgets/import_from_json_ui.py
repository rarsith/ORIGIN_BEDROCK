import pprint
import sys
import json
from pathlib import Path
from typing import List

from PySide2 import QtWidgets
from origin.database.entities.actions import Create
from origin.database.mongo import CollectionOperators
from origin.database.mongo_connection import MongoConnection


class ImportAppsUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(ImportAppsUI, self).__init__(parent)

        self.setMinimumWidth(600)
        self.setMinimumHeight(450)

        self.setWindowTitle("Import From JSON")
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def open_system_file_explorer(self):
        import os
        get_origin_dev_root = Path(os.getenv("ORIGIN_ROOT"))
        origin_configs = get_origin_dev_root / Path("origin/config/applications/")

        self.json_file, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File", str(origin_configs))
        self.app_json_file_le.setText(self.json_file[0])

    def create_widgets(self):
        self.message_wdg = QtWidgets.QTextEdit()
        self.app_json_lb = QtWidgets.QLabel("Applications JSON File")
        self.browse_btn = QtWidgets.QPushButton("Browse")
        self.app_json_file_le = QtWidgets.QLineEdit()
        self.app_json_file_le.setPlaceholderText("Browse and Select Json File")
        self.import_btn = QtWidgets.QPushButton("Import")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QHBoxLayout()
        form_layout.addWidget(self.app_json_lb)
        form_layout.addWidget(self.app_json_file_le)
        form_layout.addWidget(self.browse_btn)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.import_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.message_wdg)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.import_btn.clicked.connect(self.import_apps)
        self.browse_btn.clicked.connect(self.open_system_file_explorer)
        self.cancel_btn.clicked.connect(self.close)

    def get_config_data(self, app_config_file=None):
        from origin.common_utils import json_utils
        config_data = json_utils.open_json(app_config_file)
        return config_data["applications"]

    def format_as_html(self, data: List[dict]):
        html_lines = ["<b style='color:green;'>Added Applications</b><br>"]
        for app_set in data:
            for app_name, app_version_data in app_set.items():
                html_lines.append(f"<b>Added {app_name}</b>: version ------> {app_version_data} .......................<b style='color:green;'>OK</b><br>")
        return "<br>".join(html_lines)

    def get_current_apps(self):
        db_ops = CollectionOperators(db_collection="Applications", database=MongoConnection().origin_setup_database())
        root_documents = db_ops.get_root_documents(attrib_field="type", attrib_value="application")
        return root_documents

    def import_apps(self):
        get_file = self.app_json_file_le.text()

        existing_apps = self.get_current_apps()

        apps_added_report = []

        if get_file:
            all_apps = self.get_config_data(app_config_file=get_file)

            for application, app_data in all_apps.items():
                app_entry_id = Create().application_entry(app_name=application, app_icon=app_data["icon"])

                for version_id, version_data in app_data["versions"].items():
                    safe_name = version_id
                    if "." in version_id:
                        safe_name = version_id.replace(".", "_")

                    if version_data:
                        Create().application_version_entry(parent_id=app_entry_id,
                                                           active=True,
                                                           version_id=safe_name,
                                                           exec_path=version_data["executable_path"],
                                                           exec_python='',
                                                           envars=version_data["envar_data"],
                                                           )
                        apps_added_report.append({app_entry_id: safe_name})

        to_html = self.format_as_html(apps_added_report)

        self.message_wdg.setHtml(to_html)
        self.app_json_file_le.clear()

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
