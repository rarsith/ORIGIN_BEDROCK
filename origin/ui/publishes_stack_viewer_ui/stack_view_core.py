import os

from PySide2 import QtWidgets, QtGui, QtCore
from origin.database.mongo import CollectionOperators
from origin.envars.origin_envars import ContextHandler
from origin.ui.publishes_stack_viewer_ui.stack_view_UI import StackViewUI
from origin.ui.status_widgets.publish_status_wdg import PublishStatusWidget

origin_dev_root = os.getenv("ORIGIN_ROOT")
img_path = os.path.normpath(os.path.join(origin_dev_root, "origin/icons/play_icon_vsmall.png"))
thumbnail_path = os.path.normpath(os.path.join(origin_dev_root, "origin/dcc/icons/movie_pic.png"))


class PublishThumbnailViewer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PublishThumbnailViewer, self).__init__(parent)

        self.create_widget()
        self.create_layout()

    def create_widget(self):
        self.label_icon = QtWidgets.QLabel()

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.label_icon)
        main_layout.setMargin(0)

    def set_thumbnail(self, icon_path, thumbnail_width, thumbnail_height):
        self.label_icon.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap(icon_path).scaled(thumbnail_width, thumbnail_height)
        self.label_icon.setPixmap(pixmap)


class StackViewCore(StackViewUI):
    current_context = QtCore.Signal(object)
    changes_to_database = []

    def __init__(self, parent=None):
        super(StackViewCore, self).__init__(parent)

        self.context_handler = None
        self.create_connections()
        self.tweak_ui()

    def create_connections(self):
        self.publish_view_tw.itemSelectionChanged.connect(self.get_current_selected_publish)
        self.refresh_btn.clicked.connect(self.populate_widget)
        self.save_changes_btn.clicked.connect(self.commit_changes)

    def tweak_ui(self):
        self.publish_view_tw.setColumnHidden(10, True)
        self.publish_view_tw.setColumnHidden(9, True)
        self.publish_view_tw.setColumnHidden(8, True)
        self.publish_view_tw.setColumnHidden(7, True)
        self.publish_view_tw.setColumnHidden(6, True)
        self.publish_view_tw.setColumnHidden(2, True)
        self.publish_view_tw.setColumnHidden(4, True)
        self.publish_view_tw.setColumnHidden(5, True)
        self.publish_view_tw.setColumnHidden(0, True)

    def context_receiver(self, context: ContextHandler):
        self.context_handler = context

    def commit_changes(self):
        db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        db_ops.multiple_ops(self.changes_to_database)
        self.populate_widget()
        self.changes_to_database.clear()
        self.check_changes()

    def publish_widget_construct(self, root_item, publish_data):
        publish_item = QtWidgets.QTreeWidgetItem(root_item)

        self.publish_thumbnail_small = PublishThumbnailViewer()
        self.publish_thumbnail_small.set_thumbnail(icon_path=thumbnail_path,
                                                   thumbnail_width=30,
                                                   thumbnail_height=15)

        self.publish_name_capture = publish_data["label"]
        self.get_version = publish_data["version"]

        self.get_status = publish_data["status"]
        self.status_cb = PublishStatusWidget()
        self.status_cb.setCurrentText(self.get_status)

        db_asset_version_type = (publish_data["db_asset_type"]).split("__")[1]
        self.pub_asset_type = db_asset_version_type.capitalize()

        self.asset_task_type = (publish_data["parent_task_type"]).capitalize()

        self.published_by = publish_data["owner"]

        pub_date = publish_data["date"]
        pub_time = publish_data["time"]

        self.published_date = f"{pub_date} {pub_time}"

        self.get_description = publish_data["description"]  # TODO: implement DESCRIPTION in the task attributes

        self.published_id = publish_data["_id"]
        self.published_parent = publish_data["parent"]
        self.published_has_notes = "description"

        # Connections
        self.status_cb.currentIndexChanged.connect(self.changed_status)

        self.publish_view_tw.setItemWidget(publish_item, 0, self.publish_thumbnail_small)
        # publish_item.setText(0, "---")
        publish_item.setText(1, self.publish_name_capture)
        publish_item.setText(2, self.get_version)
        publish_item.setText(3, self.status_cb.currentText())
        self.publish_view_tw.setItemWidget(publish_item, 3, self.status_cb)
        publish_item.setText(4, self.pub_asset_type)
        publish_item.setText(5, self.asset_task_type)
        publish_item.setText(6, self.published_by)
        publish_item.setText(7, self.published_date)
        publish_item.setText(8, self.get_description)
        publish_item.setData(9, 1, self.published_id)
        publish_item.setText(10, self.published_parent)
        publish_item.setText(11, self.published_has_notes)

        return publish_item

    def changed_status(self, data):
        sender = self.sender()
        current_publish_id = self.get_current_selected_publish()
        if current_publish_id:
            attr_path = "status"
            attr_value = sender.currentText()
            self.changes_to_database.append({current_publish_id: {attr_path: attr_value}})
            self.check_changes()
            return {attr_path: attr_value}

    def check_changes(self):
        from origin.ui.style import buttons_styles as btns

        if len(self.changes_to_database) != 0:
            self.save_changes_btn.setStyleSheet("background-color: #db70b8; color: black")
        else:
            self.save_changes_btn.setStyleSheet(btns.hover_orange)

    def populate_widget(self):
        self.changes_to_database.clear()
        stack_versions = self.get_publishes()

        self.publish_view_tw.clear()
        published_doc_buff = self.stored_buffer(doc_id_list=stack_versions)
        if published_doc_buff is not None:
            self.publish_view_tw.setUpdatesEnabled(False)
            self.publish_view_tw.addTopLevelItems(published_doc_buff)
            self.publish_view_tw.setUpdatesEnabled(True)

    def stored_buffer(self, doc_id_list):
        buffer = []
        if doc_id_list is not None:
            for stack_slot, db_asset_id in doc_id_list.items():
                fetch_ent = CollectionOperators(db_collection=self.context_handler.project_publishes)
                published_doc = fetch_ent.entity_document(doc_id=db_asset_id)
                if published_doc is not None:
                    root_item = self.publish_view_tw.invisibleRootItem()
                    row_item = self.publish_widget_construct(root_item=root_item, publish_data=published_doc)
                    buffer.append(row_item)
            return buffer

    def get_publishes(self):
        if self.context_handler.db_asset_type == "db_asset__stack_version":
            fetch_ent = CollectionOperators(db_collection=self.context_handler.project_publishes)
            stack_version_doc = fetch_ent.entity_document(doc_id=self.context_handler.db_asset_version_id)

            return stack_version_doc["data"]
        else:
            return None

    def get_current_selected_publish(self):
        get_selected_publish = self.publish_view_tw.selectedItems()
        if get_selected_publish:
            for item in get_selected_publish:
                get_publish_id = item.data(9, 1)
                self.context_handler.db_asset_version_id = get_publish_id
                self.current_context.emit(self.context_handler)
                return get_publish_id

    def get_current_selected(self):
        selected = self.publish_view_tw.selectedItems()
        return selected


if __name__ == "__main__":
    import sys

    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'tafer',
                      'entity_id': 'The_Rock.assets.chr.tafer',
                      'asset_breakdown_id': 'The_Rock.assets.chr.tafer.breakdown',
                      'entity_type': 'asset',
                      'task_name': "modeling",
                      'task_type': "modeling",
                      'task_id': "The_Rock.assets.chr.tafer.modeling",
                      'db_asset_id': 'The_Rock.assets.chr.tafer.tafer_main.asset_stack.v0008',
                      'db_asset_version_id': 'The_Rock.assets.chr.tafer.tafer_main.asset_stack.v0008',
                      'db_asset_type': 'db_asset__stack_version',
                      'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer_main',
                      'stack_id': 'The_Rock.assets.chr.tafer.tafer_main.asset_stack'
                      }

    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.props',
                      'entity_name': 'knife',
                      'entity_id': 'The_Rock.assets.props.knife',
                      'asset_breakdown_id': 'The_Rock.assets.props.knife.breakdown',
                      'entity_type': 'asset',
                      'task_name': "modeling",
                      'task_type': "modeling",
                      'task_id': "The_Rock.assets.props.knife.modeling",
                      'db_asset_stream_id': 'The_Rock.assets.props.knife.knife_main',
                      'db_asset_id': 'The_Rock.assets.props.knife.geometry.knife_main',
                      'db_asset_version_id': 'The_Rock.assets.props.knife.knife_main.asset',

                      'stack_id': 'The_Rock.assets.props.knife.knife_main.asset_stack',
                      }

    app = QtWidgets.QApplication(sys.argv)

    context = ContextHandler()
    context.load_session(session_data=context_sample)

    test_dialog = StackViewCore()
    test_dialog.context_receiver(context)

    # randomize_pub_statuses(widget=test_dialog)

    test_dialog.populate_widget()

    test_dialog.show()
    sys.exit(app.exec_())
