import sys
from PySide2 import QtWidgets, QtCore


class ImportsFromBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(ImportsFromBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setDisabled(False)
        self.setMinimumWidth(465)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Task Name", "Status", "Preview"])
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        header = self.verticalHeader()
        header.hide()
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 95)


class WorkFilesBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(WorkFilesBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setDisabled(False)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["File Name", "User", "Date"])
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        header = self.verticalHeader()
        header.hide()
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)


class PublishesBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PublishesBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setDisabled(False)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Publish Name", "Version", "Status", "Preview"])
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        header = self.verticalHeader()
        header.hide()
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)


class PublishesComponentsBuild(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(PublishesComponentsBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setDisabled(False)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Slot Name", "Status", "Notes", "Preview"])
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        header = self.verticalHeader()
        header.hide()
        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 80)
        self.setColumnWidth(2, 80)


class ContextMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ContextMenu, self).__init__(parent)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.setMinimumWidth(650)

        self.show_branch_cb = QtWidgets.QComboBox()
        self.show_branch_cb.setMinimumWidth(650)

        self.category_cb = QtWidgets.QComboBox()
        self.category_cb.setMinimumWidth(650)

        self.entry_name_cb = QtWidgets.QComboBox()
        self.entry_name_cb.setMinimumWidth(650)

        self.task_name_cb = QtWidgets.QComboBox()
        self.task_name_cb.setMinimumWidth(650)

        self.fetch_btn = QtWidgets.QPushButton("Populate Below...")
        self.fetch_btn.setMinimumWidth(650)

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name ", self.show_name_cb)
        form_layout.addRow("Show Branch", self.show_branch_cb)
        form_layout.addRow("Category", self.category_cb)
        form_layout.addRow("Entry Name", self.entry_name_cb)
        form_layout.addRow("Task Name", self.task_name_cb)
        form_layout.addRow("------>", self.fetch_btn)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        form_layout.setLabelAlignment(QtCore.Qt.AlignLeft)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(30)


class WorkMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(WorkMenu, self).__init__(parent)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.imports_from_lb = QtWidgets.QLabel("Imports From...")
        self.imports_from_tb = ImportsFromBuild()

        self.work_files_lb = QtWidgets.QLabel("Scenes Files... ")
        self.publishes_lb = QtWidgets.QLabel("Publishes... ")
        self.pub_components_lb = QtWidgets.QLabel("Pub Components...")

        self.work_files_tb = WorkFilesBuild()
        self.publishes_tb = PublishesBuild()
        self.pub_components_tb = PublishesComponentsBuild()

        self.scene_search_le = QtWidgets.QLineEdit()
        self.scene_search_le.setPlaceholderText("Search...")

        self.publish_search_le = QtWidgets.QLineEdit()
        self.publish_search_le.setPlaceholderText("Search...")

        self.setup_scene_btn = QtWidgets.QPushButton("Setup Fresh Scene")
        self.load_btn = QtWidgets.QPushButton("Load")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.load_btn)
        buttons_layout.addWidget(self.cancel_btn)

        imports_from_layout = QtWidgets.QVBoxLayout()
        imports_from_layout.addWidget(self.imports_from_lb)
        imports_from_layout.addWidget(self.imports_from_tb)
        imports_from_layout.addWidget(self.setup_scene_btn)

        work_files_layout = QtWidgets.QVBoxLayout()
        work_files_layout.addWidget(self.work_files_lb)
        work_files_layout.addWidget(self.work_files_tb)
        work_files_layout.addWidget(self.scene_search_le)

        publish_slots_layout = QtWidgets.QVBoxLayout()
        publish_slots_layout.addWidget(self.publishes_lb)
        publish_slots_layout.addWidget(self.publishes_tb)
        publish_slots_layout.addWidget(self.publish_search_le)

        pub_components_layout = QtWidgets.QVBoxLayout()
        pub_components_layout.addWidget(self.pub_components_lb)
        pub_components_layout.addWidget(self.pub_components_tb)

        pub_slots_components_layout = QtWidgets.QHBoxLayout()
        pub_slots_components_layout.addLayout(publish_slots_layout)
        pub_slots_components_layout.addLayout(pub_components_layout)

        windows_layout = QtWidgets.QVBoxLayout()
        windows_layout.addLayout(imports_from_layout)
        windows_layout.addLayout(work_files_layout)
        windows_layout.addLayout(pub_slots_components_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(windows_layout)
        main_layout.addLayout(buttons_layout)


class AssetManagerUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AssetManagerUI, self).__init__(parent)

        self.setWindowTitle("Origin Asset Manager")
        self.setMinimumWidth(800)
        self.setMaximumWidth(800)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.context_menu_wdg = ContextMenu()
        self.work_menu = WorkMenu()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.context_menu_wdg)
        main_layout.addWidget(self.work_menu)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    create_shot = AssetManagerUI()
    create_shot.show()
    sys.exit(app.exec_())