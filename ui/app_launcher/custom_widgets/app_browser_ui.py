from PySide2 import QtWidgets, QtCore, QtGui
from ui.app_launcher.custom_widgets.add_app_ui import AddAppUI


class AppBrowser(QtWidgets.QWidget):
    selection_data = QtCore.Signal(dict)
    selection_full_data = QtCore.Signal(dict)

    def __init__(self, config_file_path=None, parent=None):
        super(AppBrowser, self).__init__(parent)

        self.config_file_path = config_file_path

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

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.app_tree_tw)
        main_layout.addWidget(self.add_app_group_btn)
        main_layout.addWidget(self.remove_app_group_btn)

    def create_connections(self):
        self.app_tree_tw.itemClicked.connect(self.get_versions_from_selected)
        self.app_tree_tw.itemClicked.connect(self.get_full_data_from_selected)
        self.add_app_group_btn.clicked.connect(self.add_app_menu)
        self.remove_app_group_btn.clicked.connect(self.remove_app)

    def remove_app(self):
        import json

        sel_name = self.get_selected()

        if sel_name:
            with open(self.config_file_path, 'r') as file:
                existing_data = json.load(file)

            del existing_data["applications"][sel_name]

            with open(self.config_file_path, 'w') as file:
                json.dump(existing_data, file, indent=4)

        self.populate_app_viewer()

    def populate_app_viewer(self):
        self.app_tree_tw.clear()
        get_apps = self.get_config_data(app_config_file=self.config_file_path)

        if get_apps:
            for keys, values in get_apps.items():
                app_display_name = keys.capitalize()
                app_version = values["versions"]
                app_icon = values["icon"]

                item = QtWidgets.QTreeWidgetItem([app_display_name])
                item.setData(0, QtCore.Qt.UserRole, app_version)
                item.setData(1, QtCore.Qt.UserRole, values)

                icon = QtGui.QIcon(app_icon)
                item.setIcon(0, icon)

                self.app_tree_tw.addTopLevelItem(item)

    def get_config_data(self, app_config_file=None):
        from common_utils import json_utils
        config_data = json_utils.open_json(app_config_file)
        return config_data["applications"]

    def get_versions_from_selected(self):
        sel = self.app_tree_tw.currentItem()
        app_versions = sel.data(0, QtCore.Qt.UserRole)
        self.selection_data.emit(app_versions)

    def get_full_data_from_selected(self):
        sel = self.app_tree_tw.currentItem()
        app_data = sel.data(1, QtCore.Qt.UserRole)
        self.selection_full_data.emit(app_data)

    def get_selected(self):
        sel = self.app_tree_tw.currentItem()
        return sel.text(0).lower()

    def add_app_menu(self):
        self.ui = AddAppUI(config_file_path=self.config_file_path)
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.populate_app_viewer)
        self.ui.create_and_close_btn.clicked.connect(self.populate_app_viewer)



if __name__ == "__main__":
    import sys

    # print(applications_config_file)

    config_file_path = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\ui\origin_globals_ui\settings\applications004.json"

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = AppBrowser(config_file_path=config_file_path)
    # test_dialog.get_config_data(app_config_file=config_file_path)
    test_dialog.show()
    sys.exit(app.exec_())
