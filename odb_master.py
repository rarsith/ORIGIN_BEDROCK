import sys
from PySide2 import QtWidgets, QtGui, QtCore

from o_database.entities.actions import Query
from o_database.odb_statuses import DbTaskStatuses
from ui.odb_links_ui import ButtonsWidget
from ui.odb_notes_ui import NotesWidget
from ui.odb_main_publishes_view_core import MainPublishesViewCore
from ui.odb_slot_component_viewer_core import SlotComponentsViewerCore
from ui.odb_project_tree_viewer_core import ProjectTreeViewerCore
from ui.odb02_task_viewer_core import TaskViewerCore
from ui.odb_entry_properties_editor_UI import EntryPropertiesEditorUI


class ThumbnailViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ThumbnailViewer, self).__init__(parent)
        self.thumbnail_path = ""
        self.thumbnail_width = 256
        self.thumbnail_height = 256

        self.create_widget()
        self.create_layout()
        self.set_thumbnail()

    def create_widget(self):
        self.label_lb = QtWidgets.QLabel()
        self.pixamp_pix = QtGui.QPixmap()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.label_lb)

    def set_thumbnail(self):
        color = QtGui.QColor(200, 200, 200)

        painter = QtGui.QPainter(self.pixamp_pix)
        painter.fillRect(self.pixamp_pix.rect(), color)
        painter.end()

        self.pixamp_pix.scaled(self.thumbnail_width, self.thumbnail_height)
        self.pixamp_pix.fill(color)
        self.label_lb.setPixmap(self.pixamp_pix)
        self.label_lb.show()


class EntityBriefInfo(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EntityBriefInfo, self).__init__(parent)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.status_lb = QtWidgets.QLabel("Status")
        self.status_cb = QtWidgets.QComboBox()
        self.status_cb.addItems(DbTaskStatuses().list_all())

        self.linked_to_lb = QtWidgets.QLabel("Linked to")
        self.task_lb = QtWidgets.QLabel("Task")

    def create_layout(self):
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addWidget(self.status_lb, 0, 0)
        main_layout.addWidget(self.status_cb, 0, 1)
        main_layout.addWidget(self.linked_to_lb, 1, 0)
        main_layout.addWidget(self.task_lb, 2, 0)


class RepresentationViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RepresentationViewer, self).__init__(parent)

        self.setMinimumHeight(150)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.thumbnail_wdg = ThumbnailViewer()
        self.entity_summary_wdg = EntityBriefInfo()

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.thumbnail_wdg)
        main_layout.addWidget(self.entity_summary_wdg)


class EntityDetailsViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EntityDetailsViewer, self).__init__(parent)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.representation_wdg = RepresentationViewer()

        self.notes_wdg = NotesWidget()
        self.links_wdg = ButtonsWidget()
        self.properties_wdg = EntryPropertiesEditorUI()
        self.components_wdg = SlotComponentsViewerCore()

        self.details_tabmenu_tab = QtWidgets.QTabWidget()
        self.details_tabmenu_tab.setTabPosition(QtWidgets.QTabWidget.North)
        self.details_tabmenu_tab.addTab(self.components_wdg, "Components")
        self.details_tabmenu_tab.addTab(self.links_wdg, "Links")
        self.details_tabmenu_tab.addTab(self.notes_wdg, "Notes")
        self.details_tabmenu_tab.addTab(self.properties_wdg, "Properties")


    def create_layout(self):
        details_layout = QtWidgets.QVBoxLayout(self)
        # splitter_sp = QtWidgets.QSplitter()
        # splitter_sp.setOrientation(QtCore.Qt.Horizontal)
        # details_layout.addWidget(splitter_sp)
        details_layout.addWidget(self.representation_wdg)
        details_layout.addWidget(self.details_tabmenu_tab)



class OriginControlCenterUI(QtWidgets.QWidget):
    WINDOW_TITLE = "Origin Control Center"

    def __init__(self):
        super(OriginControlCenterUI, self).__init__()

        self.setWindowTitle(self.WINDOW_TITLE)

        self.setMinimumHeight(700)
        self.setMinimumWidth(1500)

        self.create_widgets()

        self.create_layout()
        self.create_connections()
        self.populate_main_publishes()

    def create_widgets(self):
        self.launcher_tw = QtWidgets.QTableWidget()
        self.launcher_tw.setMaximumHeight(100)

        self.show_view_twd = ProjectTreeViewerCore()
        self.tasks_view_lwd = TaskViewerCore()
        self.versions_view_tvw = MainPublishesViewCore()
        self.entity_details_viewer_wdg = EntityDetailsViewer()

        self.middle_tabmenu_tab = QtWidgets.QTabWidget()
        self.middle_tabmenu_tab.addTab(self.tasks_view_lwd, "Tasks")
        self.middle_tabmenu_tab.addTab(self.versions_view_tvw, "Publishes")

        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        views_layout = QtWidgets.QHBoxLayout()
        views_layout.setContentsMargins(2, 2, 2, 2)
        views_layout.setSpacing(0)
        self.horizontal_splitter = QtWidgets.QSplitter()
        views_layout.addWidget(self.horizontal_splitter)

        self.horizontal_splitter.insertWidget(0, self.show_view_twd)
        self.horizontal_splitter.insertWidget(1, self.middle_tabmenu_tab)
        self.horizontal_splitter.insertWidget(2, self.entity_details_viewer_wdg)
        self.horizontal_splitter.setSizes([100, 700, 300])

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.launcher_tw)
        button_layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(views_layout)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(0)
        main_layout.addLayout(button_layout)



    def create_connections(self):
        self.show_view_twd.show_select_cb.currentIndexChanged.connect(self.populate_main_publishes)
        self.show_view_twd.show_select_cb.currentIndexChanged.connect(self.get_tasks)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.get_tasks)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.update_entry_properties_list)

        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_shows)
        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_tree_widget)

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

    def get_tasks(self):
        self.tasks_view_lwd.populate_tasks()

    def update_entry_properties_list(self):
        properties = self.get_entry_properties()
        self.entity_details_viewer_wdg.properties_wdg.create_properties(properties)

    def get_entry_properties(self):
        spare_it = {}
        definitions_list = Query().curr_asset().definition

        if definitions_list is None:
            return spare_it
        else:
            try:
                if len(definitions_list) == 0:
                    return spare_it
                elif len(definitions_list) >= 1:
                    return definitions_list["definition"]
            except:
                pass

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
