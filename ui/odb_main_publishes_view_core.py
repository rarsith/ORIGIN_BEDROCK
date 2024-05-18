from PySide2 import QtWidgets, QtGui, QtCore
from database.db_statuses import DbStatuses
from envars.origin_envars import OriginEnvar
from database.entities.db_entities import DbPublish
from ui.odb_main_publishes_view_UI import MainPublishesViewUI
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
    def __init__(self, parent=None):
        super(MainPublishesViewCore, self).__init__(parent)

        self.create_connections()

    def create_connections(self):
        self.load_limit_le.returnPressed.connect(self.get_limit_load)
        self.load_limit_le.returnPressed.connect(self.populate_publishes)
        self.publish_view_tw.itemSelectionChanged.connect(self.get_current_selected_publish())
        self.refresh_btn.clicked.connect(self.populate_publishes)

    def get_limit_load(self):
        limit_val = self.load_limit_le.text()
        return int(limit_val)

    def deselect_all(self):
        self.publish_view_tw.clearSelection()

    def commit_changes(self):
        Set().tasks(entity_id=OriginEnvar().entity_id).multiple_ops(self.changes_to_database)
        self.populate_tasks()
        return self.changes_to_database.clear()

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

        self.published_date = f"{pub_date}/{pub_time}"

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
        self.publish_view_tw.setItemWidget(publish_item, 3, self.status_cb)
        publish_item.setText(4, self.pub_asset_type)
        publish_item.setText(5, self.asset_task_type)
        publish_item.setText(6, self.published_by)
        publish_item.setText(7, self.published_date)
        publish_item.setText(8, self.get_description)
        publish_item.setText(9, self.published_id)
        publish_item.setText(10, self.published_parent)
        publish_item.setText(11, self.published_has_notes)

        return publish_item

    def changed_status(self, data):
        sender = self.sender()
        current_publish_name = self.get_current_selected_publish()
        if current_publish_name:
            attr_path = "status"
            attr_value = sender.currentText()
            self.changes_to_database.append({attr_path: attr_value})
            return {attr_path: attr_value}

    def populate_publishes(self):
        self.changes_to_database.clear()
        get_entry_tasks_names = self.get_publishes()
        if get_entry_tasks_names is not None:
            self.publish_view_tw.clear()
            for published_doc in get_entry_tasks_names:
                root_item = self.publish_view_tw.invisibleRootItem()
                row_item = self.publish_widget_construct(root_item=root_item, publish_data=published_doc)
                self.publish_view_tw.addTopLevelItem(row_item)
            self.get_rows_count()

    def get_rows_count(self):
        rows_cnt = self.publish_view_tw.topLevelItemCount()
        for row in range(self.publish_view_tw.topLevelItemCount()):
            self.publish_view_tw.sizeHintForRow(20) * row
        return rows_cnt

    def sort_documens(self, doc_list, by_field, revr=False):
        sorted_list = sorted(doc_list, key=lambda x: x[by_field], reverse=revr)
        return sorted_list

    def get_publishes(self):
        get_limit_value = self.get_limit_load()
        context_resolve = OriginEnvar().resolve_to_full_context()
        fetch_ent = Fetch().project_publish_entities()

        if get_limit_value != 0:
            fetch_ent.limit = get_limit_value
        else:
            fetch_ent.limit = 1

        fetch_ent.sort_documents = -1
        fetch_ent.sort_attribute = "date"

        get_publishes_test = fetch_ent.entities_attr_value_starts_with(attr_field="origin_db_path",
                                                                       val_starts_with=context_resolve)

        return get_publishes_test

    def get_selected_task(self):
        names = []
        get_selected_objects = self.task_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return None
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.data(11, 1))
            return names[0]

    def get_current_selected_publish(self):
        get_selected_publish = self.publish_view_tw.selectedItems()
        if get_selected_publish:
            for item in get_selected_publish:
                get_task_name = item.data(9, 0)
                return get_task_name

    def get_current_selected(self):
        get_selected_task = self.task_viewer_wdg.selectedItems()
        return get_selected_task

        # context Menu for the task viewer

    def create_tasks_actions(self):
        self.omit_task_action = QtWidgets.QAction("Omit and Hide...", self)
        self.show_hide_omitted_action = QtWidgets.QAction("Show/Hide Omitted...", self)


if __name__ == "__main__":
    import sys
    from envars.origin_envars import OriginEnvar

    db_path = ["assets", "characters"]

    OriginEnvar.show_name = "New_Era"
    OriginEnvar().origin_path_hierarchy = db_path
    # print(OriginEnvar().origin_path_hierarchy)
    OriginEnvar.entry_name = "hulk"
    OriginEnvar.task_name = "texturing"

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = MainPublishesViewCore()
    test_dialog.populate_publishes()
    # test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())
