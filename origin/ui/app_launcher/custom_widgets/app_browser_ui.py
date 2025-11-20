from PySide2 import QtWidgets, QtCore, QtGui

from origin.database.entities.actions import Create
from origin.database.entities.operators import DCCBaseModel
from origin.database.mongo import CollectionOperators, DBRemove, DBDelete
from origin.database.mongo_connection import MongoConnection
from origin.ui.app_launcher.custom_widgets.add_app_ui import AddAppUI
from origin.ui.app_launcher.custom_widgets.import_from_json_ui import ImportAppsUI


class AppBrowser(QtWidgets.QWidget):
    selection_data = QtCore.Signal(dict)
    selection_full_data = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(AppBrowser, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.populate_app_viewer()

    def create_widgets(self):
        self.app_tree_tw = QtWidgets.QTreeWidget()
        self.app_tree_tw.setHeaderHidden(True)
        self.app_tree_tw.expandAll()
        self.app_tree_tw.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.app_tree_tw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.app_tree_tw.setFocusPolicy(QtCore.Qt.NoFocus)

        self.add_app_group_btn = QtWidgets.QPushButton("Add Application...")
        self.remove_app_group_btn = QtWidgets.QPushButton("Remove Application")
        self.import_app_group_btn = QtWidgets.QPushButton("Import From JSON...")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.app_tree_tw)
        main_layout.addWidget(self.add_app_group_btn)
        main_layout.addWidget(self.import_app_group_btn)
        main_layout.addWidget(self.remove_app_group_btn)

    def create_connections(self):
        self.app_tree_tw.itemClicked.connect(self.get_app_data_from_selected)
        self.add_app_group_btn.clicked.connect(self.add_app_menu)
        self.import_app_group_btn.clicked.connect(self.import_app_menu)
        self.remove_app_group_btn.clicked.connect(self.remove_app)

    def remove_app(self):
        sel_id = self.get_selected_app_id()
        if sel_id:
            DBDelete(database=MongoConnection().origin_setup_database(),
                     db_collection="Applications",
                     entry_id=sel_id).document()

        self.populate_app_viewer()

    def populate_app_viewer(self):
        self.app_tree_tw.clear()
        db_ops = CollectionOperators(db_collection="Applications", database=MongoConnection().origin_setup_database())
        root_documents = db_ops.get_root_documents(attrib_field="type", attrib_value="application")

        if root_documents:
            for root_doc in root_documents:
                doc_data_class = DCCBaseModel(**root_doc)

                app_display_name = doc_data_class.name
                app_icon = doc_data_class.icon_path

                item = QtWidgets.QTreeWidgetItem([app_display_name])
                item.setData(0, QtCore.Qt.UserRole, doc_data_class)

                icon = QtGui.QIcon(app_icon)
                item.setIcon(0, icon)

                self.app_tree_tw.addTopLevelItem(item)

    def get_app_data_from_selected(self):
        sel = self.app_tree_tw.currentItem()
        doc_data_class = sel.data(0, QtCore.Qt.UserRole)
        self.selection_data.emit(doc_data_class)

    def get_selected(self):
        sel = self.app_tree_tw.currentItem()
        return sel.text(0).lower()

    def get_selected_app_id(self):
        sel = self.app_tree_tw.currentItem()
        doc_data_class = sel.data(0, QtCore.Qt.UserRole)
        return doc_data_class.id

    def add_app_menu(self):
        self.ui = AddAppUI()
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.populate_app_viewer)
        self.ui.create_and_close_btn.clicked.connect(self.populate_app_viewer)

    def import_app_menu(self):
        self.ui = ImportAppsUI()
        self.ui.show()
        self.ui.import_btn.clicked.connect(self.populate_app_viewer)


if __name__ == "__main__":
    import sys
    import os
    import shutil
    import platform


    def find_executable(software_name):
        """
        Searches for the given software's executable in the system's PATH.
        Works on both Windows and Linux.

        Args:
            software_name (str): The name of the software to search for.

        Returns:
            str: The full path of the executable if found, None otherwise.
        """
        # Check for the OS
        system = platform.system().lower()

        # Try to locate the executable in the system PATH
        executable_path = shutil.which(software_name)

        if executable_path:
            return executable_path

        # Additional method for Windows (Registry-based search can be added if needed)
        if system == "windows":
            # Look for .exe suffix automatically
            if not software_name.endswith(".exe"):
                executable_path = shutil.which(f"{software_name}.exe")
                if executable_path:
                    return executable_path

        # Not found
        return None


    # software = "Maya"
    # path = find_executable(software)
    # if path:
    #     print(f"{software} found at: {path}")
    # else:
    #     print(f"{software} not found.")


    # app = QtWidgets.QApplication(sys.argv)
    #
    # test_dialog = AppBrowser()
    # test_dialog.show()
    # sys.exit(app.exec_())


    # config_file_path = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\origin\config\applications\config_applications.json"
    #
    #
    # def get_config_data(app_config_file=None):
    #     from origin.common_utils import json_utils
    #     config_data = json_utils.open_json(app_config_file)
    #     return config_data["applications"]
    #
    # all_apps = get_config_data(config_file_path)
    #
    # for app, app_data in all_apps.items():
    #     app_entry_id = Create().application_entry(app_name=app, app_icon=app_data["icon"])
    #     for version_id, version_data in app_data["versions"].items():
    #         safe_name = version_id
    #         if "." in version_id:
    #             safe_name = version_id.replace(".", "_")
    #
    #         if version_data:
    #             Create().application_version_entry(parent_id=app_entry_id,
    #                                                active=True,
    #                                                version_id=safe_name,
    #                                                exec_path=version_data["executable_path"],
    #                                                exec_python='',
    #                                                envars=version_data["envar_data"],
    #                                                )

import os






# Example Usage


