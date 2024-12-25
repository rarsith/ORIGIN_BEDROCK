import sys
from PySide2 import QtWidgets, QtCore

from origin.envars.origin_envars import ContextHandler
from origin.database.dispachers.entity_class_dispatcher import extract_asset_class

from origin.database.mongo import CollectionOperators


class DeleteEmptyStreamsUI(QtWidgets.QDialog):

    def __init__(self, context: ContextHandler, parent=None):
        super(DeleteEmptyStreamsUI, self).__init__(parent)

        self.setWindowTitle("Delete Empty Stream")

        self.context_handler = context
        self.asset_class = extract_asset_class(context=self.context_handler)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.populate_streams()

    def reload_asset_class(self):
        self.asset_class = extract_asset_class(context=self.context_handler)

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLabel()

        item_path = ".".join([self.context_handler.show_name,
                              self.context_handler.origin_path_hierarchy,
                              self.context_handler.entity_name,
                              self.context_handler.task_type
                              ])

        self.show_name_le.setText(item_path)

        self.stream_name_lw = QtWidgets.QListWidget()

        self.delete_btn = QtWidgets.QPushButton("Delete Selected")
        self.delete_and_close_btn = QtWidgets.QPushButton("Delete and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Entry Path: ", self.show_name_le)
        form_layout.addRow("Stream Name:", self.stream_name_lw)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.delete_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.delete_btn.clicked.connect(self.db_commit)
        self.delete_and_close_btn.clicked.connect(self.db_commit_close)
        self.cancel_btn.clicked.connect(self.close)

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        self.remove_doc_from_db()
        self.populate_streams()

    def populate_streams(self):
        stack_streams = self.get_stack_streams()
        print(stack_streams)
        self.stream_name_lw.clear()
        if stack_streams:
            for stream in stack_streams:
                get_stream_name = stream.rsplit(".", 1)[1]
                item = QtWidgets.QListWidgetItem(get_stream_name)
                item.setData(QtCore.Qt.UserRole, stream)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.stream_name_lw.addItem(item)

    def get_stack_streams(self):
        stack_steams = self.asset_class.operations().find_empty_stack_streams()

        if self.asset_class.type != "group":
            if stack_steams is None:
                return {}
            if len(stack_steams) == 0:
                return {}
            else:
                return stack_steams

    def get_list_items(self):
        list_items = {}
        for index in range(self.stream_name_lw.count()):
            item = self.stream_name_lw.item(index)
            list_items[index] = item
        return list_items

    def items_checked(self):
        checked_items = {}
        items = self.get_list_items()
        for idx, item in items.items():
            if item.checkState() == QtCore.Qt.Checked:
                checked_items[idx] = item

        return checked_items

    def remove_idx_from_list(self):
        checked_items = self.items_checked()
        checked_items_ids = []
        for idx, item in checked_items.items():
            self.stream_name_lw.takeItem(idx)
            stream_id = item.data(QtCore.Qt.UserRole)
            checked_items_ids.append(stream_id)
        return checked_items_ids

    def remove_doc_from_db(self):
        db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        checked_items_ids = []
        checked_items = self.items_checked()
        for idx, item in checked_items.items():
            stream_id = item.data(QtCore.Qt.UserRole)
            checked_items_ids.append(stream_id)
            self.stream_name_lw.takeItem(idx)

        for checked_item_id in checked_items_ids:
            self.asset_class.operations().remove_stack_stream(stream_id=checked_item_id)
            db_ops.delete_entity_document(doc_id=checked_item_id)





if __name__ == "__main__":
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
                      # 'db_asset_stream_id': 'The_Rock.assets.chr.tafer.main'
                      }

    context_obj = ContextHandler()
    context_obj.load_session(context_sample)

    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = DeleteEmptyStreamsUI(context=context_obj)
    create_asset.show()
    sys.exit(app.exec_())