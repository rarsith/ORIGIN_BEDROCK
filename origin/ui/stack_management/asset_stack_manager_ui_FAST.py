import os

from PySide2 import QtWidgets, QtGui, QtCore

from origin.envars.origin_envars import ContextHandler


class StackLoader(QtWidgets.QTableWidget):

    def __init__(self, parent=None):
        super(StackLoader, self).__init__(parent)

        self.setColumnCount(2)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.verticalScrollBar().setVisible(False)
        self.horizontalScrollBar().setVisible(False)

        self.setShowGrid(False)
        vertical_header = self.verticalHeader()

        for row in range(self.rowCount()):
            self.setRowHeight(row, 10)

        self.setAlternatingRowColors(False)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        vertical_header.setDefaultSectionSize(2)
        vertical_header.hide()
        horizontal_header = self.horizontalHeader()
        horizontal_header.setMinimumHeight(2)
        horizontal_header.setMaximumHeight(3)
        horizontal_header.hide()

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setStyleSheet("""
            QTreeWidget::item:selected {
                background: transparent;
                color: black;  /* Change text color to the normal one */
            }
            QTreeWidget::item:hover {
                background: transparent;
            }
        """)


class AssetStackManager(QtWidgets.QWidget):

    def __init__(self, pub_options=None, parent=None):
        super(AssetStackManager, self).__init__(parent)

        self.pub_options = pub_options
        self.context_handler = None
        if self.pub_options is not None:
            self.context_handler = self.pub_options["context_object"]

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.load_existing_stack_streams()
        self.populate_widget()

    def reinitialize(self, pub_options=None):
        self.pub_options = pub_options
        self.context_handler: ContextHandler = None
        if self.pub_options is not None:
            self.context_handler = self.pub_options.get("context_object")

        self.load_existing_stack_streams()
        self.populate_widget()

    def create_widgets(self):
        self.stack_loader_lw = StackLoader()
        self.clear_target_btn = QtWidgets.QPushButton("Clear")
        self.create_btn = QtWidgets.QPushButton("Create Stack")
        self.remove_btn = QtWidgets.QPushButton("Delete Stack")

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.stack_loader_lw)

        buttons_layout = QtWidgets.QHBoxLayout()

        buttons_layout.addWidget(self.remove_btn)
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.clear_target_btn)
        buttons_layout.setAlignment(QtCore.Qt.AlignRight)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(buttons_layout)

        horizontal_splitter = QtWidgets.QSplitter()
        horizontal_splitter.setOrientation(QtCore.Qt.Horizontal)
        top_layout.addWidget(horizontal_splitter)

        horizontal_splitter.insertWidget(0, self.stack_loader_lw)
        horizontal_splitter.setSizes([100, 300])

    def create_connections(self):
        self.stack_loader_lw.itemSelectionChanged.connect(self.get_selected_stack)

    def load_existing_stack_streams(self):
        pass

    def populate_widget(self):
        current_stream_doc = self.get_stream_stacks()
        if current_stream_doc is not None:
            stream_stacks = current_stream_doc.stacks

            if stream_stacks is not None:
                row_count = (len(stream_stacks))
                self.stack_loader_lw.setRowCount(row_count)

                for row, items in enumerate(stream_stacks):
                    stream_name = items.split(".")[-2]
                    item = QtWidgets.QTableWidgetItem(stream_name)
                    item.setData(QtCore.Qt.UserRole, items)
                    item_type = QtWidgets.QTableWidgetItem(self.pub_options["publish_type"])
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                    item_type.setFlags(item_type.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.stack_loader_lw.setItem(row, 0, item)
                    self.stack_loader_lw.setItem(row, 1, item_type)

    def get_stream_stacks(self):
        if self.context_handler is not None:
            current_stream = self.context_handler.database_handler().get_db_asset_stream_document()
            if current_stream is not None:
                return current_stream
            else:
                return None

    def get_selected_stack(self):
        selected = self.stack_loader_lw.selectedItems()
        if selected:
            return selected[0].data(QtCore.Qt.UserRole)

    def get_selected_options(self):
        current_selected_stack_id = self.get_selected_stack()
        self.context_handler.stack_id = current_selected_stack_id
        if current_selected_stack_id is not None:
            return {"stack_db_asset_id": current_selected_stack_id}
        else:
            return None


class LoaderMainUI(QtWidgets.QMainWindow):
    def __init__(self, pub_options=None, parent=None):
        super(LoaderMainUI, self).__init__(parent)

        self.central_widget = AssetStackManager(pub_options=pub_options)

        self.setWindowTitle(f"Asset Stack Manager")

        self.setCentralWidget(self.central_widget)
        self.show()


if __name__ == "__main__":
    import sys

    origin_dev_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

    context_sample = {'asset_breakdown_id': None,
'asset_breakdown_version_id': 'Black_Rock.assets.characters.tafar.tafar_BLACK.breakdown.v0003',
'db_asset_id': 'Black_Rock.assets.characters.tafar.geometry.tafar_BLACK',
'db_asset_stream_id': 'Black_Rock.assets.characters.tafar.tafar_BLACK',
'db_asset_type': None,
'db_asset_version_id': 'Black_Rock.assets.characters.tafar.geometry.tafar_BLACK.v0003',
'entity_id': 'Black_Rock.assets.characters.tafar',
'entity_name': 'tafar',
'entity_type': 'asset',
'origin_path_hierarchy': 'assets.characters',
'project_control': 'Black_Rock__CONTROL',
'project_publishes': 'Black_Rock__PUBLISHES',
'project_work': 'Black_Rock__WORK',
'publish_id': None,
'show_name': 'Black_Rock',
'stack_id': 'Black_Rock.assets.characters.tafar.tafar_BLACK.asset_stack',
'stack_version_id': None,
'task_id': 'Black_Rock.assets.characters.tafar.modeling',
'task_name': 'modeling',
'task_type': 'modeling'}

    context_obj = ContextHandler()
    context_obj.load_session(session_data=context_sample)

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    options = {'publish_type': 'geometry',
               'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer_main',
               'context_object': context_obj,
               'db_asset_qc': 'OK',
               'user_file_formats': ['abc', 'usd', 'obj'],
               'persistent_file_formats': ['master'],
               'material_collections': {},
               'inject_textures_path': None,
               'bundle_db_asset_id': '',
               'review_options': [],
               'pub_comment': '',
               'pub_status': 'WIP'}

    test_dialog = LoaderMainUI(pub_options=options)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        test_dialog.setStyleSheet(_style)

    # test_dialog.populate_widget()
    test_dialog.show()
    sys.exit(app.exec_())