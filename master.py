import os
import sys

from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QIcon

from origin.config.sessions.session_manager import SessionManager
from origin.envars.origin_envars import ContextHandler
from origin.ui.publishes_viewer_ui.publishes_view_core import MainPublishesViewCore
from origin.ui.project_viewer_ui.project_tree_viewer_core import ProjectTreeViewerCore
from origin.ui.task_viewer_ui.task_viewer_core import TaskViewerCore
from origin.ui.entity_properties_ui.properties_viewer import PropertiesViewer
from origin.ui.app_launcher.app_launcher_ui import AppLauncher
from origin.ui.sanity_checker_ui.sanity_checker_wdg import SanityChecker


origin_dev_root = os.getenv("ORIGIN_ROOT")
thumbnail_path = os.path.normpath(os.path.join(origin_dev_root, "origin/dcc/icons/movie_pic.png"))


class OriginControlCenterUI(QtWidgets.QWidget):
    WINDOW_TITLE = "Origin Control Center"

    def __init__(self, parent=None):
        super(OriginControlCenterUI, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.current_context = None

        self.setMinimumHeight(850)
        self.setMinimumWidth(1800)

        self.create_widgets()

        self.create_layout()
        self.create_connections()
        self.load_last_session()

    def create_widgets(self):
        self.sanity_checker_wdg = SanityChecker()
        self.launcher_tw = AppLauncher()
        self.show_view_twd = ProjectTreeViewerCore()
        self.tasks_view_lwd = TaskViewerCore()
        self.versions_view_tvw = MainPublishesViewCore()
        self.entity_details_viewer_wdg = PropertiesViewer()
        self.entity_details_viewer_wdg.set_thumbnail_icon(icon_path=thumbnail_path)

        self.context_viewer = QtWidgets.QLabel()
        self.context_viewer.setMaximumHeight(20)
        self.context_viewer.setStyleSheet("background-color: #868071; color: #0d0d0d; font-size: 12px; font-weight: bold;")
        # self.context_viewer.setText(self.show_view_twd.show_select_cb.currentText())

        self.middle_tabmenu_tab = QtWidgets.QTabWidget()
        self.middle_tabmenu_tab.addTab(self.tasks_view_lwd, "Tasks")
        self.middle_tabmenu_tab.addTab(self.versions_view_tvw, "Publishes")

        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def load_last_session(self):
        session = SessionManager()
        last_session = session.get_last_session()
        self.context_viewer.setText(last_session["show_name"])
        self.show_view_twd.show_select_cb.setCurrentText(last_session["show_name"])

    def save_last_session(self):
        session = SessionManager()
        session.save_last_session(session=self.show_view_twd.show_select_cb.currentText())

    def closeEvent(self, event):
        self.save_last_session()

    def current_context_receiver(self, context: ContextHandler):
        self.current_context = context.resolve_to_full_context()
        self.context_viewer.setText(self.current_context)
        return self.current_context

    def update_context_label(self):
        current_show = self.show_view_twd.show_select_cb.currentText()
        self.context_viewer.setText(current_show)

    def update_window_name(self, name):
        if "." in name:
            name_elements = name.split(".")
            compose_name = "--".join(name_elements)
            self.setWindowTitle(f"ORIGIN - {compose_name}")

        else:
            self.setWindowTitle(f"ORIGIN - {name}")

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
        vertical_splitter.setSizes([150, 890, 465, 150])

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.context_viewer)
        main_layout.addLayout(views_layout)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)
        main_layout.addLayout(button_layout)

    def create_connections(self):

        self.show_view_twd.show_select_cb.currentIndexChanged.connect(self.populate_main_publishes)
        self.show_view_twd.show_select_cb.currentIndexChanged.connect(self.save_last_session)
        self.show_view_twd.show_select_cb.currentIndexChanged.connect(self.update_context_label)

        self.show_view_twd.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_task_viewer)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_task_viewer)

        self.show_view_twd.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_main_publishes)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_main_publishes)

        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_entry_properties)
        self.show_view_twd.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_entry_properties)

        self.show_view_twd.current_context.connect(self.entity_details_viewer_wdg.properties_wdg.context_receiver)
        self.show_view_twd.current_context.connect(self.tasks_view_lwd.context_receiver)
        self.show_view_twd.current_context.connect(self.versions_view_tvw.context_receiver)
        self.show_view_twd.current_context.connect(self.current_context_receiver)

        self.versions_view_tvw.selected_version.connect(self.entity_details_viewer_wdg.components_wdg.context_receiver)
        self.versions_view_tvw.selected_version.connect(self.entity_details_viewer_wdg.stack_slots_wdg.context_receiver)

        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_shows)
        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_tree_widget)

        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.launcher_tw.populate_widget)
        self.tasks_view_lwd.current_context.connect(self.launcher_tw.context_receiver)
        self.tasks_view_lwd.current_context.connect(self.entity_details_viewer_wdg.versions_wdg.context_receiver)
        self.tasks_view_lwd.current_context.connect(self.current_context_receiver)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.clear_launch_app_wdg)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_task_versions)

        self.versions_view_tvw.publish_view_tw.itemSelectionChanged.connect(self.populate_file_components)
        self.versions_view_tvw.publish_view_tw.itemSelectionChanged.connect(self.populate_stack_viewer)

        self.middle_tabmenu_tab.currentChanged.connect(self.on_middle_tab_change)
        self.entity_details_viewer_wdg.details_tabmenu_tab.currentChanged.connect(self.on_properties_tab_change)

    def set_proj_tree_focus(self):
        self.show_view_twd.setFocus()

    def set_task_viewer_focus(self):
        self.tasks_view_lwd.setFocus()

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
                self.populate_file_components()

            else:
                self.entity_details_viewer_wdg.components_wdg.slot_component_viewer_tw.clearSelection()
                self.entity_details_viewer_wdg.components_wdg.slot_component_viewer_tw.clear()

            if current_widget == self.entity_details_viewer_wdg.stack_slots_wdg:
                self.populate_stack_viewer()

            else:
                self.entity_details_viewer_wdg.stack_slots_wdg.publish_view_tw.clearSelection()
                self.entity_details_viewer_wdg.stack_slots_wdg.publish_view_tw.clear()

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
                    self.tasks_view_lwd.current_context.connect(
                        self.entity_details_viewer_wdg.versions_wdg.context_receiver)
                    self.entity_details_viewer_wdg.versions_wdg.populate_widget()
        else:
            self.entity_details_viewer_wdg.versions_wdg.publish_view_tw.clearSelection()
            self.entity_details_viewer_wdg.versions_wdg.publish_view_tw.clear()

    def populate_stack_viewer(self):
        widget_selection = self.versions_view_tvw.get_current_selected()
        if len(widget_selection) != 0:
            tab_idx = self.entity_details_viewer_wdg.details_tabmenu_tab.currentIndex()
            current_widget = self.entity_details_viewer_wdg.details_tabmenu_tab.widget(tab_idx)
            if current_widget:
                if current_widget == self.entity_details_viewer_wdg.stack_slots_wdg:
                    self.versions_view_tvw.selected_version.connect(
                        self.entity_details_viewer_wdg.stack_slots_wdg.context_receiver)
                    self.entity_details_viewer_wdg.stack_slots_wdg.populate_widget()
        else:
            self.entity_details_viewer_wdg.stack_slots_wdg.publish_view_tw.clearSelection()
            self.entity_details_viewer_wdg.stack_slots_wdg.publish_view_tw.clear()

    def clear_launch_app_wdg(self):
        widget_selection = self.tasks_view_lwd.get_current_selected()
        if len(widget_selection) == 0:
            self.launcher_tw.clear_app_widget()
            self.tasks_view_lwd.task_viewer_wdg.clearSelection()

    def populate_file_components(self):
        widget_selection = self.versions_view_tvw.get_current_selected()
        if len(widget_selection) != 0:
            tab_idx = self.entity_details_viewer_wdg.details_tabmenu_tab.currentIndex()
            current_widget = self.entity_details_viewer_wdg.details_tabmenu_tab.widget(tab_idx)
            if current_widget:
                if current_widget == self.entity_details_viewer_wdg.components_wdg:
                    self.versions_view_tvw.selected_version.connect(
                        self.entity_details_viewer_wdg.components_wdg.context_receiver)
                    self.entity_details_viewer_wdg.components_wdg.populate_widget()
        else:
            self.entity_details_viewer_wdg.components_wdg.slot_component_viewer_tw.clearSelection()
            self.entity_details_viewer_wdg.components_wdg.slot_component_viewer_tw.clear()

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

        self.central_widget = OriginControlCenterUI()
        self.setWindowTitle("Origin Control Center")
        self.setWindowIcon(QIcon("path/to/your/icon.png"))
        self.setCentralWidget(self.central_widget)
        # self.show()

        # self.set_style()

    def set_style(self):
        origin_dev_root = os.getenv("ORIGIN_ROOT")

        qss_style_file = os.path.normpath(
            os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

        with open(qss_style_file, "r") as f:
            _style = f.read()
            self.central_widget.setStyleSheet(_style)

        app_font = self.central_widget.font()
        app_font.setPointSize(7)
        self.central_widget.setFont(app_font)


if __name__ == "__main__":
    origin_dev_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))
    window_icon_file = os.path.normpath(os.path.join(origin_dev_root, "origin/icons/origin_tray_icons/origin_tray_v007_32x32.png"))

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    font = app.font()
    font.setPointSize(7)
    app.setFont(font)

    test_dialog = MainUI()
    test_dialog.setWindowIcon(QIcon(window_icon_file))
    test_dialog.show()

    sys.exit(app.exec_())
