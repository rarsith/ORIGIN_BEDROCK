import sys
from PySide2 import QtWidgets, QtCore
from ui.odb_project_tree_viewer_UI import ProjectTreeViewerUI
from ui.publish_ui.create_stack_stream_ui import CreateStreamUI
from ui.publish_ui.delete_stack_stream_ui import DeleteEmptyStreamsUI
from common_utils import nice_names as nice_names
from o_database.entities.actions import Query, Set, Fetch, Remove
from envars.origin_envars import OriginEnvar


class ContextViewer(ProjectTreeViewerUI):
    def __init__(self, parent=None):
        super(ContextViewer, self).__init__(parent)

        self.create_project_btn.setVisible(False)
        self.show_select_cb.setVisible(False)

    def isolate_to_context(self, entity_id):
        import os
        asset_document = Fetch().project_structure_entities().entity_document(doc_id=entity_id)

        get_full_context = asset_document["origin_db_path"]
        entity_name = asset_document["entry_name"]
        entity_type = asset_document["type"]

        separate_elements = get_full_context.split(".")[1:]
        separate_elements.append(entity_name)
        full_context_path = os.path.join(*separate_elements)

        if entity_type != "group":
            self.project_tree_viewer_wdg.clear()

            item = QtWidgets.QTreeWidgetItem([full_context_path])
            item.setData(0, QtCore.Qt.UserRole, entity_id)
            item.setData(1, QtCore.Qt.UserRole, entity_type)
            self.project_tree_viewer_wdg.addTopLevelItem(item)
            return item

class EntryStackStream(QtWidgets.QWidget):
    def __init__(self, entity_id=None, current_stream=None, parent=None):
        super(EntryStackStream, self).__init__(parent)

        self.entity_id = entity_id
        self.current_stream = current_stream

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.context_display_control(state=0)

    def create_widgets(self):
        self.project_tree = ContextViewer()

        self.stack_stream_lw = QtWidgets.QListWidget()

        self.create_new_stream_btn = QtWidgets.QPushButton("Create New Stream")
        self.delete_empty_streams_btn = QtWidgets.QPushButton("Delete Empty Stream")

        self.current_stream_context = QtWidgets.QRadioButton("Current Stream")
        self.current_stream_context.setChecked(True)

        self.all_streams = QtWidgets.QRadioButton("All Streams")
        self.unlock_context = QtWidgets.QCheckBox("Unlock Context")

    def create_layout(self):
        context_wdg_layout = QtWidgets.QVBoxLayout()
        context_wdg_layout.addWidget(self.current_stream_context)
        context_wdg_layout.addWidget(self.all_streams)
        # context_wdg_layout.addWidget(self.unlock_context)
        context_wdg_layout.setAlignment(QtCore.Qt.AlignTop)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.delete_empty_streams_btn)
        buttons_layout.addWidget(self.create_new_stream_btn)
        buttons_layout.setAlignment(QtCore.Qt.AlignRight)

        windows_layout = QtWidgets.QHBoxLayout()
        windows_layout.addLayout(context_wdg_layout)
        windows_layout.addWidget(self.project_tree)
        windows_layout.addWidget(self.stack_stream_lw)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(windows_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.setStretch(1, 1)

    def create_connections(self):
        self.project_tree.project_tree_viewer_wdg.itemClicked.connect(self.populate_streams)
        self.current_stream_context.toggled.connect(self.populate_streams)
        self.all_streams.toggled.connect(self.populate_streams)
        self.create_new_stream_btn.clicked.connect(self.create_stack_stream)
        self.delete_empty_streams_btn.clicked.connect(self.delete_empty_streams)

    def context_display_control(self, state):
        if state == 2:
            self.project_tree.refresh_tree_widget()
        else:
            created_item = self.project_tree.isolate_to_context(entity_id=self.entity_id)
            self.project_tree.project_tree_viewer_wdg.setCurrentItem(created_item)
            self.populate_streams()

    def populate_streams(self):
        stack_streams = self.get_stack_streams()

        is_current_stream_context = self.current_stream_context.isChecked()
        is_all_streams = self.all_streams.isChecked()

        if is_current_stream_context:
            self.delete_empty_streams_btn.setEnabled(False)
            self.stack_stream_lw.clear()
            list_item = QtWidgets.QListWidgetItem(self.current_stream)
            self.stack_stream_lw.addItem(list_item)
            self.stack_stream_lw.setCurrentItem(list_item)

        else:
            self.stack_stream_lw.clear()
            self.delete_empty_streams_btn.setEnabled(True)
            if stack_streams:
                for stream in stack_streams:
                    list_item = QtWidgets.QListWidgetItem(stream)
                    self.stack_stream_lw.addItem(list_item)

    # def selected_entry_id(self):
    #     sel_item = self.project_tree.get_selected()
    #     if sel_item:
    #         self.current_asset_id = sel_item.data(0, QtCore.Qt.UserRole)
    #         return self.current_asset_id

    def get_stack_streams(self):
        item_id = self.entity_id
        spare_it = {}
        curr_asset_type = Query().entity(entity_id=item_id).entity_type
        stack_steams = Query().entity(entity_id=item_id).stack_stream

        if curr_asset_type != "group":
            if stack_steams is None:
                return spare_it
            if len(stack_steams) == 0:
                return spare_it
            else:
                return stack_steams

    def create_stack_stream(self):
        self.ui = CreateStreamUI(entity_id=self.entity_id)
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.populate_streams)
        self.ui.create_and_close_btn.clicked.connect(self.populate_streams)

    def delete_empty_streams(self):
        self.ui = DeleteEmptyStreamsUI(entity_id=self.entity_id)
        self.ui.show()
        self.ui.delete_btn.clicked.connect(self.populate_streams)
        self.ui.delete_and_close_btn.clicked.connect(self.populate_streams)


if __name__ == "__main__":
    import sys
    # from envars.origin_envars import OriginEnvar

    path = ["assets", "characters"]

    OriginEnvar.show_name = "New_Era"
    OriginEnvar.origin_path_hierarchy = path
    OriginEnvar.entry_name = "green_hulk"
    asset_id = OriginEnvar.resolve_entity_id()
    # curr_stream = "green_hulk_main"

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = EntryStackStream(entity_id=asset_id)

    test_dialog.show()
    sys.exit(app.exec_())
