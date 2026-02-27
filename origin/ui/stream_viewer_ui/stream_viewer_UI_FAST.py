from PySide2 import QtWidgets, QtCore

from origin.database.entities.operators import Asset
from origin.database.mongo import CollectionOperators
from origin.envars.origin_envars import ContextHandler
from origin.ui.publish.asset_stream_manager.widgets.create_asset_stream_ui import CreateStreamUI
from origin.ui.publish.asset_stream_manager.widgets.delete_asset_stream_ui import DeleteEmptyStreamsUI


class CustomListWidget(QtWidgets.QListWidget):
    def mousePressEvent(self, event):
        # Check if the click is on an item
        item = self.itemAt(event.pos())
        if item is None:
            # If no item is clicked, clear the selection
            self.clearSelection()
        # Call the base class implementation to handle other mouse events
        super().mousePressEvent(event)

class StreamViewerUI(QtWidgets.QWidget):
    current_context = QtCore.Signal(object)

    def __init__(self, context: ContextHandler = None, current_stream=None, parent=None):
        super(StreamViewerUI, self).__init__(parent)

        self.context_handler = context

        self.current_stream = current_stream

        self.create_widgets()
        self.create_connections()
        self.create_layout()

    def create_widgets(self):
        self.stack_stream_lw = CustomListWidget()
        self.stack_stream_lw.setFocusPolicy(QtCore.Qt.NoFocus)

        self.create_new_stream_btn = QtWidgets.QPushButton("Create New Stream")
        self.delete_empty_streams_btn = QtWidgets.QPushButton("Delete Empty Stream")

    def create_connections(self):
        self.stack_stream_lw.itemClicked.connect(self.update_context)
        self.stack_stream_lw.itemSelectionChanged.connect(self.update_context)
        self.create_new_stream_btn.clicked.connect(self.create_stack_stream)
        self.delete_empty_streams_btn.clicked.connect(self.delete_empty_streams)

    def create_layout(self):
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.delete_empty_streams_btn)
        buttons_layout.addWidget(self.create_new_stream_btn)
        buttons_layout.setAlignment(QtCore.Qt.AlignRight)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.stack_stream_lw)
        main_layout.addLayout(buttons_layout)
        main_layout.setContentsMargins(0,0,0,0)
        # main_layout.setStretch(1, 1)

    def context_receiver(self, context: ContextHandler):
        self.context_handler = context

    def populate_widget(self):
        stack_streams = self.get_stack_streams()
        self.stack_stream_lw.clear()

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
        print(stack_steams)

        if curr_asset_type != "group":
            if stack_steams is None:
                return {}
            if len(stack_steams) == 0:
                return {}
            else:
                return stack_steams

    def update_context(self):
        selected_item = self.stack_stream_lw.selectedItems()
        current_item = selected_item[0] if selected_item else None
        if current_item is not None:
            item_data = current_item.data(QtCore.Qt.UserRole)
            self.context_handler.db_asset_stream_id = item_data
            self.current_context.emit(self.context_handler)
        else:
            self.context_handler.db_asset_stream_id = None
            self.current_context.emit(self.context_handler)


    def create_stack_stream(self):
        self.ui = CreateStreamUI(context=self.context_handler)
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.populate_widget)
        self.ui.create_and_close_btn.clicked.connect(self.populate_widget)

    def delete_empty_streams(self):
        self.ui = DeleteEmptyStreamsUI(context=self.context_handler)
        self.ui.show()
        self.ui.delete_btn.clicked.connect(self.populate_widget)
        self.ui.delete_and_close_btn.clicked.connect(self.populate_widget)


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
    test_dialog = StreamViewerUI(context=context_obj)
    test_dialog.populate_widget()

    test_dialog.show()
    sys.exit(app.exec_())