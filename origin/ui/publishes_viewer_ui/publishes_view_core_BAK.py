import os
from typing import List

from Qt import QtWidgets, QtGui, QtCore
from origin.database.mongo import CollectionOperators
from origin.envars.origin_envars import ContextHandler
from origin.ui.publishes_viewer_ui.publishes_view_UI import MainPublishesViewUI
from origin.ui.status_widgets.publish_status_wdg import PublishStatusWidget
from origin.database.entities.actions import Create
from origin.database.statuses import DbVersionStatuses

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


class MainPublishesViewCore(MainPublishesViewUI):
    selected_version = QtCore.Signal(object)
    changes_to_database = []
    paginated_ids = []

    def __init__(self, parent=None):
        super(MainPublishesViewCore, self).__init__(parent)

        self.context_handler = None
        self.publishes_docs = None
        self.total_pages = 0
        self.create_connections()

    def create_connections(self):
        self.load_limit_le.returnPressed.connect(self.get_limit_load)
        self.load_limit_le.returnPressed.connect(self.populate_widget)

        self.publish_view_tw.itemSelectionChanged.connect(self.get_current_selected_publish)

        self.go_to_next_page_btn.clicked.connect(self.go_to_next_page)
        self.go_to_prev_page_btn.clicked.connect(self.go_to_previous_page)
        self.go_to_first_page_btn.clicked.connect(self.go_to_first_page)
        self.go_to_last_page_btn.clicked.connect(self.go_to_last_page)

        self.show_current_page_le.returnPressed.connect(self.populate_widget_from_page)

        self.refresh_btn.clicked.connect(self.populate_widget)
        self.save_changes_btn.clicked.connect(self.commit_changes)
        # self.save_changes_btn.clicked.connect(self.resolve_entity_stack)

    def context_receiver(self, context):
        self.context_handler = context

    def resolve_entity_stack(self):
        version_statuses = DbVersionStatuses()
        Create(context=self.context_handler).asset_stack_version_update(status=version_statuses.pending_rev)

    def get_limit_load(self):
        limit_val = self.load_limit_le.text()
        return int(limit_val)

    def get_current_page(self):
        curr_page_val = self.show_current_page_le.text()
        return int(curr_page_val)

    def commit_changes(self):
        db_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        db_ops.multiple_ops(self.changes_to_database)
        self.populate_widget()
        self.changes_to_database.clear()
        self.check_changes()

    def publish_widget_construct(self, root_item, publish_data):
        publish_item = QtWidgets.QTreeWidgetItem(root_item)

        self.publish_thumbnail_small = PublishThumbnailViewer(self.publish_view_tw)
        self.publish_thumbnail_small.set_thumbnail(icon_path=thumbnail_path,
                                                   thumbnail_width=30,
                                                   thumbnail_height=15)

        self.publish_name_capture = publish_data["label"]
        self.get_version = publish_data["version"]

        self.get_status = publish_data["status"]
        self.status_cb = PublishStatusWidget(self.publish_view_tw)
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
        publish_item.setData(10, 1, publish_data["db_asset_type"])
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
        self.publish_view_tw.clear()

        self.get_publishes(page_size=self.get_limit_load(),
                           page_number=self.get_current_page())

        pub_items_wdg = self.buffered_widget_items(self.publishes_docs)

        self.show_total_pages_le.setText(str(self.total_pages))

        self.show_current_page_le.setText("1")

        has_items = len(pub_items_wdg) > 0
        if len(pub_items_wdg) != 0:
            try:
                self.publish_view_tw.setUpdatesEnabled(False)
                self.publish_view_tw.addTopLevelItems(pub_items_wdg)
                self.publish_view_tw.setUpdatesEnabled(True)
            except Exception as e:
                print(f"Error adding items: {e}")

            self.go_to_next_page_btn.setEnabled(has_items)
            self.go_to_prev_page_btn.setEnabled(has_items)
            self.go_to_first_page_btn.setEnabled(has_items)
            self.go_to_last_page_btn.setEnabled(has_items)
            self.show_current_page_le.setEnabled(has_items)
            self.show_total_pages_le.setEnabled(has_items)
            self.load_limit_le.setEnabled(has_items)
        else:
            self.publish_view_tw.clear()
            self.go_to_next_page_btn.setEnabled(has_items)
            self.go_to_prev_page_btn.setEnabled(has_items)
            self.go_to_first_page_btn.setEnabled(has_items)
            self.go_to_last_page_btn.setEnabled(has_items)
            self.show_current_page_le.setEnabled(has_items)
            self.show_total_pages_le.setEnabled(has_items)
            self.load_limit_le.setEnabled(has_items)

    def populate_widget_from_page(self, page_number):
        self.changes_to_database.clear()
        self.publish_view_tw.clear()

        self.get_publishes(page_size=self.get_limit_load(),
                           page_number=page_number)

        pub_items_wdg = self.buffered_widget_items(self.publishes_docs)

        self.show_total_pages_le.setText(str(self.total_pages))

        has_items = len(pub_items_wdg) > 0
        if len(pub_items_wdg) != 0:
            try:
                self.publish_view_tw.setUpdatesEnabled(False)
                self.publish_view_tw.addTopLevelItems(pub_items_wdg)
                self.publish_view_tw.setUpdatesEnabled(True)
            except Exception as e:
                print(f"Error adding items: {e}")

            self.go_to_next_page_btn.setEnabled(has_items)
            self.go_to_prev_page_btn.setEnabled(has_items)
            self.go_to_first_page_btn.setEnabled(has_items)
            self.go_to_last_page_btn.setEnabled(has_items)
            self.show_current_page_le.setEnabled(has_items)
            self.show_total_pages_le.setEnabled(has_items)
            self.load_limit_le.setEnabled(has_items)
        else:
            self.publish_view_tw.clear()
            self.go_to_next_page_btn.setEnabled(has_items)
            self.go_to_prev_page_btn.setEnabled(has_items)
            self.go_to_first_page_btn.setEnabled(has_items)
            self.go_to_last_page_btn.setEnabled(has_items)
            self.show_current_page_le.setEnabled(has_items)
            self.show_total_pages_le.setEnabled(has_items)
            self.load_limit_le.setEnabled(has_items)

    def buffered_widget_items(self, doc_list):
        buffer = []
        for doc in doc_list:
            root_item = self.publish_view_tw.invisibleRootItem()
            row_item = self.publish_widget_construct(root_item=root_item, publish_data=doc)
            buffer.append(row_item)
        return buffer

    def resolve_extra_filters(self, default_filter: List[dict] = None, filters_input: List[dict] = None):
        extra_filters = default_filter
        if filters_input:
            for extra_filter in filters_input:
                extra_filters.append(extra_filter)
        return extra_filters

    def get_publishes(self, page_number, page_size):
        extra_filters = [{"type": ["publish", "db_asset__stack_version"]}]

        if self.context_handler.task_id is not None:
            extra_filters = self.resolve_extra_filters(default_filter=[{"type": ["publish", "db_asset__stack_version"]},
                                                                       {"parent_task_id": self.context_handler.task_id}])

        fetch_ent = CollectionOperators(db_collection=self.context_handler.project_publishes)
        db_extraction = fetch_ent.pagination_entities_attr_value_starts_with(attr_field="_id",
                                                                             val_starts_with=self.context_handler.resolve_to_base_context(),
                                                                             extra_filters=extra_filters,
                                                                             page_number=page_number,
                                                                             page_size=page_size,
                                                                             ids_only=False
                                                                             )

        total_count = db_extraction[0]['total_count'][0]['count'] if db_extraction[0]['total_count'] else 0
        self.total_pages = (total_count + page_size - 1) // page_size

        self.publishes_docs = db_extraction[0]["pages_results"]

    def go_to_next_page(self):
        current_page = self.show_current_page_le.text()
        next_page = int(current_page) + 1
        self.populate_widget_from_page(page_number=next_page)
        if next_page == self.total_pages:
            self.show_current_page_le.setText(str(self.total_pages))
            self.go_to_next_page_btn.setEnabled(False)
            self.go_to_last_page_btn.setEnabled(False)

        else:
            self.show_current_page_le.setText(str(next_page))

    def go_to_previous_page(self):
        current_page = self.show_current_page_le.text()
        previous_page = int(current_page) - 1
        if previous_page != 0:
            self.show_current_page_le.setText(str(previous_page))
            self.populate_widget_from_page(page_number=previous_page)

        else:
            self.go_to_prev_page_btn.setEnabled(False)
            self.go_to_first_page_btn.setEnabled(False)
            self.show_current_page_le.setText("1")

    def go_to_first_page(self):
        self.show_current_page_le.setText("1")
        self.populate_widget_from_page(page_number=1)

    def go_to_last_page(self):
        self.show_current_page_le.setText(str(self.total_pages))
        self.populate_widget_from_page(page_number=self.total_pages)

    def get_current_selected_publish(self):
        get_selected_publish = self.publish_view_tw.selectedItems()
        if get_selected_publish:
            for item in get_selected_publish:
                get_publish_id = item.data(9, 1)
                get_asset_type = item.data(10, 1)
                self.context_handler.db_asset_version_id = get_publish_id
                self.context_handler.db_asset_type = get_asset_type
                self.selected_version.emit(self.context_handler)
                return get_publish_id

    def get_current_selected(self):
        selected = self.publish_view_tw.selectedItems()
        return selected


if __name__ == "__main__":
    import sys

    qss_style_file = "../style/stylesheets/dark_orange/dark_orange_style.qss"

    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.props',
                      'entity_name': 'knife',
                      'entity_id': 'The_Rock.assets.props.knife',
                      'asset_breakdown_id': 'The_Rock.assets.props.knife.breakdown',
                      'entity_type': 'asset',
                      # 'task_name': "modeling",
                      # 'task_type': "modeling",
                      # 'task_id': "The_Rock.assets.props.knife.modeling",
                      # 'db_asset_id': 'The_Rock.assets.props.knife.geometry.knife_main',
                      # 'db_asset_stream_id': 'The_Rock.assets.props.knife.knife_main',
                      # 'stack_id': 'The_Rock.assets.props.knife.knife_main.asset_stack',
                      }

    app = QtWidgets.QApplication(sys.argv)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    context = ContextHandler()
    context.load_session(session_data=context_sample)

    test_dialog = MainPublishesViewCore()
    test_dialog.context_receiver(context)

    test_dialog.populate_widget()

    test_dialog.show()
    sys.exit(app.exec_())
