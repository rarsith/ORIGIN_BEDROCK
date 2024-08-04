from PySide2 import QtWidgets, QtCore, QtGui
from ui.app_launcher.app_launcher_settings_ui import AppLauncherSettings


class AppWidget(QtWidgets.QWidget):
    def __init__(self,  parent=None):
        super(AppWidget, self).__init__(parent)


class IconTextWidget(QtWidgets.QWidget):
    def __init__(self, text, icon_path, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label_icon = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(icon_path).scaled(256, 256)
        self.label_icon.setPixmap(pixmap)

        self.label_text = QtWidgets.QLabel(text)

        layout.addWidget(self.label_icon)
        layout.addWidget(self.label_text)

class AppLauncher(QtWidgets.QWidget):
    def __init__(self, config_file_path=None, parent=None):
        super(AppLauncher, self).__init__(parent)

        self.config_file_path = config_file_path

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        # self.populate_widget()

    def create_widgets(self):
        self.launcher_tw = QtWidgets.QTableWidget()

        self.launcher_tw.setColumnCount(3)
        self.launcher_tw.setColumnWidth(0, 20)
        self.launcher_tw.setColumnWidth(1, 70)
        self.launcher_tw.setColumnHidden(2, True)

        self.launcher_tw.setShowGrid(False)
        self.launcher_tw.setFocusPolicy(QtCore.Qt.NoFocus)
        self.launcher_tw.horizontalHeader().setVisible(False)
        self.launcher_tw.verticalHeader().setVisible(False)

        self.launcher_tw.horizontalHeader().setStretchLastSection(True)

        self.launcher_tw.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.launcher_tw.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.launcher_tw.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.app_version_select_cb = QtWidgets.QComboBox()
        self.app_version_select_cb.setMinimumHeight(30)
        delegate = QtWidgets.QStyledItemDelegate(self.app_version_select_cb)
        self.app_version_select_cb.setItemDelegate(delegate)


        # self.app_version_select_cb.setAlignment(QtCore.Qt.AlignCenter)

        self.launch_app_btn = QtWidgets.QPushButton("Start App")
        self.launch_app_btn.setMinimumHeight(30)

        self.add_app_btn = QtWidgets.QPushButton("Add App...")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.launcher_tw)
        main_layout.addWidget(self.app_version_select_cb)
        main_layout.addWidget(self.launch_app_btn)
        main_layout.addWidget(self.add_app_btn)

    def populate_widget(self):
        self.launcher_tw.clear()

        get_apps = self.get_config_data(app_config_file=self.config_file_path)

        rows_cnt = len(get_apps)
        self.launcher_tw.setRowCount(rows_cnt)

        if get_apps:
            cnt = 0
            for keys, values in get_apps.items():
                app_display_name = keys.capitalize()
                app_icon = values["icon"]

                self.app_widget_built(name=app_display_name,
                                      row=cnt,
                                      icon_path=app_icon,
                                      custom_data={keys: values})

                self.launcher_tw.resizeRowsToContents()
                cnt += 1

    def clear_app_widget(self):
        self.launcher_tw.clear()
        self.launch_app_btn.setText("Start App")
        self.app_version_select_cb.clear()


    def app_widget_built(self, name, row, icon_path, custom_data=None):
        custom_item = QtWidgets.QTableWidgetItem(name)

        self.label_icon = QtWidgets.QLabel()

        self.label_icon.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap(icon_path).scaled(20, 20)
        self.label_icon.setPixmap(pixmap)
        self.label_icon.setStyleSheet("background-color: rgba(50, 50, 50, 50);")

        self.label_text = QtWidgets.QLabel()
        self.label_text.setText(name)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_text.setFont(font)
        self.label_text.setAlignment(QtCore.Qt.AlignCenter)
        self.label_text.setStyleSheet("background-color: rgba(50, 50, 50, 50); color: rgba(200, 200, 200, 255);")

        self.launcher_tw.setCellWidget(row, 0, self.label_icon)
        self.launcher_tw.setCellWidget(row, 1, self.label_text)

        if custom_data:
            custom_item.setData(QtCore.Qt.UserRole, custom_data)

        self.launcher_tw.setItem(row, 2, custom_item)

    def get_config_data(self, app_config_file=None):
        from common_utils import json_utils
        config_data = json_utils.open_json(app_config_file)
        return config_data["applications"]

    def create_connections(self):
        self.add_app_btn.clicked.connect(self.add_app_menu)
        self.launcher_tw.itemSelectionChanged.connect(self.load_app_versions)
        self.app_version_select_cb.currentIndexChanged.connect(self.update_launch_btn)
        self.launch_app_btn.clicked.connect(self.launch_app)

    def update_launch_btn(self):
        curr_sel = self.get_current_selection()
        if curr_sel:
            current_app = curr_sel.text()
            current_version = self.app_version_select_cb.currentText()

            if current_app and current_version:
                self.launch_app_btn.setText(f"Launch - {current_app} - {current_version}")
        else:
            self.clear_app_widget()

    def launch_app(self):
        import subprocess
        exe_path = self.get_ver_exec_path()
        self.update_launch_btn()
        subprocess.Popen(exe_path, shell=True)

    def load_app_versions(self):
        versions = self.get_app_versions()
        if versions:
            app_current_versions = []
            for version_name, version_details in versions.items():
                app_current_versions.append(version_name)

            self.app_version_select_cb.clear()
            self.app_version_select_cb.addItems(app_current_versions)
            self.update_launch_btn()


    def get_ver_exec_path(self):
        curr_sel = self.get_current_selection()
        if curr_sel:
            item_data = curr_sel.data(QtCore.Qt.UserRole)
            curr_sel_ver = self.app_version_select_cb.currentText()
            exe_path = item_data[curr_sel.text().lower()]["versions"][curr_sel_ver]["executable_path"]

            return exe_path

    def get_app_versions(self):
        curr_sel = self.get_current_selection()
        if curr_sel:
            item_data = curr_sel.data(QtCore.Qt.UserRole)
            versions = item_data[curr_sel.text().lower()]["versions"]
            return versions

    def get_current_selection(self):
        selected_rows = [index.row() for index in self.launcher_tw.selectedIndexes()]
        if selected_rows is not None:
            if len(selected_rows) != 0:
                row_id = selected_rows[0]
                item = self.launcher_tw.item(row_id, 2)
                return item


    def add_app_menu(self):
        self.ui = AppLauncherSettings(config_file_path=self.config_file_path)
        self.ui.show()
        self.ui.commit_btn.clicked.connect(self.populate_widget)
        self.ui.refresh_btn.clicked.connect(self.populate_widget)


if __name__ == "__main__":
    import sys

    APP_CONFIG_FILE =  r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\config\applications\config_applications.json"

    qss_style_file = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\ui\style\stylesheets\dark_orange\dark_orange_style.qss"

    app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)



    test_dialog = AppLauncher(config_file_path=APP_CONFIG_FILE)
    test_dialog.populate_widget()
    test_dialog.show()
    sys.exit(app.exec_())