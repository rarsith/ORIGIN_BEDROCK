from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import Slot
from envars.origin_envars import OriginEnvar
from o_database.odb_statuses import DbTaskStatuses
from o_database.odb_priorities import DbPriorities

from ui.odb02_task_viewer_UI import TaskViewerUI
from ui.odb_task_status_wdg import TaskStatusWidget
from database.entities.db_entities import DbTasks
from o_database.entities.actions import Query, Set
from ui.odb_create_task_ui import CreateTaskUI


class TaskViewerCore(TaskViewerUI):
    changes_to_database = []

    def __init__(self, parent=None):
        super(TaskViewerCore, self).__init__(parent)

        self.create_tasks_actions()
        self.create_connections()

    def create_connections(self):
        self.add_btn.clicked.connect(self.create_task_menu)
        self.task_viewer_wdg.itemSelectionChanged.connect(self.get_task_list_current_selected)
        self.save_changes_btn.clicked.connect(self.commit_changes)
        self.refresh_btn.clicked.connect(self.populate_tasks)

    def commit_changes(self):
        Set().tasks().multiple(self.changes_to_database)
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

    def task_widget_construct(self, root_item, task_name, task_data):
        task_item = QtWidgets.QTreeWidgetItem(root_item)
        task_item.setFlags(task_item.flags() | QtCore.Qt.ItemIsEditable)

        self.task_name_capture = QtWidgets.QLineEdit()
        self.task_name_capture.setText(task_name)
        self.task_name_capture.setReadOnly(True)

        self.task_type_capture = QtWidgets.QLineEdit()
        self.task_type_capture.setText((task_data["type"]).capitalize())
        self.task_type_capture.setReadOnly(True)

        self.get_status = task_data["status"]
        self.status_cb = TaskStatusWidget()
        # self.status_cb.addItems(DbTaskStatuses().list_all())


        self.priority = task_data["priority"]
        self.priorities_cb = QtWidgets.QComboBox()
        self.priorities_cb.addItems(DbPriorities().list_all())


        self.assigned_artist = task_data["artist"]
        self.artist_cb = QtWidgets.QComboBox()
        self.artist_cb.addItems(["arsithra", "unassigned"])  # TODO: Implement User_Database


        self.get_start_date = task_data["start_date"]
        self.start_date_dt = QtWidgets.QDateEdit(calendarPopup=True)
        get_start_date = self.set_date_from_string(self.get_start_date)



        self.get_end_date = task_data["end_date"]
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

        self.task_viewer_wdg.setItemWidget(task_item, 0, self.task_name_capture)
        self.task_viewer_wdg.setItemWidget(task_item, 1, self.task_type_capture)
        self.task_viewer_wdg.setItemWidget(task_item, 2, self.status_cb)
        task_item.setText(3, task_data["bid_days"])
        task_item.setText(4, self.get_used_days)
        task_item.setText(5, self.get_parity)
        self.task_viewer_wdg.setItemWidget(task_item, 6, self.start_date_dt)
        self.task_viewer_wdg.setItemWidget(task_item, 7, self.end_date_dt)
        self.task_viewer_wdg.setItemWidget(task_item, 8, self.priorities_cb)
        self.task_viewer_wdg.setItemWidget(task_item, 9, self.artist_cb)
        task_item.setText(10, self.get_description)
        task_item.setData(11, 1, task_name)

        return task_item

    def changed_status(self, data):
        sender = self.sender()
        current_task_name = self.get_task_list_current_selected()
        if current_task_name:
            attr_path = ".".join(["tasks", current_task_name, "status"])
            attr_value = sender.currentText()
            self.changes_to_database.append({attr_path:attr_value})
            return {attr_path:attr_value}

    def changed_prio(self, data):
        sender = self.sender()
        current_task_name = self.get_task_list_current_selected()
        if current_task_name:
            attr_path = ".".join(["tasks", current_task_name, "priority"])
            attr_value = sender.currentText()
            self.changes_to_database.append({attr_path: attr_value})
            return {attr_path: attr_value}

    def changed_artist(self, data):
        sender = self.sender()
        current_task_name = self.get_task_list_current_selected()
        if current_task_name:
            attr_path = ".".join(["tasks", current_task_name, "artist"])
            attr_value = sender.currentText()
            self.changes_to_database.append({attr_path: attr_value})
            return {attr_path: attr_value}

    def changed_start_date(self, data):
        sender = self.sender()
        current_task_name = self.get_task_list_current_selected()
        if current_task_name:
            date_to_string = self.set_date_as_string(sender.date())
            attr_path = ".".join(["tasks", current_task_name, "start_date"])
            self.changes_to_database.append({attr_path: date_to_string})
            return {attr_path: date_to_string}

    def changed_end_date(self, data):
        sender = self.sender()
        current_task_name = self.get_task_list_current_selected()
        if current_task_name:
            date_to_string = self.set_date_as_string(sender.date())
            attr_path = ".".join(["tasks", current_task_name, "end_date"])
            self.changes_to_database.append({attr_path: date_to_string})
            return {attr_path: date_to_string}

    def populate_tasks(self):
        get_entry_tasks_names = self.get_tasks()
        self.task_viewer_wdg.clear()
        for task_name, task_schema in get_entry_tasks_names.items():
            root_item = self.task_viewer_wdg.invisibleRootItem()
            row_item = self.task_widget_construct(root_item=root_item, task_name=task_name, task_data=task_schema)
            self.task_viewer_wdg.addTopLevelItem(row_item)

    def get_tasks(self):
        spare_it = {}
        curr_asset_type = Query().curr_asset().entity_type
        tasks_list = Query().curr_asset().tasks

        if curr_asset_type != "group":
            if tasks_list is None:
                return spare_it
            else:
                try:
                    if len(tasks_list) == 0:
                        return spare_it
                    elif len(tasks_list) >= 1:
                        return tasks_list
                except ValueError as e:
                    raise e
        else:
            return spare_it

    def get_selected_task(self):
        names = []
        get_selected_objects = self.task_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return None
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.data(11, 1))
            return names[0]

    def get_task_list_current_selected(self):
        get_selected_task = self.task_viewer_wdg.selectedItems()
        if get_selected_task:
            for item in get_selected_task:
                get_task_name_data = item.data(11, 1)
                OriginEnvar.task_name = get_task_name_data
                return get_task_name_data

    #context Menu for the task viewer
    def create_tasks_actions(self):
        self.omit_task_action = QtWidgets.QAction("Omit and Hide...", self)
        self.show_hide_omitted_action = QtWidgets.QAction("Show/Hide Omitted...", self)

    def create_task_menu(self):
        self.ui = CreateTaskUI()
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.populate_tasks)
        self.ui.create_and_close_btn.clicked.connect(self.populate_tasks)

if __name__ == '__main__':
    import sys

    path = ["assets", "characters"]

    OriginEnvar.show_name = "New_World"
    OriginEnvar().origin_path_hierarchy = path
    OriginEnvar.entry_name = "hulk"
    # Envars.task_name = "cfx_set"


    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    qss_style_file = "stylesheets/Task_Viewer.qss"

    with open(qss_style_file, "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    test_dialog = TaskViewerCore()



    test_dialog.populate_tasks()

    test_dialog.show()
    sys.exit(app.exec_())