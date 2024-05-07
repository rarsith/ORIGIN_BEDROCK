from PySide2 import QtWidgets

from ui.odb_entry_properties_editor_UI import EntryPropertiesEditorUI
from ui.properties_ui.odb_links_ui import ButtonsWidget
from ui.properties_ui.odb_notes_ui import NotesWidget
from ui.properties_ui.odb_slot_component_viewer_core import SlotComponentsViewerCore
from ui.properties_ui.representation_viewer_wdg import RepresentationViewer

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

        self.details_tabmenu_tab = QtWidgets.QTabWidget()
        self.details_tabmenu_tab.setTabPosition(QtWidgets.QTabWidget.North)
        self.details_tabmenu_tab.addTab(self.components_wdg, "Components")
        self.details_tabmenu_tab.addTab(self.links_wdg, "Links")
        self.details_tabmenu_tab.addTab(self.notes_wdg, "Notes")
        self.details_tabmenu_tab.addTab(self.properties_wdg, "Properties")

    def set_thumbnail_icon(self, icon_path):
        self.representation_wdg.thumbnail_wdg.set_thumbnail(icon_path=icon_path)


    def create_layout(self):
        details_layout = QtWidgets.QVBoxLayout(self)
        # splitter_sp = QtWidgets.QSplitter()
        # splitter_sp.setOrientation(QtCore.Qt.Horizontal)
        # details_layout.addWidget(splitter_sp)
        details_layout.addWidget(self.representation_wdg)
        details_layout.addWidget(self.details_tabmenu_tab)
