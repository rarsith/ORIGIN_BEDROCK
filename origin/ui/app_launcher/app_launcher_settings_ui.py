import json
from PySide2 import QtWidgets, QtCore

from origin.database.mongo import DBSet
from origin.database.mongo_connection import MongoConnection
from origin.ui.app_launcher.custom_widgets.app_browser_ui import AppBrowser
from origin.ui.app_launcher.custom_widgets.app_properties_ui import AppProperties


class AppLauncherSettings(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AppLauncherSettings, self).__init__(parent)

        self.setMinimumWidth(1000)
        self.setMinimumHeight(850)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.app_browser_wdg = AppBrowser()
        self.app_properties_wdg = AppProperties()

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
        origin_setup_db = MongoConnection().origin_setup_database()
        origin_applications_collection = "Applications"
        extract_current_properties = self.app_properties_wdg.extract_properties()
        current_selected_data = self.app_properties_wdg.selected_app

        DBSet(database=origin_setup_db,
              db_collection=origin_applications_collection,
              entry_id=current_selected_data.id,
              attribute=current_selected_data.ACTIVE).attribute_value(extract_current_properties['base']['enabled'])

        DBSet(database=origin_setup_db,
              db_collection=origin_applications_collection,
              entry_id=current_selected_data.id,
              attribute=current_selected_data.ICON_PATH).attribute_value(extract_current_properties['base']['icon'])

        DBSet(database=origin_setup_db,
              db_collection=origin_applications_collection,
              entry_id=current_selected_data.id,
              attribute=current_selected_data.NAME).attribute_value(extract_current_properties['base']['display_name'])

        DBSet(database=origin_setup_db,
              db_collection=origin_applications_collection,
              entry_id=current_selected_data.id,
              attribute=current_selected_data.VERSIONS).attribute_value(data={})

        DBSet(database=origin_setup_db,
              db_collection=origin_applications_collection,
              entry_id=current_selected_data.id,
              attribute=current_selected_data.VERSIONS).attribute_value(extract_current_properties['base']['versions'])

        self.app_browser_wdg.populate_app_viewer()
        self.app_properties_wdg.clear_all_properties()


if __name__ == "__main__":
    from origin.ui.tests.manual_cotext import test_ui
    test_ui(main_widget=AppLauncherSettings)
