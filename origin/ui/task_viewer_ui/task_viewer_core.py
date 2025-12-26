from PySide2 import QtWidgets, QtGui, QtCore
from origin.envars.origin_envars import ContextHandler
from origin.ui.task_viewer_ui.task_viewer_UI import TaskViewerUI
from origin.ui.status_widgets.task_status_wdg import TaskStatusWidget
from origin.ui.status_widgets.task_priority_wdg import TaskPriorityWidget
from origin.database.entities.operators import (Task)
from origin.database.mongo import CollectionOperators

from origin.ui.creators_ui.create_task_ui import CreateTaskUI


class TaskViewerCore(TaskViewerUI):
    changes_to_database = []
    current_context = QtCore.Signal(object)

    def __init__(self, context: ContextHandler = None, parent=None):
        super(TaskViewerCore, self).__init__(parent)

        self.entity_received = None
        self.project_received = None

        self.context_handler = context
        if self.context_handler is not None:
            self.resolve_entity()
            self.resolve_project()

        self.create_tasks_actions()
        self.create_connections()

    def create_connections(self):
        self.add_btn.clicked.connect(self.create_task_menu)
        self.task_viewer_wdg.itemSelectionChanged.connect(self.get_task_list_current_selected)
        self.task_viewer_wdg.itemClicked.connect(self.get_task_list_current_selected)
        self.save_changes_btn.clicked.connect(self.commit_changes)
        self.refresh_btn.clicked.connect(self.populate_widget)

    def context_receiver(self, context: ContextHandler):
        self.context_handler = context
        self.resolve_project()
        self.resolve_entity()

    def resolve_entity(self):
        if self.context_handler.entity_type != "group":
            self.entity_received = self.context_handler.database_handler().get_asset_document()
            return self.entity_received
        else:
            self.entity_received = None

    def resolve_project(self):
        self.project_received = self.context_handler.database_handler().get_project_document()
        return self.project_received

    def commit_changes(self):
        db_ops = CollectionOperators(db_collection=self.project_received.id)
        db_ops.multiple_ops(self.changes_to_database)
        self.populate_widget()
        self.check_changes()
        return self.changes_to_database.clear()

    def set_date_from_string(self, date: str):
        if date:
            year, month, day = map(int, date.split("-"))
            qdate = QtCore.QDate(year, month, day)
            return qdate

    def set_date_as_string(self, date_widget):
        # date = date_widget.date()
        return date_widget.toString("yyyy-MM-dd")

    def task_widget_construct(self, root_item, task_name, task_data):
        task_item = QtWidgets.QTreeWidgetItem(root_item)
        task_item.setFlags(task_item.flags() | QtCore.Qt.ItemIsEditable)

        self.task_name_capture = QtWidgets.QLineEdit()
        self.task_name_capture.setText(task_data.name)
        self.task_name_capture.setReadOnly(True)

        self.task_type_capture = QtWidgets.QLineEdit()
        task_type = f"task ( {task_data.task_type} )"
        task_type_nice = task_type.capitalize()

        self.get_status = task_data.status
        self.status_cb = TaskStatusWidget()

        self.priority = task_data.priority
        self.priorities_cb = TaskPriorityWidget()

        self.assigned_artist = task_data.artist
        self.artist_cb = QtWidgets.QComboBox()
        self.artist_cb.wheelEvent = lambda event: None
        self.artist_cb.addItems(["arsithra", "unassigned"])  # TODO: Implement User_Database

        self.get_start_date = task_data.start_date
        self.start_date_dt = QtWidgets.QDateEdit(calendarPopup=True)
        get_start_date = self.set_date_from_string(self.get_start_date)

        self.get_end_date = task_data.end_date
        self.end_date_dt = QtWidgets.QDateEdit(calendarPopup=True)
        get_end_date = self.set_date_from_string(self.get_end_date)

        self.get_used_days = "15"  # TODO: Compile used days from user time tracking
        self.get_parity = "-2"  # TODO: Compile parity from used days vs bid days
        self.get_description = "This is the description"  # TODO: implement DESCRIPTION in the task attributes

        #Connections
        self.status_cb.currentIndexChanged.connect(self.changed_status)
        self.priorities_cb.currentIndexChanged.connect(self.changed_prio)
        self.artist_cb.currentIndexChanged.connect(self.changed_artist)
        self.start_date_dt.dateChanged.connect(self.changed_start_date)
        self.end_date_dt.dateChanged.connect(self.changed_end_date)

        try:
            self.status_cb.setCurrentText(self.get_status)
            self.priorities_cb.setCurrentText(self.priority)
            self.artist_cb.setCurrentText(self.assigned_artist)
            self.start_date_dt.setDate(get_start_date)
            self.end_date_dt.setDate(get_end_date)

        except ValueError as e:
            raise e

        task_item.setText(0, task_name)
        task_item.setText(1, task_type_nice)
        self.task_viewer_wdg.setItemWidget(task_item, 2, self.status_cb)
        task_item.setText(3, task_data.bid_days)
        task_item.setText(4, self.get_used_days)
        task_item.setText(5, self.get_parity)
        self.task_viewer_wdg.setItemWidget(task_item, 6, self.start_date_dt)
        self.task_viewer_wdg.setItemWidget(task_item, 7, self.end_date_dt)
        self.task_viewer_wdg.setItemWidget(task_item, 8, self.priorities_cb)
        self.task_viewer_wdg.setItemWidget(task_item, 9, self.artist_cb)
        task_item.setText(10, self.get_description)
        task_item.setData(11, 1, task_name)
        task_item.setData(11, 0, task_data)


        return task_item

    def updates_tasks_data(self, target_attr):
        sender = self.sender()
        current_task_data = self.get_task_list_current_selected()
        if current_task_data:
            task_id = current_task_data.id
            attr_value = sender.currentText()
            self.changes_to_database.append({task_id: {target_attr: attr_value}})
            self.check_changes()

    def changed_status(self, data):
        self.updates_tasks_data(target_attr="status")

    def changed_prio(self, data):
        self.updates_tasks_data(target_attr="priority")

    def changed_artist(self, data):
        self.updates_tasks_data(target_attr="artist")

    def changed_start_date(self, data):
        sender = self.sender()
        current_task_data = self.get_task_list_current_selected()
        if current_task_data:
            task_id = current_task_data.id
            date_to_string = self.set_date_as_string(sender.date())
            self.changes_to_database.append({task_id: {"start_date": date_to_string}})
            self.check_changes()

    def changed_end_date(self, data):
        sender = self.sender()
        current_task_data = self.get_task_list_current_selected()
        if current_task_data:
            task_id = current_task_data.id
            date_to_string = self.set_date_as_string(sender.date())
            self.changes_to_database.append({task_id: {"end_date": date_to_string}})
            self.check_changes()

    def check_changes(self):
        if len(self.changes_to_database) != 0:
            self.save_changes_btn.setStyleSheet("background-color: #db70b8; color: black")
        else:
            self.save_changes_btn.setStyleSheet("QPushButton { border: none; background: transparent; }")

    def populate_widget(self):
        self.changes_to_database.clear()
        self.task_viewer_wdg.clearSelection()
        self.task_viewer_wdg.clear()

        get_entry_tasks = self.get_tasks()

        for task in get_entry_tasks:
            root_item = self.task_viewer_wdg.invisibleRootItem()
            row_item = self.task_widget_construct(root_item=root_item, task_name=task.name, task_data=task)
            self.task_viewer_wdg.addTopLevelItem(row_item)

    def get_tasks(self):
        if self.entity_received is not None and self.entity_received.type != "group":
            item_tasks = self.entity_received.operations().get_children()

            if item_tasks is None:
                return {}
            else:
                try:
                    if len(item_tasks) == 0:
                        return {}
                    elif len(item_tasks) >= 1:
                        return [Task(**item_task) for item_task in item_tasks]
                except ValueError as e:
                    raise e
        else:
            return {}

    def get_task_list_current_selected(self):
        get_selected_task = self.task_viewer_wdg.selectedItems()
        if len(get_selected_task) != 0:
            for item in get_selected_task:
                get_task_data = item.data(11, 0)

                self.context_handler.task_name = get_task_data.name
                self.context_handler.task_type = get_task_data.task_type
                self.context_handler.task_id = get_task_data.id
                self.current_context.emit(self.context_handler)
                # print("TASKS: ", self.context_handler.snapshot_session())

                return get_task_data
        else:
            self.context_handler.reset_to_entity()
            self.current_context.emit(self.context_handler)

    def get_current_selected(self):
        get_selected_task = self.task_viewer_wdg.selectedItems()
        return get_selected_task

    #context Menu for the task viewer
    def create_tasks_actions(self):
        self.omit_task_action = QtWidgets.QAction("Omit and Hide...", self)
        self.show_hide_omitted_action = QtWidgets.QAction("Show/Hide Omitted...", self)

    def resolve_parent_id(self):
        task_parent_type = self.entity_received.type
        if task_parent_type:
            if task_parent_type != "group":
                doc_id = self.entity_received.id
                return doc_id
            else:
                doc_id = None
                return doc_id

    def create_task_menu(self):
        task_parent = self.resolve_parent_id()
        print(task_parent)
        if task_parent is not None:
            self.ui = CreateTaskUI(context=self.context_handler, task_parent=task_parent,)
            self.ui.show()
            self.ui.create_btn.clicked.connect(self.populate_widget)
            self.ui.create_and_close_btn.clicked.connect(self.populate_widget)
        else:
            print("Please select an ASSET!")


if __name__ == '__main__':
    import sys

    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.chr.tafer',
                      'entity_name': 'tafer',
                      'db_asset_id': 'The_Rock.assets.chr.tafer.modeling.main',
                      'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer',
                      'entity_type': 'asset',
                      'entity_id': 'The_Rock.assets.chr.tafer',
                      'task_name': "modeling",
                      'task_type': "modeling"}

    context_obj = ContextHandler()
    context_obj.load_session(session_data=context_sample)

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = TaskViewerCore(context=context_obj)
    test_dialog.populate_widget()
    test_dialog.show()
    sys.exit(app.exec_())
