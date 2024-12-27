import os
import sys

from PySide2 import QtWidgets, QtCore, QtGui


class CustomEnvarWidget(QtWidgets.QWidget):
    def __init__(self,  parent=None):
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
    origin_mandatory_envars = {"ORIGIN_ROOT": "",
                               "ORIGIN_PROJECTS_ROOT": "",
                               "ORIGIN_INITIAL_SETUP": "",
                               "ORIGIN_MONGO_URL": "",
                               "ORIGIN_STUDIO_NAME": ""}

    def __init__(self,  parent=None):
        super(SettingsUI, self).__init__(parent)

        self.mongo_url_data = None
        self.origin_dev_data = None
        self.origin_projects_data = None
        self.origin_studio_name = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.main_envars_wdg = QtWidgets.QWidget()
        self.custom_envar_table = QtWidgets.QTableWidget()
        self.custom_envar_table.setColumnCount(3)
        self.custom_envar_table.setHorizontalHeaderLabels(["Variable", "Value", "Remove"])
        self.custom_envar_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.mongo_url_le = QtWidgets.QLineEdit()

        self.studio_name_le = QtWidgets.QLineEdit()
        self.origin_dev_root_le = QtWidgets.QLineEdit()
        self.origin_projects_root_le = QtWidgets.QLineEdit()

        self.custom_envar_name_le = QtWidgets.QLineEdit()
        self.custom_envar_value_le = QtWidgets.QLineEdit()

        self.browse_origin_dev_root = QtWidgets.QPushButton("...")
        self.browse_origin_proj_root = QtWidgets.QPushButton("...")

        self.add_envar_btn = QtWidgets.QPushButton("Add")

        self.checkbox_ckb = QtWidgets.QCheckBox()

        self.save_settings_btn = QtWidgets.QPushButton("Save")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        origin_dev_root_layout = QtWidgets.QHBoxLayout()
        origin_dev_root_layout.addWidget(self.origin_dev_root_le)
        origin_dev_root_layout.addWidget(self.browse_origin_dev_root)

        origin_proj_root_layout = QtWidgets.QHBoxLayout()
        origin_proj_root_layout.addWidget(self.origin_projects_root_le)
        origin_proj_root_layout.addWidget(self.browse_origin_proj_root)


        mandatory_variables_layout = QtWidgets.QFormLayout()
        mandatory_variables_layout.addRow("MONGO URL", self.mongo_url_le)
        mandatory_variables_layout.addRow("STUDIO NAME", self.studio_name_le)
        mandatory_variables_layout.addRow("ORIGIN DEV ROOT", origin_dev_root_layout)
        mandatory_variables_layout.addRow("ORIGIN PROJECTS ROOT", origin_proj_root_layout)

        custom_envar_buttons_layout = QtWidgets.QHBoxLayout()
        custom_envar_buttons_layout.addWidget(self.add_envar_btn)

        custom_envars_layout = QtWidgets.QVBoxLayout()
        custom_envars_layout.addWidget(self.custom_envar_table)
        custom_envars_layout.addLayout(custom_envar_buttons_layout)

        control_buttons_layout = QtWidgets.QHBoxLayout()
        control_buttons_layout.addWidget(self.cancel_btn)
        control_buttons_layout.addWidget(self.save_settings_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(mandatory_variables_layout)
        main_layout.addLayout(custom_envars_layout)
        main_layout.addLayout(control_buttons_layout)

    def create_connections(self):
        self.browse_origin_dev_root.clicked.connect(self.open_origin_dev_path)
        self.browse_origin_proj_root.clicked.connect(self.open_origin_proj_path)

    def open_origin_dev_path(self):
        import os
        get_origin_root = os.getenv("ORIGIN_PROJECTS_ROOT")
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select File",
                                                                 get_origin_root,
                                                                 QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)

        if file_path:
             self.origin_dev_root_le.setText(file_path)

    def open_origin_proj_path(self):
        import os
        get_origin_root = os.getenv("ORIGIN_PROJECTS_ROOT")
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select File",
                                                                 get_origin_root,
                                                                 QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)

        if file_path:
            self.origin_dev_root_le.setText(file_path)

    def collect_from_widget(self):
        pass


    def populate_widget(self):
        pass
        # for envar_name, envar_value in self.origin_mandatory_envars.items():
        #     if envar_name in os.environ:
        #          = os.environ["MAYA_SCRIPT_PATH"]
        #         if unix_path not in maya_scripts_dir.split(";"):
        #             os.environ["MAYA_SCRIPT_PATH"] = maya_scripts_dir + unix_path
        #     else:
        #         os.environ["MAYA_SCRIPT_PATH"] = unix_path


class SettingsMainUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(SettingsMainUI, self).__init__(parent)

        self.central_widget = SettingsUI()
        self.setWindowTitle(f"Origin Settings")
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    origin_dev_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

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
    exit_code = app.exec_()
    sys.exit(exit_code)


