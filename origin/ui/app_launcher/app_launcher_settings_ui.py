import json
from PySide2 import QtWidgets, QtCore
from origin.ui.app_launcher.custom_widgets.app_browser_ui import AppBrowser
from origin.ui.app_launcher.custom_widgets.app_properties_ui import AppProperties


class AppLauncherSettings(QtWidgets.QWidget):

    def __init__(self, config_file_path=None, parent=None):
        super(AppLauncherSettings, self).__init__(parent)

        self.config_file_path = config_file_path

        self.setMinimumWidth(1000)
        self.setMinimumHeight(850)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.app_browser_wdg = AppBrowser(config_file_path=self.config_file_path)
        self.app_properties_wdg = AppProperties(config_file_path=self.config_file_path)

        self.commit_btn = QtWidgets.QPushButton("Commit")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        vertical_splitter = QtWidgets.QSplitter()
        vertical_splitter.setOrientation(QtCore.Qt.Horizontal)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(vertical_splitter)
        main_layout.addWidget(self.commit_btn)
        main_layout.addWidget(self.refresh_btn)

        vertical_splitter.insertWidget(0, self.app_browser_wdg)
        vertical_splitter.insertWidget(1, self.app_properties_wdg)
        vertical_splitter.setSizes([200, 900])

    def create_connections(self):
        self.app_browser_wdg.selection_data.connect(self.app_properties_wdg.existing_versions_data)
        self.app_browser_wdg.selection_full_data.connect(self.app_properties_wdg.existing_app_base_data)
        self.app_browser_wdg.remove_app_group_btn.clicked.connect(self.refresh_all)
        self.commit_btn.clicked.connect(self.update_app_config)
        self.refresh_btn.clicked.connect(self.refresh_all)

    def refresh_all(self):
        self.app_browser_wdg.populate_app_viewer()
        self.app_properties_wdg.clear_all_properties()

    def get_selected_app(self):
        sel_app = self.app_browser_wdg.get_selected()
        return sel_app

    def update_app_config(self):
        extract_current_properties = self.app_properties_wdg.extract_properties()
        current_selected = self.app_browser_wdg.get_selected()

        with open(self.config_file_path, 'r') as file:
            existing_data = json.load(file)

        existing_data["applications"][current_selected] = (extract_current_properties["base"])

        with open(self.config_file_path, 'w') as file:
            json.dump(existing_data, file, indent=4)

        self.app_browser_wdg.populate_app_viewer()
        self.app_properties_wdg.clear_all_properties()


if __name__ == "__main__":
    import sys

    APP_CONFIG_FILE = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\origin\ui\origin_globals_ui\settings\applications004.json"

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = AppLauncherSettings(config_file_path=APP_CONFIG_FILE)
    test_dialog.show()
    sys.exit(app.exec_())