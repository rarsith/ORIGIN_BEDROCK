from PySide2 import QtWidgets, QtGui
from envars.origin_envars import OriginEnvar
from ui.odb_task_viewer_UI import TaskViewerUI
from database.entities.db_entities import DbTasks
from o_database.entities.actions import Query
from ui.odb_create_task_ui import CreateTaskUI


class TaskViewerCore(TaskViewerUI):
    def __init__(self, parent=None):
        super(TaskViewerCore, self).__init__(parent)

        self.create_tasks_actions()
        self.create_connections()
        self.context_menu()

    def create_connections(self):
        self.add_btn.clicked.connect(self.create_task_menu)
        self.task_viewer_wdg.itemSelectionChanged.connect(self.get_task_list_current_selected)

    def set_task_is_active(self):
        is_active = self.task_is_active_properties_ckb.isChecked()
        try:
            DbTasks().current_is_active = is_active
            self.populate_task_details()
        except:
            pass
        print('{} status changed to {}'.format(self.tasks_view_lwd.get_selected_task(), is_active))

    def populate_tasks(self):
        get_entry_tasks_names = self.get_tasks()
        self.task_viewer_wdg.clear()
        self.add_tasks_to_list(get_entry_tasks_names)

    def add_tasks_to_list(self, task_list):
        if task_list:
            if len(task_list) != 0:
                for task_name, task_type in task_list.items():
                    root_item = self.task_viewer_wdg.invisibleRootItem()
                    item = QtWidgets.QTreeWidgetItem(root_item)
                    item.setText(0, (str(task_name)).capitalize())
                    # item.setText(1, (str(task_type)).capitalize())

    def get_tasks(self):
        spare_it = {}
        tasks_info = {}
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
                        for k, v in tasks_list.items():
                            tasks_info[k] = v["type"]
                        return tasks_info
                except:
                    pass
        else:
            return spare_it

    def get_selected_task(self):
        names = []
        get_selected_objects = self.task_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return None
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text(0))
            return names[0]

    def get_task_list_current_selected(self):
        get_selected_task = self.task_viewer_wdg.selectedItems()
        for i in get_selected_task:
            OriginEnvar.task_name = i.text(0)
            return i.text(0)

    #context Menu for the task viewer
    def create_tasks_actions(self):
        self.omit_task_action = QtWidgets.QAction("Omit and Hide...", self)
        self.show_hide_omitted_action = QtWidgets.QAction("Show/Hide Omitted...", self)
        self.add_user_to_task_action = QtWidgets.QAction("User Assign...", self)

    def context_menu(self):
        self.task_viewer_wdg.customContextMenuRequested.connect(self.tasks_con_menu)

    def tasks_con_menu(self, point):
        selected = self.get_selected_task()
        tasks_context_menu = QtWidgets.QMenu()

        if selected:
            tasks_context_menu.addAction(self.omit_task_action)
            tasks_context_menu.addAction(self.show_hide_omitted_action)
            tasks_context_menu.addAction(self.split_task_action)
            tasks_context_menu.addAction(self.add_user_to_task_action)
            tasks_context_menu.exec_(self.mapToGlobal(point))

    def create_task_menu(self):
        self.ui = CreateTaskUI()
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.populate_tasks)
        self.ui.create_and_close_btn.clicked.connect(self.populate_tasks)

if __name__ == '__main__':
    import sys

    path = ["assets", "characters"]

    OriginEnvar.show_name = "New_World"
    OriginEnvar.origin_path_hierarchy = path
    OriginEnvar.entry_name = "hulk"
    # Envars.task_name = "cfx_set"


    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = TaskViewerCore()
    test_dialog.populate_tasks()

    test_dialog.show()
    sys.exit(app.exec_())