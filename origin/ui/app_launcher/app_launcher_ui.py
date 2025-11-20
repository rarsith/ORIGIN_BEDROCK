import threading
from PySide2 import QtWidgets, QtCore, QtGui

from origin.database.entities.operators import DCCBaseModel, DCCVersion
from origin.database.mongo import CollectionOperators
from origin.database.mongo_connection import MongoConnection
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler
from origin.ui.app_launcher.app_launcher_settings_ui import AppLauncherSettings


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
    def __init__(self, context: ContextHandler = None, parent=None):
        super(AppLauncher, self).__init__(parent)

        self.context_handler = None
        self.current_context = None
        if context is not None:
            self.context_handler = context

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

        self.launch_app_btn = QtWidgets.QPushButton("Start App")
        self.launch_app_btn.setMinimumHeight(30)

        self.add_app_btn = QtWidgets.QPushButton("Applications Settings...")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.launcher_tw)
        main_layout.addWidget(self.app_version_select_cb)
        main_layout.addWidget(self.launch_app_btn)
        main_layout.addWidget(self.add_app_btn)

    def context_receiver(self, context: ContextHandler):
        self.context_handler = context

    def populate_widget(self):
        self.launcher_tw.clear()

        get_applications_docs = self.get_config_data()

        rows_cnt = len(get_applications_docs)
        self.launcher_tw.setRowCount(rows_cnt)

        if get_applications_docs:
            cnt = 0
            for idx, docs_data in enumerate(get_applications_docs):
                self.app_widget_built(row=cnt, doc_data=docs_data)
                self.launcher_tw.resizeRowsToContents()
                cnt += 1

    def clear_app_widget(self):
        self.launcher_tw.clear()
        self.launch_app_btn.setText("Start App")
        self.app_version_select_cb.clear()

    def app_widget_built(self, row, doc_data=None):
        app_display_name = doc_data.name.capitalize()
        custom_item = QtWidgets.QTableWidgetItem(app_display_name)

        self.label_icon = QtWidgets.QLabel()

        self.label_icon.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap(doc_data.icon_path).scaled(20, 20)
        self.label_icon.setPixmap(pixmap)
        self.label_icon.setStyleSheet("background-color: rgba(50, 50, 50, 50);")

        self.label_text = QtWidgets.QLabel()
        self.label_text.setText(app_display_name)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_text.setFont(font)
        self.label_text.setAlignment(QtCore.Qt.AlignCenter)
        self.label_text.setStyleSheet("background-color: rgba(50, 50, 50, 50); color: rgba(200, 200, 200, 255);")

        self.launcher_tw.setCellWidget(row, 0, self.label_icon)
        self.launcher_tw.setCellWidget(row, 1, self.label_text)

        custom_item.setData(QtCore.Qt.UserRole, doc_data)

        self.launcher_tw.setItem(row, 2, custom_item)

    def get_config_data(self):
        db_ops = CollectionOperators(db_collection="Applications", database=MongoConnection().origin_setup_database())
        root_documents_docs = db_ops.get_root_documents(attrib_field="type", attrib_value="application")

        root_documents = []
        if root_documents_docs:
            for root_doc in root_documents_docs:
                doc_data_class = DCCBaseModel(**root_doc)
                root_documents.append(doc_data_class)
        return root_documents

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

    def launch_async_app(self):
        import os
        import subprocess
        exe_path = self.get_ver_exec_path()
        if exe_path:
            try:
                self.update_launch_btn()
                if self.context_handler is not None:
                    current_session = self.context_handler.snapshot_session()
                    sys_envar_upper = self.context_handler.convert_to_uppercases(current_session)
                    path_handler = OriginOSPathHandler(context=self.context_handler)
                    path_handler.create_work_folders()
                    env = os.environ.copy()
                    filtered_dict = dict(filter(lambda item: item[1] is not None, sys_envar_upper.items()))
                    env.update(filtered_dict)

                    subprocess.Popen(exe_path, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP, env=env)
                else:
                    subprocess.Popen(exe_path, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

            except Exception as e:
                print(f"No application selected!: {e}")
        else:
            print("Please select an Application to start!")

    def launch_app(self):
        threading.Thread(target=self.launch_async_app).start()

    def load_app_versions(self):
        versions = self.get_app_versions()
        if versions:
            app_current_versions_docs = []
            for version_name, version_details in versions.items():
                app_current_versions_docs.append(DCCVersion(**version_details))

            self.app_version_select_cb.clear()

            for version_doc in app_current_versions_docs:
                self.app_version_select_cb.addItem(version_doc.version, userData=version_doc)

            self.update_launch_btn()

    def get_ver_exec_path(self):
        curr_sel = self.get_current_selection()
        if curr_sel:
            curr_sel_data = self.app_version_select_cb.currentData()
            exec_path = curr_sel_data.exec_path
            return exec_path

    def get_app_versions(self):
        curr_sel = self.get_current_selection()
        if curr_sel:
            item_data = curr_sel.data(QtCore.Qt.UserRole)
            versions = item_data.versions
            return versions

    def closeEvent(self, event):
        # Disconnect signals here
        super().closeEvent(event)

    def get_current_selection(self):
        selected_rows = [index.row() for index in self.launcher_tw.selectedIndexes()]
        if selected_rows is not None:
            if len(selected_rows) != 0:
                row_id = selected_rows[0]
                item = self.launcher_tw.item(row_id, 2)
                return item


    def add_app_menu(self):
        self.ui = AppLauncherSettings()
        self.ui.show()
        self.ui.commit_btn.clicked.connect(self.populate_widget)
        self.ui.refresh_btn.clicked.connect(self.populate_widget)


class AppLauncherMainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AppLauncherMainUI, self).__init__(parent)

        self.central_widget = AppLauncher()
        self.central_widget.populate_widget()
        self.setWindowTitle(f"Origin Application Launcher")
        self.setCentralWidget(self.central_widget)


if __name__ == "__main__":
    import sys
    import os

    origin_dev_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    font = app.font()
    font.setPointSize(7)
    app.setFont(font)

    test_dialog = AppLauncherMainUI()
    test_dialog.show()
    sys.exit(app.exec_())
