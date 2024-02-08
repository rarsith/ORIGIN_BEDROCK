from PySide2 import QtWidgets, QtGui, QtCore
from envars.envars import Envars
from ui.task_viewer_UI import TaskViewerUI
from database.entities.db_entities import DbTasks

class TaskViewerCore(TaskViewerUI):
    def __init__(self, parent=None):
        super(TaskViewerCore, self).__init__(parent)

        self.create_tasks_actions()
        self.create_connections()
        # self.populate_tasks()
        self.context_menu()

    def create_connections(self):
        self.add_btn.clicked.connect(self.add_to_task_list)
        self.task_viewer_wdg.itemSelectionChanged.connect(self.get_task_list_current_selected)

    def set_task_is_active(self):
        # if child.checkState(0) == QtCore.Qt.Checked
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
        for task in task_list:
            item = QtWidgets.QListWidgetItem(task)
            self.task_viewer_wdg.addItem(item)

            is_active = DbTasks().is_active(task=task)
            if is_active:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)


    def get_tasks(self):
        spare_it = []
        tasks_list = DbTasks().get_tasks()

        if tasks_list == None:
            return spare_it
        else:
            try:
                if len(tasks_list) == 0:
                    return spare_it
                elif len(tasks_list) >= 1:
                    return sorted(tasks_list)
            except:
                pass

    def get_selected_task(self):
        names = []
        get_selected_objects = self.task_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return None
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text())
            return names[0]

    def get_task_list_current_selected(self):
        get_selected_task = self.task_viewer_wdg.selectedItems()
        for i in get_selected_task:
            Envars.task_name = i.text()
            return i.text()

    def insert_task_row(self, name):
        self.task_viewer_wdg.insertItem(0, name)
        DbTasks().create(name=self.add_task_le.text())

    def add_to_task_list(self):
        if self.add_task_le.text():
            self.insert_task_row(self.add_task_le.text())
            self.add_task_le.clear()
            self.populate_tasks()

        else:
            return

    #context Menu for the task viewer
    def create_tasks_actions(self):
        self.omit_task_action = QtWidgets.QAction("Omit and Hide...", self)
        self.show_hide_omitted_action = QtWidgets.QAction("Show/Hide Omitted...", self)
        self.split_task_action = QtWidgets.QAction("Split...", self)
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


if __name__ == '__main__':
    import sys

    Envars.show_name = "Green"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "monster"
    # Envars.task_name = "cfx_set"


    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = TaskViewerCore()
    test_dialog.populate_tasks()

    test_dialog.show()
    sys.exit(app.exec_())