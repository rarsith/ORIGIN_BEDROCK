from PySide2 import QtWidgets, QtCore

from origin.envars.origin_envars import ContextHandler
from origin.database.dispachers.entity_class_dispatcher import extract_asset_class
from origin.ui.project_tree_viewer_UI import ProjectTreeViewerUI
from origin.ui.publish.asset_stream_manager.widgets.create_asset_stream_ui import CreateStreamUI
from origin.ui.publish.asset_stream_manager.widgets.delete_asset_stream_ui import DeleteEmptyStreamsUI
from origin.database.entities.operators import Asset
from origin.database.mongo import CollectionOperators
from origin.ui.stream_viewer_UI import StreamViewerUI


class ContextViewer(ProjectTreeViewerUI):
    def __init__(self, context: ContextHandler, parent=None):
        super(ContextViewer, self).__init__(parent)

        self.context_handler = context

        self.asset_class = extract_asset_class(context=self.context_handler)

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
    current_context = QtCore.Signal(object)

    def __init__(self, context: ContextHandler, current_stream=None, parent=None):
        super(EntryStackStream, self).__init__(parent)

        self.context_handler = context

        self.current_stream = current_stream

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.context_display_control(state=0)
        self.init_return = self.get_selected_options()

    def create_widgets(self):
        self.project_tree = ContextViewer(context=self.context_handler)

        self.stack_stream_lw = QtWidgets.QListWidget()
        self.stack_stream_lw.setFocusPolicy(QtCore.Qt.NoFocus)

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
        self.stack_stream_lw.itemClicked.connect(self.update_context)
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

    def update_context(self):
        current_item = self.stack_stream_lw.currentItem()
        if current_item:
            item_data = current_item.data(QtCore.Qt.UserRole)
            self.context_handler.db_asset_stream_id = item_data

    def get_selected_options(self):
        current_item = self.stack_stream_lw.currentItem()
        if current_item:
            item_data = current_item.data(QtCore.Qt.UserRole)
            self.context_handler.db_asset_stream_id = item_data

            return {"db_asset_stream_id": item_data,
                    "context_object": self.context_handler}
        else:
            return None

    def create_stack_stream(self):
        self.ui = CreateStreamUI(context=self.context_handler)
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.populate_streams)
        self.ui.create_and_close_btn.clicked.connect(self.populate_streams)

    def delete_empty_streams(self):
        self.ui = DeleteEmptyStreamsUI(context=self.context_handler)
        self.ui.show()
        self.ui.delete_btn.clicked.connect(self.populate_streams)
        self.ui.delete_and_close_btn.clicked.connect(self.populate_streams)


if __name__ == "__main__":
    import sys

    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'tafer',
                      'entity_type': 'asset',
                      'entity_id': 'The_Rock.assets.chr.tafer',
                      'task_name': "modeling",
                      'task_type': "modeling",
                      'task_id': "The_Rock.assets.chr.tafer.modeling",
                      'db_asset_stream_id': 'The_Rock.assets.chr.tafer.main'}

    context_obj = ContextHandler()
    context_obj.load_session(session_data=context_sample)

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = EntryStackStream(context=context_obj)
    test_dialog.populate_streams()

    test_dialog.show()
    sys.exit(app.exec_())
