from PySide2 import QtWidgets

from ui.odb_entry_properties_editor_UI import EntryPropertiesEditorUI
from ui.entity_properties_ui.custom_widgets.odb_links_ui import ButtonsWidget
from ui.entity_properties_ui.custom_widgets.odb_notes_ui import NotesWidget
from ui.entity_properties_ui.custom_widgets.component_viewer_core import SlotComponentsViewerCore
from ui.entity_properties_ui.custom_widgets.representation_viewer_wdg import RepresentationViewer
from ui.odb_main_publishes_view_core import MainPublishesViewCore

icon_path = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\dcc\icons\mvoie.png"


class PropertiesViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PropertiesViewer, self).__init__(parent)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.representation_wdg = RepresentationViewer()

        self.notes_wdg = NotesWidget()
        self.links_wdg = ButtonsWidget()
        self.properties_wdg = EntryPropertiesEditorUI()
        self.components_wdg = SlotComponentsViewerCore()

        self.versions_wdg = MainPublishesViewCore()
        self.versions_wdg.publish_view_tw.setObjectName("PropertiesPublishesViewer")
        self.versions_wdg.publish_view_tw.setColumnHidden(11, True)
        self.versions_wdg.publish_view_tw.setColumnHidden(10, True)
        self.versions_wdg.publish_view_tw.setColumnHidden(9, True)
        self.versions_wdg.publish_view_tw.setColumnHidden(8, True)
        self.versions_wdg.publish_view_tw.setColumnHidden(7, True)
        # self.versions_wdg.publish_view_tw.setColumnHidden(6, True)
        self.versions_wdg.publish_view_tw.setColumnHidden(5, True)
        self.versions_wdg.publish_view_tw.setColumnHidden(4, True)
        self.versions_wdg.publish_view_tw.setColumnHidden(1, True)

        self.details_tabmenu_tab = QtWidgets.QTabWidget()
        self.details_tabmenu_tab.setTabPosition(QtWidgets.QTabWidget.North)
        self.details_tabmenu_tab.addTab(self.components_wdg, "Components")
        self.details_tabmenu_tab.addTab(self.versions_wdg, "Publishes")
        self.details_tabmenu_tab.addTab(self.links_wdg, "Links")
        self.details_tabmenu_tab.addTab(self.notes_wdg, "Notes")
        self.details_tabmenu_tab.addTab(self.properties_wdg, "Properties")

    def on_middle_tab_change(self, index):
        current_widget = self.middle_tabmenu_tab.widget(index)
        if current_widget:
            if current_widget == self.tasks_view_lwd:
                current_widget.populate_widget()
            else:
                self.tasks_view_lwd.task_viewer_wdg.clear()

            if current_widget == self.versions_view_tvw:
                self.populate_main_publishes()
            else:
                self.versions_view_tvw.publish_view_tw.clear()

    def set_thumbnail_icon(self, icon_path):
        self.representation_wdg.thumbnail_wdg.set_thumbnail(icon_path=icon_path)


    def create_layout(self):
        details_layout = QtWidgets.QVBoxLayout(self)
        # splitter_sp = QtWidgets.QSplitter()
        # splitter_sp.setOrientation(QtCore.Qt.Horizontal)
        # details_layout.addWidget(splitter_sp)
        details_layout.addWidget(self.representation_wdg)
        details_layout.addWidget(self.details_tabmenu_tab)
