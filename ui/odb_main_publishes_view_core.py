from PySide2 import QtWidgets, QtGui, QtCore
from database.db_statuses import DbStatuses
from envars.origin_envars import OriginEnvar
from database.entities.db_entities import DbPublish
from ui.odb_main_publishes_view_UI import MainPublishesViewUI
from ui.odb_publish_status_wdg import PublishStatusWidget
from o_database.entities.actions import Fetch, Query, Set, Add, Remove

img_path = "../icons/play_icon_vsmall.png"
thumbnail_path = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\dcc\icons\movie_pic.png"


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
    changes_to_database = []
    paginated_ids = []

    def __init__(self, parent=None):
        super(MainPublishesViewCore, self).__init__(parent)

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

    def get_limit_load(self):
        limit_val = self.load_limit_le.text()
        return int(limit_val)

    def set_total_pages_cnt(self):
        pass

    def deselect_all(self):
        self.publish_view_tw.clearSelection()

    def commit_changes(self):
        Set().publishes().multiple_ops(self.changes_to_database)
        self.populate_widget()
        self.changes_to_database.clear()
        self.check_changes()

    def set_date_from_string(self, date: str):
        if date:
            year, month, day = map(int, date.split("-"))
            qdate = QtCore.QDate(year, month, day)
            return qdate

    def set_date_as_string(self, date_widget):
        # date = date_widget.date()
        return date_widget.toString("yyyy-MM-dd")

    def publish_widget_construct(self, root_item, publish_data):
        publish_item = QtWidgets.QTreeWidgetItem(root_item)
        # publish_item.setFlags(publish_item.flags() | QtCore.Qt.ItemIsEditable)

        self.publish_thumbnail_small = PublishThumbnailViewer()
        self.publish_thumbnail_small.set_thumbnail(icon_path=thumbnail_path,
                                                   thumbnail_width=30,
                                                   thumbnail_height=15)

        self.publish_name_capture = publish_data["entry_name"]
        self.get_version = publish_data["version"]

        self.get_status = publish_data["status"]
        self.status_cb = PublishStatusWidget()
        self.status_cb.setCurrentText(self.get_status)

        self.pub_asset_type = publish_data["asset_type"]

        self.asset_task_type = publish_data["task_type"]

        self.published_by = publish_data["owner"]

        pub_date = publish_data["date"]
        pub_time = publish_data["time"]

        self.published_date = f"{pub_date} {pub_time}"

        self.get_description = "This is the description"  # TODO: implement DESCRIPTION in the task attributes

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
        from ui.style import buttons_styles as btns

        if len(self.changes_to_database) != 0:
            self.save_changes_btn.setStyleSheet("background-color: #db70b8; color: black")
        else:
            self.save_changes_btn.setStyleSheet(btns.hover_orange)

    def populate_widget(self):
        self.changes_to_database.clear()
        self.get_publishes()

        self.show_total_pages_le.setText(str(len(self.paginated_ids)))

        self.show_current_page_le.setText("1")
        current_page = self.show_current_page_le.text()

        if len(self.paginated_ids) != 0:
            current_ids = self.paginated_ids[int(current_page)-1]
            self.publish_view_tw.clear()
            published_doc_buff = self.try_buffer(current_ids)
            self.publish_view_tw.setUpdatesEnabled(False)
            self.publish_view_tw.addTopLevelItems(published_doc_buff)
            self.publish_view_tw.setUpdatesEnabled(True)
            self.go_to_next_page_btn.setEnabled(True)
            self.go_to_prev_page_btn.setEnabled(True)
            self.go_to_first_page_btn.setEnabled(True)
            self.go_to_last_page_btn.setEnabled(True)
            self.show_current_page_le.setEnabled(True)
            self.show_total_pages_le.setEnabled(True)
            self.load_limit_le.setEnabled(True)
        else:
            self.publish_view_tw.clear()
            self.go_to_next_page_btn.setEnabled(False)
            self.go_to_prev_page_btn.setEnabled(False)
            self.go_to_first_page_btn.setEnabled(False)
            self.go_to_last_page_btn.setEnabled(False)
            self.show_current_page_le.setEnabled(False)
            self.show_total_pages_le.setEnabled(False)
            self.load_limit_le.setEnabled(False)

    def populate_widget_from_page(self):
        self.changes_to_database.clear()
        self.show_total_pages_le.setText(str(len(self.paginated_ids)))
        current_page = self.show_current_page_le.text()

        if len(self.paginated_ids) != 0:
            current_ids = self.paginated_ids[int(current_page) - 1]
            self.publish_view_tw.clear()
            published_doc_buff = self.try_buffer(current_ids)
            self.publish_view_tw.setUpdatesEnabled(False)
            self.publish_view_tw.addTopLevelItems(published_doc_buff)
            self.publish_view_tw.setUpdatesEnabled(True)
            self.go_to_next_page_btn.setEnabled(True)
            self.go_to_prev_page_btn.setEnabled(True)
            self.go_to_first_page_btn.setEnabled(True)
            self.go_to_last_page_btn.setEnabled(True)
            self.show_current_page_le.setEnabled(True)
            self.show_total_pages_le.setEnabled(True)
            self.load_limit_le.setEnabled(True)

        else:
            self.publish_view_tw.clear()
            self.go_to_next_page_btn.setEnabled(False)
            self.go_to_prev_page_btn.setEnabled(False)
            self.go_to_first_page_btn.setEnabled(False)
            self.go_to_last_page_btn.setEnabled(False)
            self.show_current_page_le.setEnabled(False)
            self.show_total_pages_le.setEnabled(False)
            self.load_limit_le.setEnabled(False)

    def try_buffer(self, doc_id_list):
        buffer = []
        for doc_id in doc_id_list:
            # published_doc = Fetch().project_publish_entities().entity_document(doc_id["_id"])
            root_item = self.publish_view_tw.invisibleRootItem()
            row_item = self.publish_widget_construct(root_item=root_item, publish_data=doc_id)
            buffer.append(row_item)
        return buffer

    def get_publishes(self):
        get_limit_value = self.get_limit_load()
        context_resolve = OriginEnvar.resolve_to_full_context()
        fetch_ent = Fetch().project_publish_entities()

        publishes_docs = fetch_ent.entities_attr_value_starts_with(attr_field="origin_db_path",
                                                                  val_starts_with=context_resolve,
                                                                  ids_only=False)

        self.paginate_publishes(publishes_docs, get_limit_value)
        return self.paginated_ids

    def buffer_pub_items(self, doc_list):
        buffer = []
        for pub_doc in doc_list:
            root_item = self.publish_view_tw.invisibleRootItem()
            row_item = self.publish_widget_construct(root_item=root_item, publish_data=pub_doc)
            buffer.append(row_item)
        return buffer

    def paginate_pub_items(self, target_list, page_size):
        if len(target_list) != 0:
            self.paginated_ids = []
            for i in range(0, len(target_list), page_size):
                self.paginated_ids.append(target_list[i:i + page_size])
        else:
            self.paginated_ids = []

    def paginate_publishes(self, target_list, page_size):
        if len(target_list) != 0:
            self.paginated_ids = []
            for i in range(0, len(target_list), page_size):
                self.paginated_ids.append(target_list[i:i + page_size])
        else:
            self.paginated_ids = []

    def XXpaginate_publishes(self, target_list, page_size):
        if len(target_list) != 0:
            self.paginated_ids = []
            for i in range(0, len(target_list), page_size):
                end_index = min(i + page_size, len(target_list))
                self.paginated_ids.append((i, end_index))

            print("paginated idx:  ", self.paginated_ids)

        else:
            self.paginated_ids = []

    def sort_documentsX(self, doc_list, by_field, revr=False):
        sorted_list = sorted(doc_list, key=lambda x: x[by_field], reverse=revr)
        return sorted_list

    def go_to_next_page(self):
        current_page = self.show_current_page_le.text()
        next_page = int(current_page) + 1
        total_pages = len(self.paginated_ids)
        if next_page >= total_pages:
            self.show_current_page_le.setText(str(total_pages))
            self.populate_widget_from_page()
        else:
            self.show_current_page_le.setText(str(next_page))
            self.populate_widget_from_page()

    def go_to_previous_page(self):
        current_page = self.show_current_page_le.text()
        previous_page = int(current_page) - 1
        if previous_page != 0:
            self.show_current_page_le.setText(str(previous_page))
        else:
            self.show_current_page_le.setText("1")
        self.populate_widget_from_page()

    def go_to_first_page(self):
        self.show_current_page_le.setText("1")
        self.populate_widget_from_page()

    def go_to_last_page(self):
        total_pages = len(self.paginated_ids)
        self.show_current_page_le.setText(str(total_pages))
        self.populate_widget_from_page()

    def get_current_selected_publish(self):
        get_selected_publish = self.publish_view_tw.selectedItems()
        if get_selected_publish:
            for item in get_selected_publish:
                get_publish_id = item.data(9, 1)
                return get_publish_id

    def get_current_selected(self):
        get_selected_task = self.task_viewer_wdg.selectedItems()
        return get_selected_task

        # context Menu for the task viewer

    def create_tasks_actions(self):
        self.omit_task_action = QtWidgets.QAction("Omit and Hide...", self)
        self.show_hide_omitted_action = QtWidgets.QAction("Show/Hide Omitted...", self)


if __name__ == "__main__":
    import sys
    import random
    from envars.origin_envars import OriginEnvar
    from o_database.odb_statuses import DbVersionStatuses


    def randomize_pub_statuses(widget: MainPublishesViewCore):
        pubs_ids = widget.get_publishes()

        buffer_all_ids = []
        for item_lists in pubs_ids:
            for id_dict in item_lists:
                buffer_all_ids.append(id_dict["_id"])

        commands_list = []
        for buff in buffer_all_ids:
            commands_list.append({buff: {"status": random.choice(pub_statuses)}})

        Set().publishes().multiple_ops(commands_list)

        print("All DONE!")


    db_path = ["assets", "characters"]

    OriginEnvar.show_name = "New_Bubu"
    OriginEnvar.origin_path_hierarchy = db_path
    # print(OriginEnvar.origin_path_hierarchy)
    # OriginEnvar.entry_name = "hulk"
    # OriginEnvar.task_name = "texturing"

    # Set().publishes().multiple_ops(self.changes_to_database)

    pub_statuses = DbVersionStatuses().list_all()


    app = QtWidgets.QApplication(sys.argv)

    test_dialog = MainPublishesViewCore()

    randomize_pub_statuses(widget=test_dialog)

    test_dialog.populate_widget()

    test_dialog.show()
    sys.exit(app.exec_())



