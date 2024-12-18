import json
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Slot
from origin.database.entities.operators import DCCVersion, DCCBaseModel


class AppVersionsWidget(QtWidgets.QWidget):
    def __init__(self, tree_widget=None, parent=None):
        super(AppVersionsWidget, self).__init__(parent)

        self.tree_widget = tree_widget

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.version_name_le = QtWidgets.QLineEdit()
        self.executable_path_le = QtWidgets.QLineEdit()
        self.executable_python_path_le = QtWidgets.QLineEdit()
        self.active_chk = QtWidgets.QCheckBox()
        # self.active_plugins = QtWidgets.QLineEdit()
        self.browse_executable_btn = QtWidgets.QPushButton("Browse")
        self.envar_data_pt = QtWidgets.QPlainTextEdit()
        self.envar_data_pt.setMaximumHeight(50)
        self.envar_data_pt.setMaximumWidth(250)
        self.delete_version_btn = QtWidgets.QPushButton("X")
        self.delete_version_btn.setFixedSize(60, 180)

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Version: ", self.version_name_le)
        form_layout.addRow("Active:", self.active_chk)
        form_layout.addRow("Executable Path:", self.executable_path_le)
        form_layout.addRow("Python Executable:", self.executable_python_path_le)
        # form_layout.addRow("Active Plugins:", self.executable_path_le)
        form_layout.addRow("Environment:", self.envar_data_pt)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(form_layout)

    def create_connections(self):
        self.delete_version_btn.clicked.connect(self.delete_item)

    def delete_item(self):
        index = self.tree_widget.indexOfTopLevelItem(self.parent())

        if index != -1:
            self.tree_widget.takeTopLevelItem(index)

    def populate_properties(self,
                            version_name=None,
                            active=True,
                            executable_path=None,
                            python_executable=None,
                            envar_data=None):
        self.version_name_le.setText(version_name)
        self.active_chk.setChecked(active)
        self.executable_path_le.setText(executable_path)
        self.executable_python_path_le.setText(python_executable)
        self.envar_data_pt.insertPlainText(str(envar_data))


class AppPropertiesWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AppPropertiesWidget, self).__init__(parent)

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
        self.selected_app: DCCBaseModel = None

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

        self.app_base_config_wdg = AppPropertiesWidget()
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
    def existing_versions_data(self, doc_data):
        self.selected_app = doc_data
        self.existing_app_base_data()
        self.populate_versions()

    def extract_versions(self):
        return self.selected_app.versions

    def populate_versions(self):
        versions_objects = self.extract_versions()
        self.properties_viewer_tw.clear()
        for version_name, version_properties in versions_objects.items():
            version_doc_data = DCCVersion(**version_properties)
            self.add_version(doc_data=version_doc_data)

    def existing_app_base_data(self):
        self.app_base_config_wdg.app_name_le.clear()
        self.app_base_config_wdg.app_icon_path.clear()

        self.app_base_config_wdg.app_name_le.setText(self.selected_app.name)
        self.app_base_config_wdg.app_icon_path.setText(self.selected_app.icon_path)

        if self.selected_app.active is True:
            self.app_base_config_wdg.app_is_active.setChecked(True)
        else:
            self.app_base_config_wdg.app_is_active.setChecked(False)

    def create_new_version(self):
        version_document = DCCVersion(
            active=False,
            version='',
            exec_path='',
            exec_python='',
            envars='{}'
        )

        self.add_version(doc_data=version_document)

    def add_version(self, doc_data):
        root_item = self.properties_viewer_tw.invisibleRootItem()
        item = QtWidgets.QTreeWidgetItem(root_item)

        properties_widget = AppVersionsWidget(tree_widget=self.properties_viewer_tw)

        properties_widget.populate_properties(version_name=doc_data.version,
                                              active=doc_data.active,
                                              executable_path=doc_data.exec_path,
                                              python_executable=doc_data.exec_python,
                                              envar_data=doc_data.envars)

        properties_widget.delete_version_btn.clicked.connect(self.delete_version)
        self.properties_viewer_tw.setItemWidget(item, 0, properties_widget)
        self.properties_viewer_tw.setItemWidget(item, 1, properties_widget.delete_version_btn)

    def extract_properties(self):
        is_active = self.app_base_config_wdg.app_is_active.isChecked()
        app_name = self.app_base_config_wdg.app_name_le.text()
        icon_path = self.app_base_config_wdg.app_icon_path.text()

        data = {"versions_data": {}}

        for row in range(self.properties_viewer_tw.topLevelItemCount()):
            item = self.properties_viewer_tw.topLevelItem(row)

            row_item = self.properties_viewer_tw.itemWidget(item, 0)
            version_id = row_item.version_name_le.text()
            version_is_active = row_item.active_chk.isChecked()
            exec_path = row_item.executable_path_le.text()
            exec_python_path = row_item.executable_python_path_le.text()
            envar_data = row_item.envar_data_pt.toPlainText()
            collected_version_data = DCCVersion(
                active=version_is_active,
                version=version_id,
                exec_path=exec_path,
                exec_python=exec_python_path,
                envars=envar_data
            )
            collected_version_dict = collected_version_data.model_dump()

            data["versions_data"][version_id] = collected_version_dict

        base_entry_schema = {"base": {"enabled": is_active,
                                      "icon": f"{icon_path}",
                                      "display_name": app_name,
                                      "versions": data["versions_data"]}}

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
