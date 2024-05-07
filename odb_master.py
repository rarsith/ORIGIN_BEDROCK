import sys
from PySide2 import QtWidgets, QtCore

from ui.odb_main_publishes_view_core import MainPublishesViewCore
from ui.odb_project_tree_viewer_core import ProjectTreeViewerCore
from ui.odb02_task_viewer_core import TaskViewerCore
from ui.properties_ui.properties_viewer import PropertiesViewer
from ui.app_launcher.app_launcher_ui import AppLauncher
from ui.odb_sanity_checker_wdg import SanityChecker

APP_CONFIG_FILE = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\ui\origin_globals_ui\settings\applications004.json"
thumbnail_path = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\dcc\icons\movie_pic.png"

class OriginControlCenterUI(QtWidgets.QWidget):
    WINDOW_TITLE = "Origin Control Center"

    def __init__(self):
        super(OriginControlCenterUI, self).__init__()

        self.setWindowTitle(self.WINDOW_TITLE)

        self.setMinimumHeight(850)
        self.setMinimumWidth(1700)

        self.create_widgets()

        self.create_layout()
        self.create_connections()
        self.populate_main_publishes()

    def create_widgets(self):
        self.sanity_checker_wdg = SanityChecker()
        self.launcher_tw = AppLauncher(config_file_path=APP_CONFIG_FILE)
        self.show_view_twd = ProjectTreeViewerCore()
        self.tasks_view_lwd = TaskViewerCore()
        self.versions_view_tvw = MainPublishesViewCore()
        self.entity_details_viewer_wdg = PropertiesViewer()
        self.entity_details_viewer_wdg.set_thumbnail_icon(icon_path=thumbnail_path)

        self.middle_tabmenu_tab = QtWidgets.QTabWidget()
        self.middle_tabmenu_tab.addTab(self.tasks_view_lwd, "Tasks")
        self.middle_tabmenu_tab.addTab(self.versions_view_tvw, "Publishes")

        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        sanity_checker_widget = QtWidgets.QWidget()
        middle_tab_widget = QtWidgets.QWidget()

        sanity_checker_layout = QtWidgets.QVBoxLayout()
        middle_tab_layout = QtWidgets.QVBoxLayout()

        sanity_checker_layout.addWidget(self.sanity_checker_wdg)
        middle_tab_layout.addWidget(self.middle_tabmenu_tab)

        sanity_checker_widget.setLayout(sanity_checker_layout)
        middle_tab_widget.setLayout(middle_tab_layout)

        horizontal_splitter = QtWidgets.QSplitter()
        horizontal_splitter.setOrientation(QtCore.Qt.Vertical)

        horizontal_splitter.insertWidget(0, sanity_checker_widget)
        horizontal_splitter.insertWidget(1, middle_tab_widget)
        horizontal_splitter.setSizes([150, 700])

        views_layout = QtWidgets.QHBoxLayout()
        views_layout.setContentsMargins(2, 2, 2, 2)
        views_layout.setSpacing(0)

        vertical_splitter = QtWidgets.QSplitter()
        vertical_splitter.setOrientation(QtCore.Qt.Horizontal)
        views_layout.addWidget(vertical_splitter)

        app_launcher_splitter = QtWidgets.QSplitter()
        app_launcher_splitter.setOrientation(QtCore.Qt.Horizontal)
        app_launcher_splitter.addWidget(vertical_splitter)

        vertical_splitter.insertWidget(0, self.show_view_twd)
        vertical_splitter.insertWidget(1, horizontal_splitter)
        vertical_splitter.insertWidget(2, self.entity_details_viewer_wdg)
        vertical_splitter.insertWidget(3, self.launcher_tw)
        vertical_splitter.setSizes([100, 950, 350, 150])

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(views_layout)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.show_view_twd.show_select_cb.currentIndexChanged.connect(self.populate_main_publishes)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_task_viewer)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.get_entry_properties)
        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_shows)
        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_tree_widget)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.launcher_tw.populate_widget)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.clear_launch_app_wdg)


    def populate_main_publishes(self):
        main_pub_show_name = self.show_view_twd.show_select_cb.currentText()
        main_pub_branch_name = ''
        main_pub_category_name = ''
        main_pub_entry_name = ''
        main_pub_task_name = ''

        try:
            main_pub_branch_name = self.show_view_twd.get_sel_data()[1]
            main_pub_category_name = self.show_view_twd.get_sel_data()[2]
            main_pub_entry_name = self.show_view_twd.get_sel_data()[3]
            main_pub_task_name = self.tasks_view_lwd.get_selected_task()
        except:
            pass

        self.versions_view_tvw.show_name = main_pub_show_name
        self.versions_view_tvw.branch_name = main_pub_branch_name
        self.versions_view_tvw.category_name = main_pub_category_name
        self.versions_view_tvw.entry_name = main_pub_entry_name
        self.versions_view_tvw.task_name = main_pub_task_name
        self.versions_view_tvw.populate_main_widget()
        self.versions_view_tvw.publish_view_tw.clearSelection()

    def clear_launch_app_wdg(self):
        widget_selection = self.tasks_view_lwd.get_current_selected()
        if len(widget_selection) == 0:
            self.launcher_tw.clear_app_widget()

    def populate_task_viewer(self):
        self.tasks_view_lwd.populate_tasks()

    def get_entry_properties(self):
        self.entity_details_viewer_wdg.properties_wdg.populate_properties_list()

class MainUI(QtWidgets.QMainWindow):
    WINDOW_TITLE = "ORIGIN"

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setWindowTitle(self.WINDOW_TITLE)

        central_widget = OriginControlCenterUI()
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    qss_style_file = "ui/stylesheets/dark_orange/dark_orange_style.qss"

    app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    test_dialog = MainUI()
    test_dialog.show()
    sys.exit(app.exec_())
