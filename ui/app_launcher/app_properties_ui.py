import json
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Slot


class AppVersionsWidget(QtWidgets.QWidget):
    def __init__(self, tree_widget=None, parent=None):
        super(AppVersionsWidget, self).__init__(parent)

        self.tree_widget = tree_widget

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.version_name_le = QtWidgets.QLineEdit()
        self.executable_path_le = QtWidgets.QLineEdit()
        self.browse_executable_btn = QtWidgets.QPushButton("Browse")
        self.envar_data_pt = QtWidgets.QPlainTextEdit()
        self.envar_data_pt.setMaximumHeight(50)
        self.envar_data_pt.setMaximumWidth(250)
        self.delete_version_btn = QtWidgets.QPushButton("X")
        self.delete_version_btn.setFixedSize(60, 100)

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Version: ", self.version_name_le)
        form_layout.addRow("Executable Path:", self.executable_path_le)
        form_layout.addRow("Environment:", self.envar_data_pt)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(form_layout)

    def create_connections(self):
        self.delete_version_btn.clicked.connect(self.delete_item)


    def delete_item(self):
        index = self.tree_widget.indexOfTopLevelItem(self.parent())

        if index != -1:
            self.tree_widget.takeTopLevelItem(index)

    def populate_properties(self, version_name=None, executable_path=None, envar_data=None):
        self.version_name_le.setText(version_name)
        self.executable_path_le.setText(executable_path)
        self.envar_data_pt.insertPlainText(str(envar_data))


class AppPropertiesWidget(QtWidgets.QWidget):

    def __init__(self, config_file_path=None, parent=None):
        super(AppPropertiesWidget, self).__init__(parent)

        self.config_file_path = config_file_path

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.app_is_active = QtWidgets.QCheckBox()
        self.app_name_le = QtWidgets.QLineEdit()
        self.app_icon_path = QtWidgets.QLineEdit()

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Active: ", self.app_is_active)
        form_layout.addRow("App Name:", self.app_name_le)
        form_layout.addRow("Icon:", self.app_icon_path)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)


class AppProperties(QtWidgets.QWidget):

    def __init__(self, config_file_path=None, parent=None):
        super(AppProperties, self).__init__(parent)

        self.config_file_path = config_file_path

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.properties_viewer_tw = QtWidgets.QTreeWidget()
        self.properties_viewer_tw.setHeaderHidden(True)
        self.properties_viewer_tw.setColumnCount(2)
        self.properties_viewer_tw.setColumnWidth(0, 650)
        self.properties_viewer_tw.setColumnWidth(1, 50)
        self.properties_viewer_tw.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.properties_viewer_tw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.properties_viewer_tw.setFocusPolicy(QtCore.Qt.NoFocus)
        self.properties_viewer_tw.setStyleSheet("QTreeView {border: none; outline: 0;}")

        self.app_base_config_wdg = AppPropertiesWidget(config_file_path=self.config_file_path)
        self.properties_widget = AppVersionsWidget()

        self.add_version_btn = QtWidgets.QPushButton("Add Version")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.app_base_config_wdg)
        main_layout.addWidget(self.properties_viewer_tw)
        main_layout.addWidget(self.add_version_btn)

    def create_connections(self):
        self.add_version_btn.clicked.connect(self.create_new_version)

    @Slot(dict)
    def existing_versions_data(self, versions_data: dict):
        self.properties_viewer_tw.clear()

        for version_name, version_details in versions_data.items():
            root_item = self.properties_viewer_tw.invisibleRootItem()
            self.add_version(root_item, version_name, version_details)

    @Slot(dict)
    def existing_app_base_data(self, app_data: dict):
        self.app_base_config_wdg.app_name_le.clear()
        self.app_base_config_wdg.app_icon_path.clear()

        self.app_base_config_wdg.app_name_le.setText(app_data["display_name"])
        self.app_base_config_wdg.app_icon_path.setText(app_data["icon"])

        if app_data["enabled"] is True:
            self.app_base_config_wdg.app_is_active.setChecked(True)
        else:
            self.app_base_config_wdg.app_is_active.setChecked(False)

    def create_new_version(self):
        name = ''
        default_config = {'envar_data': '', 'executable_path': ''}
        root_item = self.properties_viewer_tw.invisibleRootItem()
        self.add_version(root_item, name, default_config)

    def add_version(self, parent_item, item_name, item_data):
        exec_path = item_data["executable_path"]
        envar_data = item_data["envar_data"]

        item = QtWidgets.QTreeWidgetItem(parent_item)

        properties_widget = AppVersionsWidget(tree_widget=self.properties_viewer_tw)

        properties_widget.populate_properties(version_name=item_name,
                                              executable_path=exec_path,
                                              envar_data=envar_data)

        properties_widget.delete_version_btn.clicked.connect(self.delete_version)
        self.properties_viewer_tw.setItemWidget(item, 0, properties_widget)
        self.properties_viewer_tw.setItemWidget(item, 1, properties_widget.delete_version_btn)

    def extract_properties(self):
        is_active = self.app_base_config_wdg.app_is_active.isChecked()
        app_name = self.app_base_config_wdg.app_name_le.text()
        icon_path = self.app_base_config_wdg.app_icon_path.text()

        data = {"versions": {}}
        for row in range(self.properties_viewer_tw.topLevelItemCount()):
            item = self.properties_viewer_tw.topLevelItem(row)

            row_item = self.properties_viewer_tw.itemWidget(item, 0)
            version_id = row_item.version_name_le.text()
            exec_path = row_item.executable_path_le.text()
            envar_data = row_item.envar_data_pt.toPlainText()
            data["versions"][version_id] = {"executable_path": exec_path, "envar_data": envar_data}

        base_entry_schema = {"base": {"enabled": is_active,
                                      "icon": f"{icon_path}",
                                      "display_name": app_name,
                                      "versions": data["versions"]}}

        return base_entry_schema

    def delete_version(self):
        sender_button = self.sender()
        row = self.properties_viewer_tw.indexAt(sender_button.pos()).row()
        self.properties_viewer_tw.takeTopLevelItem(row)

    def clear_all_properties(self):
        self.app_base_config_wdg.app_name_le.clear()
        self.app_base_config_wdg.app_icon_path.clear()
        self.app_base_config_wdg.app_is_active.setChecked(False)
        self.properties_viewer_tw.clear()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = AppProperties()
    test_dialog.show()
    sys.exit(app.exec_())
