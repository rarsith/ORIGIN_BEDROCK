from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QVBoxLayout

from origin.database.entities.operators import Project, Asset, Projects
from origin.database.mongo import CollectionOperators
from origin.envars.origin_envars import ContextHandler
from origin.ui.project_viewer_ui.project_tree_viewer_core import ProjectTreeViewerCore
from origin.ui.stream_viewer_ui.stream_viewer_UI import StreamViewerUI


class AssetStackSlotsLoaderWDG(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(AssetStackSlotsLoaderWDG, self).__init__(parent)

        self.context_handler = None

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Slots Type', 'Slots Versions Streams'])

        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def context_receiver(self, context: ContextHandler):
        self.context_handler = context

    def get_stack_streams(self):
        db_ops = CollectionOperators(db_collection=self.context_handler.show_name)
        entity_doc = db_ops.entity_document(doc_id=self.context_handler.entity_id)
        asset_doc = Asset(**entity_doc)

        curr_asset_type = self.context_handler.entity_type
        stack_steams = asset_doc.stack_streams
        asset_breakdown = asset_doc.get_asset_breakdown()

        if curr_asset_type != "group":
            if stack_steams is None:
                return {}
            if len(stack_steams) == 0:
                return {}
            else:
                return stack_steams

    def _get_stream_stack(self):
        self.db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)

        if self.context_handler.db_asset_stream_id is not None:
            stream_stack_db_asset_id = ".".join([self.context_handler.db_asset_stream_id + "." + "asset_stack"])
            stack_doc = self.db_ops.entity_document(doc_id=stream_stack_db_asset_id)
            print(stack_doc)
            return stack_doc

        else:
            return None

    def _get_stream_stack_versions(self):
        stream_stack = self._get_stream_stack()

        if stream_stack is not None:
            return stream_stack["children"]
        else:
            return None

    def get_stack_current_version(self):
        stack_docs = []
        stack_versions = self._get_stream_stack_versions()
        if stack_versions is not None:
            for version_id in stack_versions:
                stack_doc = self.db_ops.entity_document(doc_id=version_id)
                stack_docs.append(stack_doc)

            return stack_docs
        return None

    def pick_best_document(self, docs: list[dict]) -> dict | None:
        best = None

        if docs is not None:
            for doc in docs:
                if doc.get("status") not in {"CLIENT APPROVED", "WIP"}:
                    continue
                if "date" not in doc or "time" not in doc:
                    continue

                if best is None:
                    best = doc
                    continue

                if best["status"] != "CLIENT APPROVED" and doc["status"] == "CLIENT APPROVED":
                    best = doc
                    continue

                if doc["status"] == best["status"]:
                    if (doc["date"], doc["time"]) > (best["date"], best["time"]):
                        best = doc

            return best
        else:
            return None

    def populate_stack_slots(self):
        test = self.get_stack_current_version()
        extract_version = self.pick_best_document(test)
        print("STACK:  ", extract_version)


class AssetStackManagerUI(QtWidgets.QWidget):
    def __init__(self,  context: ContextHandler = None, parent=None):
        super(AssetStackManagerUI, self).__init__(parent)

        self.context_handler = context

        self.create_widgets()
        self.create_layout()
        self.create_conections()

        self.setMinimumWidth(800)
        self.setMinimumHeight(500)

    def create_widgets(self):
        self.project_tree_viewer = ProjectTreeViewerCore(has_project_select_wdg=True,
                                                         has_create_new_proj=False,
                                                         has_context_menu=False)
        self.project_tree_viewer.context_handler = self.context_handler
        self.project_tree_viewer.set_show_to(self.context_handler.show_name)
        self.project_tree_viewer.expand_tree_from_context()

        self.stack_viewer_wdg = StreamViewerUI(context=self.context_handler, parent=self)
        self.stack_viewer_wdg.create_new_stream_btn.hide()
        self.stack_viewer_wdg.delete_empty_streams_btn.hide()
        self.stack_viewer_wdg.setMaximumWidth(200)
        self.stack_viewer_wdg.populate_widget()

        self.db_asset_viewer_wdg = AssetStackSlotsLoaderWDG()
        self.refresh_bn = QtWidgets.QPushButton("Refresh")
        self.publish_bn = QtWidgets.QPushButton("Publish")
        self.close_bn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.project_tree_viewer)
        top_layout.addWidget(self.stack_viewer_wdg)
        top_layout.addWidget(self.db_asset_viewer_wdg)

        vertical_splitter = QtWidgets.QSplitter()
        vertical_splitter.setOrientation(QtCore.Qt.Horizontal)

        vertical_splitter.insertWidget(0, self.project_tree_viewer)
        vertical_splitter.insertWidget(1, self.stack_viewer_wdg)
        vertical_splitter.insertWidget(2, self.db_asset_viewer_wdg)
        vertical_splitter.setSizes([150, 890, 465, 150])

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(vertical_splitter)
        main_layout.addWidget(self.refresh_bn)
        main_layout.addWidget(self.publish_bn)
        main_layout.addWidget(self.close_bn)

    def create_conections(self):
        self.project_tree_viewer.current_context.connect(self.stack_viewer_wdg.context_receiver)
        self.project_tree_viewer.project_tree_viewer_wdg.itemSelectionChanged.connect(self.stack_viewer_wdg.populate_widget)
        self.project_tree_viewer.project_tree_viewer_wdg.itemClicked.connect(self.stack_viewer_wdg.populate_widget)

        self.stack_viewer_wdg.current_context.connect(self.db_asset_viewer_wdg.context_receiver)
        self.stack_viewer_wdg.stack_stream_lw.itemClicked.connect(self.db_asset_viewer_wdg.populate_stack_slots)
        self.stack_viewer_wdg.stack_stream_lw.itemSelectionChanged.connect(self.db_asset_viewer_wdg.populate_stack_slots)

    def expand_tree_from_id(self, tree_widget):
        parts = self.context_handler.entity_id.split(".")
        parent = None

        for part in parts:
            if parent:
                items = [parent.child(i) for i in range(parent.childCount())]
            else:
                items = [tree_widget.topLevelItem(i) for i in range(tree_widget.topLevelItemCount())]

            for item in items:
                if item.text(0) == part:
                    item.setExpanded(True)
                    tree_widget.setUpdatesEnabled(False)
                    stored_data = item.data(0, QtCore.Qt.UserRole)
                    tree_widget.setUpdatesEnabled(True)
                    if stored_data.type == "asset":
                        tree_widget.setCurrentItem(item)
                        item.setSelected(True)

                    parent = item
                    break

    def current_context_receiver(self, context: ContextHandler):
        self.current_context = context.resolve_to_full_context()
        self.context_viewer.setText(self.current_context)
        return self.current_context

class AssetStackManagerMain(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AssetStackManagerMain, self).__init__(parent)

        self.main_wdg = AssetStackManagerUI()
        self.setCentralWidget(self.main_wdg)
        self.show()



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
    test_dialog = AssetStackManagerUI(context=context_obj)

    test_dialog.show()
    sys.exit(app.exec_())
