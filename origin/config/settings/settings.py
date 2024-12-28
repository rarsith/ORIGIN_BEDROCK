import json
import os
import pprint
import sys
import time
from typing import ClassVar, Optional

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import QTimer

from origin.common_utils import json_utils as jutil
from pydantic import BaseModel


class UserSettingsModel(BaseModel):
    origin_projects_root: ClassVar[str] = "ORIGIN_PROJECTS_ROOT"
    ORIGIN_PROJECTS_ROOT: Optional[str] = ""

    origin_mongo_url: ClassVar[str] = "ORIGIN_MONGO_URL"
    ORIGIN_MONGO_URL: Optional[str] = ""

    origin_studio_name: ClassVar[str] = "ORIGIN_STUDIO_NAME"
    ORIGIN_STUDIO_NAME: Optional[str] = ""

    origin_initial_setup: ClassVar[str] = "ORIGIN_INITIAL_SETUP"
    ORIGIN_INITIAL_SETUP: Optional[str] = ""

    origin_sylesheet_select: ClassVar[str] = "ORIGIN_STYLESHEET_SELECT"
    ORIGIN_STYLESHEET_SELECT: Optional[str] = ""

    origin_font_size: ClassVar[str] = "ORIGIN_FONT_SIZE"
    ORIGIN_FONT_SIZE: Optional[str] = ""

    origin_font_style: ClassVar[str] = "ORIGIN_FONT_STYLE"
    ORIGIN_FONT_STYLE: Optional[str] = ""

    origin_lib_project_root: ClassVar[str] = "ORIGIN_LIB_PROJECT_ROOT"
    ORIGIN_LIB_PROJECT_ROOT: Optional[str] = ""

    model_config = {
        "from_attributes": True,
    }


class CustomEnvarWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CustomEnvarWidget, self).__init__(parent)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.envar_name_le = QtWidgets.QLineEdit()
        self.envar_value_le = QtWidgets.QLineEdit()
        self.remove_btn = QtWidgets.QPushButton("Remove")

    def create_layout(self):
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.remove_btn)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.envar_name_le)
        main_layout.addWidget(self.envar_value_le)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        pass


class SettingsUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsUI, self).__init__(parent)

        self.mongo_url_data = None
        self.origin_dev_data = None
        self.origin_projects_data = None
        self.origin_studio_name = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.populate_widget()

    def create_widgets(self):
        self.main_envars_wdg = QtWidgets.QWidget()
        self.custom_envar_table = QtWidgets.QTableWidget()
        self.custom_envar_table.setColumnCount(3)
        self.custom_envar_table.setHorizontalHeaderLabels(["Variable", "Value", "Remove"])
        self.custom_envar_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.mongo_url_le = QtWidgets.QLineEdit()

        self.studio_name_le = QtWidgets.QLineEdit()
        # self.origin_dev_root_le = QtWidgets.QLineEdit()
        self.origin_projects_root_le = QtWidgets.QLineEdit()
        self.origin_projects_lib_root_le = QtWidgets.QLineEdit()
        self.origin_look_cb = QtWidgets.QComboBox()

        self.origin_font_style_cb = QtWidgets.QComboBox()
        self.origin_font_size_cb = QtWidgets.QComboBox()
        font_sizes = ["6", "7", "8", "9", "10", "11", "12", "13", "14"]
        self.origin_font_size_cb.addItems(font_sizes)

        self.custom_envar_name_le = QtWidgets.QLineEdit()
        self.custom_envar_value_le = QtWidgets.QLineEdit()

        self.browse_origin_dev_root = QtWidgets.QPushButton("...")
        self.browse_origin_proj_root = QtWidgets.QPushButton("...")
        self.browse_origin_lib_proj_root = QtWidgets.QPushButton("...")

        self.add_envar_btn = QtWidgets.QPushButton("Add")

        self.checkbox_ckb = QtWidgets.QCheckBox()

        self.message_area = QtWidgets.QTextEdit()
        self.message_area.setPlaceholderText("FEEDBACK")
        self.message_area.setReadOnly(True)

        self.save_settings_btn = QtWidgets.QPushButton("Save")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        origin_proj_root_layout = QtWidgets.QHBoxLayout()
        origin_proj_root_layout.addWidget(self.origin_projects_root_le)
        origin_proj_root_layout.addWidget(self.browse_origin_proj_root)

        origin_lib_proj_root_layout = QtWidgets.QHBoxLayout()
        origin_lib_proj_root_layout.addWidget(self.origin_projects_lib_root_le)
        origin_lib_proj_root_layout.addWidget(self.browse_origin_lib_proj_root)

        mandatory_variables_layout = QtWidgets.QFormLayout()
        mandatory_variables_layout.addRow("Mongo Database URL", self.mongo_url_le)
        mandatory_variables_layout.addRow("Studio Name", self.studio_name_le)
        mandatory_variables_layout.addRow("Color Scheme", self.origin_look_cb)
        mandatory_variables_layout.addRow("Font Style", self.origin_font_style_cb)
        mandatory_variables_layout.addRow("Font Size", self.origin_font_size_cb)
        mandatory_variables_layout.addRow("Origin Projects ROOT", origin_proj_root_layout)
        mandatory_variables_layout.addRow("Origin Library ROOT", origin_lib_proj_root_layout)

        custom_envar_buttons_layout = QtWidgets.QHBoxLayout()
        custom_envar_buttons_layout.addWidget(self.add_envar_btn)

        custom_envars_layout = QtWidgets.QVBoxLayout()
        custom_envars_layout.addWidget(self.custom_envar_table)
        custom_envars_layout.addLayout(custom_envar_buttons_layout)
        custom_envars_layout.addWidget(self.message_area)


        control_buttons_layout = QtWidgets.QHBoxLayout()
        control_buttons_layout.addWidget(self.cancel_btn)
        control_buttons_layout.addWidget(self.save_settings_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(mandatory_variables_layout)
        main_layout.addLayout(custom_envars_layout)
        main_layout.addLayout(control_buttons_layout)

    def create_connections(self):
        self.browse_origin_proj_root.clicked.connect(self.open_origin_proj_path)
        self.browse_origin_lib_proj_root.clicked.connect(self.open_origin_lib_proj_path)
        self.save_settings_btn.clicked.connect(self.save_user_settings)

    def open_origin_lib_proj_path(self):
        import os
        home_path = os.path.expanduser("~")
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder",
                                                               home_path,
                                                               QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)

        if file_path:
            self.origin_projects_lib_root_le.setText(file_path)

    def open_origin_proj_path(self):
        import os
        home_path = os.path.expanduser("~")
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder",
                                                               home_path,
                                                               QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)

        if file_path:
            self.origin_projects_root_le.setText(file_path)

    def collect_from_widget(self):
        pass

    def populate_widget(self):
        origin_dev_root = os.getenv("ORIGIN_ROOT")
        user_setting_file_path = os.path.normpath(
            os.path.join(origin_dev_root, "origin/config/settings/user_settings.json"))
        user_setting_file = jutil.open_json(user_setting_file_path)
        settings_model = UserSettingsModel(**user_setting_file)

        self.mongo_url_le.setText(settings_model.ORIGIN_MONGO_URL)
        self.studio_name_le.setText(settings_model.ORIGIN_STUDIO_NAME)
        self.origin_look_cb.setCurrentText(settings_model.ORIGIN_STYLESHEET_SELECT)
        self.origin_font_style_cb.setCurrentText(settings_model.ORIGIN_FONT_STYLE)
        self.origin_font_size_cb.setCurrentText(settings_model.ORIGIN_FONT_SIZE)
        self.origin_projects_root_le.setText(settings_model.ORIGIN_PROJECTS_ROOT)
        self.origin_projects_lib_root_le.setText(settings_model.ORIGIN_LIB_PROJECT_ROOT)

    def convert_path(self, input_path: str) -> str:
        target_sep = os.sep
        normalized_path = os.path.normpath(input_path)

        converted_path = normalized_path.replace('\\', '/').replace('/', target_sep)
        return converted_path

    def save_user_settings(self):
        origin_dev_root = os.getenv("ORIGIN_ROOT")
        user_setting_file_path = os.path.normpath(
            os.path.join(origin_dev_root, "origin/config/settings/user_settings.json"))

        projects_root_path = self.origin_projects_root_le.text()
        projects_root_os_path = self.convert_path(projects_root_path)

        lib_projects_root_path = self.origin_projects_lib_root_le.text()
        lib_projects_root_os_path = self.convert_path(lib_projects_root_path)

        user_settings = {
            "ORIGIN_PROJECTS_ROOT": projects_root_os_path,
            "ORIGIN_MONGO_URL": self.mongo_url_le.text(),
            "ORIGIN_STUDIO_NAME": self.studio_name_le.text(),
            "ORIGIN_STYLESHEET_SELECT": self.origin_look_cb.currentText(),
            "ORIGIN_INITIAL_SETUP": "1",
            "ORIGIN_FONT_SIZE": self.origin_font_size_cb.currentText(),
            "ORIGIN_FONT_STYLE": self.origin_font_style_cb.currentText(),
            "ORIGIN_LIB_PROJECT_ROOT": lib_projects_root_os_path
        }

        split_path_file = os.path.split(user_setting_file_path)
        jutil.write_json(target_path=split_path_file[0], data=user_settings, target_file="user_settings")
        formatted_text = self.format_dict_as_html(user_settings)
        self.message_area.clear()
        QTimer.singleShot(400, lambda: (self.message_area.setHtml(formatted_text)))
        # self.message_area.setHtml(formatted_text)


    def format_dict_as_html(self, data):
        # Convert dictionary to HTML string with bold keys
        html_lines = ["<b style='color:green;'>Origin Settings Updated!</b><br>"]
        for key, value in data.items():
            html_lines.append(f"<b>{key}</b>: --> {value}.....<b style='color:green;'>OK</b><br>")
        return "<br>".join(html_lines)

    def cancel_ops(self):
        self.close()
        self.deleteLater()

class SettingsMainUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(SettingsMainUI, self).__init__(parent)

        self.central_widget = SettingsUI()
        self.setWindowTitle(f"Origin Settings")
        self.setCentralWidget(self.central_widget)

        self.setMinimumWidth(800)
        self.setMinimumHeight(800)

        self.create_connections()

    def create_connections(self):
        self.central_widget.cancel_btn.clicked.connect(lambda: self.close())


if __name__ == "__main__":
    origin_dev_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

    try:
        test_dialog.close()
        test_dialog.deleteLater()
    except:
        pass

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    font = app.font()
    font.setPointSize(7)
    app.setFont(font)

    test_dialog = SettingsMainUI()
    test_dialog.show()
    sys.exit(app.exec_())
