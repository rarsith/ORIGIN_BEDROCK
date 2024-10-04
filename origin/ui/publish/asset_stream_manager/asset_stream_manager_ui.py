from PySide2 import QtWidgets, QtCore

from origin.envars.Xorigin_envars import ContextHandler
from o_database.entities.asset_class_dispacher import extract_asset_class
from origin.ui.Xproject_tree_viewer_UI import ProjectTreeViewerUI
from origin.ui.publish.asset_stream_manager.widgets.create_asset_stream_ui import CreateStreamUI
from origin.ui.publish.asset_stream_manager.widgets.delete_asset_stream_ui import DeleteEmptyStreamsUI
from o_database.entities.Xoperators import CollectionOperators, Asset


class ContextViewer(ProjectTreeViewerUI):
    def __init__(self, context, parent=None):
        super(ContextViewer, self).__init__(parent)

        self.asset_class = extract_asset_class(context=context)

        self.create_project_btn.setVisible(False)
        self.show_select_cb.setVisible(False)

    def isolate_to_context(self):
        asset_path = self.asset_class.id.split(".", 1)[1]

        if self.asset_class.type != "group":
            self.project_tree_viewer_wdg.clear()

            item = QtWidgets.QTreeWidgetItem([asset_path])
            item.setData(0, QtCore.Qt.UserRole, self.asset_class.id)
            item.setData(1, QtCore.Qt.UserRole, self.asset_class.type)
            self.project_tree_viewer_wdg.addTopLevelItem(item)
            return item

class EntryStackStream(QtWidgets.QWidget):
    def __init__(self, context=None, current_stream=None, parent=None):
        super(EntryStackStream, self).__init__(parent)

        self.context_handler = ContextHandler()
        self.context_handler.load_session(context)

        self.current_stream = current_stream

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.context_display_control(state=0)
        self.init_return = self.get_selected_options()
        print(self.init_return)

    def create_widgets(self):
        self.project_tree = ContextViewer(context=self.context_handler.snapshot_session())

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
        self.stack_stream_lw.itemClicked.connect(self.get_selected_options)
        self.create_new_stream_btn.clicked.connect(self.create_stack_stream)
        self.delete_empty_streams_btn.clicked.connect(self.delete_empty_streams)

    def context_display_control(self, state):
        if state == 2:
            self.project_tree.refresh_tree_widget()
        else:
            created_item = self.project_tree.isolate_to_context()
            self.project_tree.project_tree_viewer_wdg.setCurrentItem(created_item)
            self.populate_streams()

    def populate_streams(self):
        stack_streams = self.get_stack_streams()
        # get_streams_names = [stream.rsplit(".", 1)[1] for stream in stack_streams]

        self.all_streams.setChecked(True)
        is_current_stream_context = self.current_stream_context.isChecked()

        if is_current_stream_context:
            self.current_stream_context.setChecked(True)
            self.delete_empty_streams_btn.setEnabled(False)

            self.stack_stream_lw.clear()

            stream_name = self.current_stream.rsplit(".", 1)[1]
            list_item = QtWidgets.QListWidgetItem(stream_name)
            self.stack_stream_lw.addItem(list_item)
            self.stack_stream_lw.setCurrentItem(list_item)

            list_item.setData(QtCore.Qt.UserRole, self.current_stream)

        else:
            self.stack_stream_lw.clear()
            self.delete_empty_streams_btn.setEnabled(True)
            if stack_streams:
                for stream in stack_streams:
                    stream_name = stream.rsplit(".", 1)[1]
                    list_item = QtWidgets.QListWidgetItem(stream_name)
                    self.stack_stream_lw.addItem(list_item)
                    list_item.setData(QtCore.Qt.UserRole, stream)

    def get_stack_streams(self):
        db_ops = CollectionOperators(db_collection=self.context_handler.show_name)
        entity_doc = db_ops.entity_document(doc_id=self.context_handler.entity_id)
        asset_doc = Asset(**entity_doc)

        curr_asset_type = self.context_handler.entity_type
        stack_steams = asset_doc.stack_streams

        if curr_asset_type != "group":
            if stack_steams is None:
                return {}
            if len(stack_steams) == 0:
                return {}
            else:
                return stack_steams

    def get_selected_options(self):
        message = "Please Select a Stream!"
        current_item = self.stack_stream_lw.currentItem()
        if current_item:
            item_data = current_item.data(QtCore.Qt.UserRole)
            return {"db_asset_id": item_data}
        else:
            return None

    def create_stack_stream(self):
        context = self.context_handler.snapshot_session()
        self.ui = CreateStreamUI(context=context)
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.populate_streams)
        self.ui.create_and_close_btn.clicked.connect(self.populate_streams)

    def delete_empty_streams(self):
        context = self.context_handler.snapshot_session()
        self.ui = DeleteEmptyStreamsUI(context=context)
        self.ui.show()
        self.ui.delete_btn.clicked.connect(self.populate_streams)
        self.ui.delete_and_close_btn.clicked.connect(self.populate_streams)


if __name__ == "__main__":
    import sys

    context_sample = {'show_name': 'New_State',
                      'project_publishes': 'New_State__PUBLISHES',
                      'project_work': 'New_State__WORK',
                      'project_control': 'New_State__CONTROL',
                      'origin_path_hierarchy': 'assets.chr.red_hulk',
                      'entity_name': 'red_hulk',
                      'entity_type': 'asset',
                      'entity_id': 'New_State.assets.chr.red_hulk',
                      'task_name': "modeling",
                      'task_type': "modeling"}

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = EntryStackStream(context=context_sample)

    test_dialog.show()
    sys.exit(app.exec_())
