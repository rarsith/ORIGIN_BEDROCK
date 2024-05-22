import sys
from PySide2 import QtWidgets, QtCore
from envars.origin_envars import OriginEnvar
from context_manager.origin_session import ContextHandler
from ui.odb_main_publishes_view_core import MainPublishesViewCore
from ui.odb_project_tree_viewer_core import ProjectTreeViewerCore
from ui.odb02_task_viewer_core import TaskViewerCore
from ui.entity_properties_ui.properties_viewer import PropertiesViewer
from ui.app_launcher.app_launcher_ui import AppLauncher
from ui.odb_sanity_checker_wdg import SanityChecker

APP_CONFIG_FILE = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\config\applications\config_applications.json"
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

        self.show_view_twd.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_task_viewer)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_task_viewer)

        self.show_view_twd.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_main_publishes)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_main_publishes)

        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_entry_properties)
        self.show_view_twd.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_entry_properties)


        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_shows)
        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_tree_widget)

        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.launcher_tw.populate_widget)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.clear_launch_app_wdg)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_task_versions)

        self.middle_tabmenu_tab.currentChanged.connect(self.on_middle_tab_change)
        self.entity_details_viewer_wdg.details_tabmenu_tab.currentChanged.connect(self.on_properties_tab_change)

        self.show_view_twd.show_select_cb.currentIndexChanged.connect(self.show_context)
        self.show_view_twd.project_tree_viewer_wdg.itemSelectionChanged.connect(self.show_context)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.show_context)

    def set_proj_tree_focus(self):
        self.show_view_twd.setFocus()

    def set_task_viewer_focus(self):
        self.tasks_view_lwd.setFocus()

    def show_context(self):
        con = OriginEnvar().resolve_to_full_context()
        # print(con)
        return con

    def on_middle_tab_change(self, index):
        current_widget = self.middle_tabmenu_tab.widget(index)
        if current_widget:
            if current_widget == self.tasks_view_lwd:
                self.populate_task_viewer()
            else:
                self.tasks_view_lwd.task_viewer_wdg.clearSelection()
                self.tasks_view_lwd.task_viewer_wdg.clear()

            if current_widget == self.versions_view_tvw:
                self.populate_main_publishes()
            else:
                self.versions_view_tvw.publish_view_tw.clearSelection()
                self.versions_view_tvw.publish_view_tw.clear()

    def on_properties_tab_change(self, index):
        current_widget = self.entity_details_viewer_wdg.details_tabmenu_tab.widget(index)
        if current_widget:
            if current_widget == self.entity_details_viewer_wdg.versions_wdg:
                self.populate_task_versions()
            else:
                self.entity_details_viewer_wdg.versions_wdg.publish_view_tw.clearSelection()
                self.entity_details_viewer_wdg.versions_wdg.publish_view_tw.clear()

            if current_widget == self.entity_details_viewer_wdg.components_wdg:
                pass

            else:
                pass

            if current_widget == self.entity_details_viewer_wdg.links_wdg:
                pass

            else:
                pass

            if current_widget == self.entity_details_viewer_wdg.notes_wdg:
                pass

            else:
                pass

            if current_widget == self.entity_details_viewer_wdg.properties_wdg:
                self.populate_entry_properties()

            else:
                self.entity_details_viewer_wdg.properties_wdg.properties_viewer.clear()

    def populate_main_publishes(self):
        has_selection = self.show_view_twd.get_selected()
        if len(has_selection) != 0:
            tab_idx = self.middle_tabmenu_tab.currentIndex()
            current_widget = self.middle_tabmenu_tab.widget(tab_idx)
            if current_widget:
                if current_widget == self.versions_view_tvw:
                    self.versions_view_tvw.populate_widget()
        else:

            self.show_view_twd.project_tree_viewer_wdg.clearSelection()
            self.versions_view_tvw.publish_view_tw.clear()

    def populate_task_viewer(self):
        has_selection = self.show_view_twd.get_selected()
        if len(has_selection) != 0:
            tab_idx = self.middle_tabmenu_tab.currentIndex()
            current_widget = self.middle_tabmenu_tab.widget(tab_idx)
            if current_widget:
                if current_widget == self.tasks_view_lwd:
                    self.tasks_view_lwd.populate_widget()
        else:

            self.show_view_twd.project_tree_viewer_wdg.clearSelection()
            self.tasks_view_lwd.task_viewer_wdg.clear()

    def populate_task_versions(self):
        widget_selection = self.tasks_view_lwd.get_current_selected()
        if len(widget_selection) != 0:
            tab_idx = self.entity_details_viewer_wdg.details_tabmenu_tab.currentIndex()
            current_widget = self.entity_details_viewer_wdg.details_tabmenu_tab.widget(tab_idx)
            if current_widget:
                if current_widget == self.entity_details_viewer_wdg.versions_wdg:
                    self.entity_details_viewer_wdg.versions_wdg.populate_widget()
        else:
            self.entity_details_viewer_wdg.versions_wdg.publish_view_tw.clearSelection()
            self.entity_details_viewer_wdg.versions_wdg.publish_view_tw.clear()

    def clear_launch_app_wdg(self):
        widget_selection = self.tasks_view_lwd.get_current_selected()
        if len(widget_selection) == 0:
            self.launcher_tw.clear_app_widget()
            self.tasks_view_lwd.task_viewer_wdg.clearSelection()

    def populate_entry_properties(self):
        widget_selection = self.show_view_twd.get_selected()
        if len(widget_selection) != 0:
            tab_idx = self.entity_details_viewer_wdg.details_tabmenu_tab.currentIndex()
            current_widget = self.entity_details_viewer_wdg.details_tabmenu_tab.widget(tab_idx)
            if current_widget:
                if current_widget == self.entity_details_viewer_wdg.properties_wdg:
                    self.entity_details_viewer_wdg.properties_wdg.populate_properties_list()
        else:
            self.entity_details_viewer_wdg.properties_wdg.properties_viewer.clear()


class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)

        self.setWindowTitle(f"ORIGIN")

        self.central_widget = OriginControlCenterUI()

        self.setCentralWidget(self.central_widget)

        self.show()



if __name__ == "__main__":
    qss_style_file = "ui/style/stylesheets/dark_orange/dark_orange_style.qss"

    app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    test_dialog = MainUI()



    # test_dialog.show()
    sys.exit(app.exec_())
