import sys
from PySide2 import QtWidgets, QtCore
from envars.origin_envars import OriginEnvar
from o_database.entities.actions import Query, Add, Set


class DeleteEmptyStreamsUI(QtWidgets.QDialog):

    def __init__(self, entity_id=None, parent=None):
        super(DeleteEmptyStreamsUI, self).__init__(parent)

        self.setWindowTitle("Create Asset")

        self.entity_id = entity_id

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.populate_streams()

    def create_widgets(self):
        self.show_name_le = QtWidgets.QLabel()
        item_path = ".".join([OriginEnvar().show_name, OriginEnvar().origin_path_hierarchy, OriginEnvar().entry_name])
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
        self.remove_idx_from_list()
        stream_name = self.get_list_items()

        Set().entity(entity_id=self.entity_id).stack_stream = []

        for remaining_item in list(stream_name.values()):
            Add().entity(entity_id=self.entity_id).stack_stream = remaining_item.text()
        self.populate_streams()

    def populate_streams(self):
        stack_streams = self.get_stack_streams()
        self.stream_name_lw.clear()
        if stack_streams:
            for stream in stack_streams:
                item = QtWidgets.QListWidgetItem(stream)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.stream_name_lw.addItem(item)

    def get_stack_streams(self):
        spare_it = {}
        curr_asset_type = Query().entity(entity_id=self.entity_id).entity_type
        stack_steams = Query().entity(entity_id=self.entity_id).stack_stream

        if curr_asset_type != "group":
            if len(stack_steams) == 0:
                return spare_it
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
        for idx, item in checked_items.items():
            self.stream_name_lw.takeItem(idx)



if __name__ == "__main__":
    db_path = ["assets", "characters"]
    OriginEnvar.show_name = "New_World"
    OriginEnvar().origin_path_hierarchy = db_path

    OriginEnvar.entry_name = "hulk"
    OriginEnvar.task_name = "modeling"

    app = QtWidgets.QApplication(sys.argv)
    try:
        create_asset.close()
        create_asset.deleteLater()
    except:
        pass
    create_asset = DeleteEmptyStreamsUI()
    create_asset.show()
    sys.exit(app.exec_())