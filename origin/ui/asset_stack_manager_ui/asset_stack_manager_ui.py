import os
import pprint

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QIcon, QFont, QBrush, QColor
from PySide2.QtWidgets import QVBoxLayout, QTableWidgetItem, QMenu

from origin.database.entities.operators import Project, Asset, Projects, AssetBreakdown
from origin.database.mongo import CollectionOperators
from origin.database.publisher.db_publisher import DBPublisher
from origin.envars.origin_envars import ContextHandler
from origin.ui.project_viewer_ui.project_tree_viewer_core import ProjectTreeViewerCore
from origin.ui.publish.origin_publisher import OriginPublisher
from origin.ui.status_widgets.color_settings import match_color_scheme
from origin.ui.status_widgets.publish_status_wdg import PublishStatusWidget
from origin.ui.stream_viewer_ui.stream_viewer_UI import StreamViewerUI


class CustomListWidget(QtWidgets.QListWidget):
    def mousePressEvent(self, event):
        # Check if the click is on an item
        item = self.itemAt(event.pos())
        if item is None:
            # If no item is clicked, clear the selection
            self.clearSelection()
        # Call the base class implementation to handle other mouse events
        super().mousePressEvent(event)


class StreamsLoaderUI(QtWidgets.QWidget):
    current_context = QtCore.Signal(object)

    def __init__(self, context: ContextHandler = None, current_stream=None, parent=None):
        super(StreamsLoaderUI, self).__init__(parent)

        self.context_handler = context

        self.current_stream = current_stream

        self.create_widgets()
        self.create_connections()
        self.create_layout()

    def create_widgets(self):
        self.stack_stream_lw = CustomListWidget()
        self.stack_stream_lw.setFocusPolicy(QtCore.Qt.NoFocus)
        self.streams_lb = QtWidgets.QLabel("Streams")

    def create_connections(self):
        self.stack_stream_lw.itemClicked.connect(self.update_context)
        self.stack_stream_lw.itemSelectionChanged.connect(self.update_context)

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.streams_lb)
        main_layout.addWidget(self.stack_stream_lw)
        main_layout.setContentsMargins(0,0,0,0)

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
        if entity_doc is not None:
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
        selected_item = self.stack_stream_lw.selectedItems()
        current_item = selected_item[0] if selected_item else None
        if current_item is not None:
            item_data = current_item.data(QtCore.Qt.UserRole)
            self.context_handler.db_asset_stream_id = item_data
            self.current_context.emit(self.context_handler)
        else:
            self.context_handler.db_asset_stream_id = None
            self.current_context.emit(self.context_handler)


class AssetStackSlotsLoaderWDG(QtWidgets.QWidget):
    current_context = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(AssetStackSlotsLoaderWDG, self).__init__(parent)

        self.context_handler = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.stack_slots_loader_tw = QtWidgets.QTableWidget()
        self.stack_slots_loader_tw.setColumnCount(4)
        self.stack_slots_loader_tw.setHorizontalHeaderLabels(['Slots Type', 'Slots Versions Streams', 'Status', 'Version'])

        self.stack_slots_loader_tw.setColumnWidth(0, 120)
        self.stack_slots_loader_tw.setColumnWidth(1, 300)
        self.stack_slots_loader_tw.setColumnWidth(2, 300)

        header = self.stack_slots_loader_tw.horizontalHeader()
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.stack_slots_loader_tw.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.stack_slots_loader_tw.verticalHeader().setVisible(False)
        self.stack_slots_loader_tw.setShowGrid(False)
        self.stack_slots_loader_tw.setFocusPolicy(Qt.NoFocus)

        self.stack_slots_loader_tw.setContextMenuPolicy(Qt.CustomContextMenu)
        self.stack_slots_loader_tw.customContextMenuRequested.connect(self.on_context_menu)

        self.stack_version_lb = QtWidgets.QLabel()
        self.stack_status_lb = QtWidgets.QLabel()

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.stack_version_lb)
        top_layout.addStretch(1)
        top_layout.addWidget(self.stack_status_lb)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.stack_slots_loader_tw)

    def create_connections(self):
        self.stack_slots_loader_tw.selectionModel().selectionChanged.connect(self.update_context)

    def context_receiver(self, context: ContextHandler):
        self.context_handler = context

    def on_context_menu(self, pos: QPoint):
        # Map point to global position
        global_pos = self.stack_slots_loader_tw.viewport().mapToGlobal(pos)

        # Get the row under the click
        row = self.stack_slots_loader_tw.rowAt(pos.y())
        if row < 0:
            return  # clicked outside rows

        version_id_item = self.stack_slots_loader_tw.item(row, 1)
        version_id_item_data = version_id_item.data(Qt.UserRole)

        # Example: retrieve data from the row
        row_data = {
            "id": self.stack_slots_loader_tw.item(row, 0).text(),
            "name": {row: version_id_item_data},
            "status": self.stack_slots_loader_tw.item(row, 3).text()
        }

        # Create menu
        menu = QMenu()
        menu.addAction("Update to Current", lambda: self.update_slot_to_current(row_data["name"]))
        menu.addAction("Add Slot...", lambda: self.add_slot(row_data))
        menu.addAction("Replace Slot...", lambda: self.add_slot(row_data))
        menu.addAction("Reset Changes...", lambda: self.add_slot(row_data))

        # Show menu
        menu.exec_(global_pos)

    def update_slot_to_current(self, data):
        for row, db_doc_obj in data.items():
            current_version_doc = self.get_current_version(db_doc_obj=db_doc_obj)
            self.populate_slot(row=row, version_doc=current_version_doc)
        # print(current_version_doc)

    def add_slot(self, data):
        print(data)

    def _get_stream_stack(self):
        self.db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)

        if self.context_handler.db_asset_stream_id is not None:
            stream_stack_db_asset_id = ".".join([self.context_handler.db_asset_stream_id + "." + "asset_stack"])
            stack_doc = self.db_ops.entity_document(doc_id=stream_stack_db_asset_id)
            return stack_doc

        else:
            return None

    def get_current_version_doc(self):
        db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        stack_doc = self._get_stream_stack()

        if stack_doc is not None:
            current_doc = db_ops.get_current_version(_id={"$regex": f"^{stack_doc['_id']}"})
            if len(current_doc) != 0:
                return current_doc[0]
        else:
            return

    def get_stack_slots(self):
        extract_version = self.get_current_version_doc()

        if extract_version is not None:
            self.stack_version_lb.setText(extract_version['name'])
            self.stack_version_lb.setStyleSheet("""
                    font-weight: bold;
                    font-size: 11px;
                    """)

            self.stack_status_lb.setText(extract_version['status'])
            self.stack_status_lb.setMinimumWidth(150)
            self.stack_status_lb.setAlignment(Qt.AlignCenter)
            color_schema = match_color_scheme(extract_version['status'])
            self.stack_status_lb.setStyleSheet(color_schema)
            return extract_version["data"]

        else:
            return None

    def check_if_current(self, doc_id: str = None):
        if doc_id is not None:
            version_parent = doc_id.rsplit(".", 1)[0]
            db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
            current_doc = db_ops.get_current_version(_id={"$regex": f"^{version_parent}"})
            if len(current_doc) != 0:
                return doc_id==current_doc[0]["_id"]
        else:
            return None

    def get_current_version(self, db_doc_obj: str = None):
        if db_doc_obj is not None:
            doc_id = db_doc_obj.id

            version_parent = doc_id.rsplit(".", 1)[0]
            db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
            current_doc = db_ops.get_current_version(_id={"$regex": f"^{version_parent}"})
            if len(current_doc) != 0:
                return current_doc[0]
        else:
            return None

    def stack_slot_item(self, current=True):
        slot_item = QtWidgets.QTableWidgetItem()

        if current:
            slot_item.setData(Qt.FontRole, QFont("Arial", 8, QFont.Bold))
            slot_item.setForeground(QColor(0, 170, 0))
        else:
            slot_item.setData(Qt.FontRole, QFont("Arial", 8, QFont.Bold))
            slot_item.setForeground(QColor(170, 0, 0))

        return slot_item

    def populate_slot(self, row, version_doc):

        is_current = self.check_if_current(version_doc["_id"])

        slot_type_item = self.stack_slot_item(current=is_current)
        slot_name_item = self.stack_slot_item(current=is_current)
        slot_version_item = self.stack_slot_item(current=is_current)

        # row = self.stack_slots_loader_tw.rowCount()
        # self.stack_slots_loader_tw.insertRow(row)

        asset_doc = Asset(**version_doc)
        asset_version_id = asset_doc.id

        asset_version_name = "__".join(asset_version_id.split(".")[3:-1])
        asset_version_cnt = asset_version_id.split(".")[-1]

        slot_type = self.stack_slots_loader_tw.item(row, 0).text()
        slot_type_item.setText(str(slot_type))
        self.stack_slots_loader_tw.setItem(row, 0, slot_type_item)

        slot_name_item.setText(str(asset_version_name))
        self.stack_slots_loader_tw.setItem(row, 1, slot_name_item)
        slot_name_item.setData(Qt.UserRole, asset_doc)

        status_widget = QtWidgets.QLabel()
        status_widget.setText(asset_doc.status)
        status_widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        color_schema = match_color_scheme(asset_doc.status)
        status_widget.setStyleSheet(color_schema)
        self.stack_slots_loader_tw.setCellWidget(row, 2, status_widget)

        slot_version_item.setText(str(asset_version_cnt))
        slot_version_item.setTextAlignment(Qt.AlignCenter)
        self.stack_slots_loader_tw.setItem(row, 3, slot_version_item)

    def populate_stack_slots(self):
        self.stack_slots_loader_tw.setRowCount(0)
        stack_slots_versions = self.get_stack_slots()

        if stack_slots_versions is not None:
            for slot_type, asset_version in stack_slots_versions.items():
                is_current = self.check_if_current(asset_version)

                slot_type_item = self.stack_slot_item(current=is_current)
                slot_name_item = self.stack_slot_item(current=is_current)
                slot_version_item = self.stack_slot_item(current=is_current)

                row = self.stack_slots_loader_tw.rowCount()
                self.stack_slots_loader_tw.insertRow(row)

                db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
                entity_doc = db_ops.entity_document(doc_id=asset_version)
                asset_doc = Asset(**entity_doc)


                asset_version_name = "__".join(asset_version.split(".")[3:-1])
                asset_version_cnt = asset_version.split(".")[-1]

                slot_type_item.setText(str(slot_type))
                self.stack_slots_loader_tw.setItem(row, 0, slot_type_item)

                slot_name_item.setText(str(asset_version_name))
                self.stack_slots_loader_tw.setItem(row, 1, slot_name_item)
                slot_name_item.setData(Qt.UserRole, asset_doc)

                status_widget = QtWidgets.QLabel()
                status_widget.setText(asset_doc.status)
                status_widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                color_schema = match_color_scheme(asset_doc.status)
                status_widget.setStyleSheet(color_schema)
                self.stack_slots_loader_tw.setCellWidget(row, 2, status_widget)

                slot_version_item.setText(str(asset_version_cnt))
                slot_version_item.setTextAlignment(Qt.AlignCenter)
                self.stack_slots_loader_tw.setItem(row, 3, slot_version_item)

        else:
            return

    def update_context(self):
        stream_stack_doc = self._get_stream_stack()
        self.context_handler.stack_id = stream_stack_doc["_id"]
        self.current_context.emit(self.context_handler)

class AssetStackManagerUI(QtWidgets.QWidget):
    def __init__(self,  context: ContextHandler = None, parent=None):
        super(AssetStackManagerUI, self).__init__(parent)

        self.setWindowTitle("Asset Stack Manager")

        self.context_handler = context

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)

    def create_widgets(self):
        self.project_tree_viewer = ProjectTreeViewerCore(has_project_select_wdg=True,
                                                         has_create_new_proj=False,
                                                         has_context_menu=False)
        self.project_tree_viewer.context_handler = self.context_handler
        self.project_tree_viewer.set_show_to(self.context_handler.show_name)
        self.project_tree_viewer.expand_tree_from_context()

        self.streams_viewer_wdg = StreamsLoaderUI(context=self.context_handler, parent=self)
        self.streams_viewer_wdg.setMaximumWidth(200)
        self.streams_viewer_wdg.populate_widget()

        self.stack_slots_viewer_wdg = AssetStackSlotsLoaderWDG()

        self.refresh_bn = QtWidgets.QPushButton("Refresh")
        self.publish_bn = QtWidgets.QPushButton("Publish")
        self.close_bn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        vertical_splitter = QtWidgets.QSplitter()
        vertical_splitter.setOrientation(QtCore.Qt.Horizontal)

        vertical_splitter.insertWidget(0, self.project_tree_viewer)
        vertical_splitter.insertWidget(1, self.streams_viewer_wdg)
        vertical_splitter.insertWidget(2, self.stack_slots_viewer_wdg)
        vertical_splitter.setContentsMargins(0,0,0,0)
        vertical_splitter.setSizes([180, 200, 850])

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(vertical_splitter)
        main_layout.addWidget(self.refresh_bn)
        main_layout.addWidget(self.publish_bn)
        main_layout.addWidget(self.close_bn)

    def create_connections(self):
        self.project_tree_viewer.current_context.connect(self.streams_viewer_wdg.context_receiver)
        self.project_tree_viewer.project_tree_viewer_wdg.itemSelectionChanged.connect(self.streams_viewer_wdg.populate_widget)
        self.project_tree_viewer.project_tree_viewer_wdg.itemClicked.connect(self.streams_viewer_wdg.populate_widget)

        self.streams_viewer_wdg.current_context.connect(self.stack_slots_viewer_wdg.context_receiver)
        self.streams_viewer_wdg.stack_stream_lw.itemClicked.connect(self.stack_slots_viewer_wdg.populate_stack_slots)
        self.streams_viewer_wdg.stack_stream_lw.itemSelectionChanged.connect(self.stack_slots_viewer_wdg.populate_stack_slots)

        self.stack_slots_viewer_wdg.current_context.connect(self.current_context_receiver)
        self.close_bn.clicked.connect(self.close)


        self.publish_bn.clicked.connect(self.publish)

    def closeEvent(self, event):
        self.deleteLater()
        event.accept()

    def current_context_receiver(self, context: ContextHandler):
        self.context_handler = context
        
    def publish(self):
        gather_ui_data = {}

        rows = self.stack_slots_viewer_wdg.stack_slots_loader_tw.rowCount()
        for row in range(rows):
            slot_name_item = self.stack_slots_viewer_wdg.stack_slots_loader_tw.item(row, 0)
            version_id_item = self.stack_slots_viewer_wdg.stack_slots_loader_tw.item(row, 1)
            version_id_data = version_id_item.data(Qt.UserRole)

            version_id = version_id_data.id

            gather_ui_data.update({slot_name_item.text(): version_id})
        pprint.pprint(gather_ui_data)

        db_pub = DBPublisher()
        new_stack_id = db_pub.create_stack_version(context=self.context_handler, slots=gather_ui_data)
        print(f"NEW STACK {new_stack_id}")
        #
        window = OriginPublisher(context=self.context_handler, publish_type="asset_stack", parent=self)
        # window.setGeometry(100, 100, 700, 300)
        # window.setWindowFlags(QtCore.Qt.Window)
        # window.show()

class AssetStackManagerMain(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AssetStackManagerMain, self).__init__(parent)

        self.main_wdg = AssetStackManagerUI()
        self.setCentralWidget(self.main_wdg)
        self.show()


if __name__ == "__main__":
    os.environ["DCC"] = "origin_standalone"

    from origin.ui.tests.manual_cotext import test_ui
    test_ui(main_widget=AssetStackManagerUI)

    pub_options = {'publish_type': 'geometry',
                   'db_asset_stream_id':'The_Rock.assets.props.rock.rock_main',
                   'context_object': "<origin.envars.origin_envars.ContextHandler object at 0x000002267E369C90>",
                   'db_asset_qc': 'OK',
                   'user_file_formats': ['abc', 'usd', 'obj'],
                   'persistent_file_formats': ['master'],
                   'material_collections': {},
                   'inject_textures_path': None,
                   'stack_db_asset_id': 'The_Rock.assets.props.rock.rock_main.asset_stack',
                   'review_medium': 'playblast',
                   'review_options': {'frame_range': (1001, 1101),
                                      'resolution': (1920, 1080),
                                      'resolution_percentage': 1,
                                      'template_asset_ver_id': 'X:/projects/The_Rock/templates/maya/playblast/template/publishes/data/template__playblast__playblast_main/maya__playblast__playblast_main__v0006/origin_scene/maya__playblast__playblast_main__v0006.mb',
                                      'camera_asset_ver_id': 'X:/projects/The_Rock/assets/props/rock/modeling/publishes/data/turntable_camera__rock__rock_main/props__rock__rock_main__v0002/alembic/props__rock__rock_main__v0002.abc'}
                   }


