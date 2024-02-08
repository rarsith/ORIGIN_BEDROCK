import sys
from PySide2 import QtWidgets, QtCore, QtGui
from envars.envars import Envars

from ui.task_imports_from_UI import TasksImportFromUI
from database.entities.db_entities import DbTasks, DbPubSlot


class TasksImportFromCore(TasksImportFromUI):
    def __init__(self, parent=None):
        super(TasksImportFromCore, self).__init__(parent)

        self.create_connections()

    def create_connections(self):
        self.save_btn.clicked.connect(self.save_to_database)
        self.rem_sel_item_btn.clicked.connect(self.remove_import_task_slot)
        self.refresh_btn.clicked.connect(self.populate_main_widget)
        self.move_to_right_btn.clicked.connect(self.move_selection_to_right)

    def populate_main_widget(self):
        self.populate_existing_tasks()
        self.populate_task_import_schema()
        self.remove_already_assigned()
        self.remove_self_task()
        self.imports_from_wdg.expandAll()

    def change_label_existing_tasks(self):
        current_entry_name = Envars().entry_name
        my_font = QtGui.QFont()
        my_font.setBold(True)

        self.tasks_existing_lb.clear()
        self.tasks_existing_lb.setText("{0}\nExisting Tasks".format(current_entry_name + " asset").upper())
        self.tasks_existing_lb.setFont(my_font)
        self.tasks_existing_lb.setStyleSheet("color: red")

    def change_label_imports_from(self):
        curr_task_name = Envars().task_name
        my_font = QtGui.QFont()
        my_font.setBold(True)

        self.tasks_imports_from_properties_lb.clear()
        self.tasks_imports_from_properties_lb.setText("{0}\nImports From".format(curr_task_name.upper()))
        self.tasks_imports_from_properties_lb.setFont(my_font)
        self.tasks_imports_from_properties_lb.setStyleSheet("color: red")

    def change_label_imports_from_assignments(self):
        current_entry_name = Envars().entry_name
        my_font = QtGui.QFont()
        my_font.setBold(True)

        self.tasks_imports_from_assignments_lb.clear()
        self.tasks_imports_from_assignments_lb.setText("{0}\nAssigned Generators".format(current_entry_name.upper()))
        self.tasks_imports_from_assignments_lb.setFont(my_font)
        self.tasks_imports_from_assignments_lb.setStyleSheet("color: red")

    def get_splits(self, data: list, idx: int, delimiter: str =".") -> list:
        output_list = []
        for element in data:
            if delimiter not in element:
                if element not in output_list:
                    output_list.append(element)
            else:
                if element.split(delimiter)[idx] not in output_list:
                    output_list.append(element.split(delimiter)[idx])
        return output_list

    def populate_task_import_schema(self):
        get_schema = self.get_saved_import_schema()
        get_tasks_only = self.get_splits(get_schema, 0, ".")

        get_active_tasks = []
        self.imports_from_wdg.clear()

        for task in get_tasks_only:
            is_active = DbTasks().is_active(task=task)
            if is_active:
                get_active_tasks.append(task)
        self.add_items_to_list(get_active_tasks)

    def add_items_to_list(self, items):
        get_schema = self.get_saved_import_schema()
        get_pubs_only = self.get_splits(get_schema, 2, ".")
        for active_task in items:
            imp_from_pub_slots_schema = DbPubSlot().get_pub_slots(task_name=active_task)
            item = QtWidgets.QTreeWidgetItem([active_task])
            self.imports_from_wdg.addTopLevelItem(item)

            try:
                for pub_slot, pub_slot_content in imp_from_pub_slots_schema.items():
                    pub_slot_item = QtWidgets.QTreeWidgetItem([pub_slot])
                    item.addChild(pub_slot_item)

                    if pub_slot_item.text(0) in get_pubs_only:
                        pub_slot_item.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        pub_slot_item.setCheckState(0, QtCore.Qt.Unchecked)

            except:
                pass

    def add_tasks_to_list(self, tasks_list):
        for active_task in tasks_list:
            imp_from_pub_slots_schema = DbPubSlot().get_pub_slots(task_name=active_task)
            item = QtWidgets.QTreeWidgetItem([active_task])
            self.all_pub_slots_wdg.addTopLevelItem(item)

            slot_used_by = self.get_pub_used_by(imp_from_pub_slots_schema)

            try:
                for pub_slot, pub_slot_content in imp_from_pub_slots_schema.items():
                    pub_slot_item = QtWidgets.QTreeWidgetItem([pub_slot])
                    item.addChild(pub_slot_item)

                    if pub_slot_item.text(0) in slot_used_by:
                        pub_slot_item.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        pub_slot_item.setCheckState(0, QtCore.Qt.Unchecked)

            except:
                pass

    def get_saved_import_schema(self):
        existing_imports_from = DbTasks().imports_from
        if existing_imports_from is None:
            return []
        else:
            return existing_imports_from

    def get_pub_used_by(self, extract):
        rel_task = DbPubSlot().get_used_by_task(data=extract)
        return rel_task

    def get_wdg_checked_items(self):
        checked = dict()
        root = self.imports_from_wdg.invisibleRootItem()
        signal_count = root.childCount()

        for idx in range(signal_count):
            signal = root.child(idx)
            checked_sweeps = list()
            num_children = signal.childCount()

            for child_idx in range(num_children):
                child = signal.child(child_idx)

                if child.checkState(0) == QtCore.Qt.Checked:
                    checked_sweeps.append(child.text(0))
            checked[signal.text(0)] = checked_sweeps
        return checked

    def get_wdg_unchecked_items(self):
        unchecked = dict()
        root = self.imports_from_wdg.invisibleRootItem()
        signal_count = root.childCount()

        for idx in range(signal_count):
            signal = root.child(idx)
            checked_sweeps = list()
            num_children = signal.childCount()

            for child_idx in range(num_children):
                child = signal.child(child_idx)

                if child.checkState(0) == QtCore.Qt.Unchecked:
                    checked_sweeps.append(child.text(0))
            unchecked[signal.text(0)] = checked_sweeps
        return unchecked

    def write_wdg_checked_items(self):
        save_new_import_schema = []
        checked_items = self.get_wdg_checked_items()

        for task_name, task_pub_slots in checked_items.items():
            for pub_slot in task_pub_slots:
                imports_from_data_format = ".".join([task_name, "pub_slots", pub_slot])
                save_new_import_schema.append(imports_from_data_format)

        return save_new_import_schema


    def remove_import_task_slot(self):
        listItems = self.imports_from_wdg.currentItem()
        selected_index = self.imports_from_wdg.indexFromItem(listItems)
        remove_it = selected_index.row()
        self.imports_from_wdg.takeTopLevelItem(remove_it)

    def save_to_database(self):
        extract_import_schema = self.write_wdg_checked_items()

        DbTasks().rem_import_slots()
        DbTasks().imports_from = extract_import_schema
        self.populate_main_widget()

    def populate_existing_tasks(self):
        self.existing_tasks_lwd.clear()
        all_tasks = self.get_all_tasks()
        if all_tasks is None:
            return []
        for task in all_tasks:
            QtWidgets.QListWidgetItem(task, self.existing_tasks_lwd)

    def get_all_tasks(self):
        tasks = DbTasks().get_tasks()
        if tasks is not None:
            return tasks
        return ["-- no tasks --"]

    def remove_self_task(self):
        current_task = Envars().task_name
        entries = self.existing_tasks_lwd.findItems(current_task, QtCore.Qt.MatchFixedString)
        for entry in entries:
            indexes = self.existing_tasks_lwd.indexFromItem(entry)
            self.existing_tasks_lwd.takeItem(indexes.row())

    def get_imports_from(self):
        list_all = []
        nnn = self.imports_from_wdg.topLevelItemCount()
        ccc = self.imports_from_wdg.invisibleRootItem()
        for each_item in (range(nnn)):
            sel = ccc.child(each_item)
            list_all.append(sel.text(0))
        return list_all

    def remove_already_assigned(self):
        existing_assignments = self.get_imports_from()
        for task_name in existing_assignments:
            entries = self.existing_tasks_lwd.findItems(task_name, QtCore.Qt.MatchFixedString)
            for entry in entries:
                indexes = self.existing_tasks_lwd.indexFromItem(entry)
                self.existing_tasks_lwd.takeItem(indexes.row())

    def move_selection_to_right(self):
        text = self.existing_tasks_lwd.selectedItems()
        for item in text:
            self.add_items_to_list([item.text()])
            self.existing_tasks_lwd.takeItem(self.existing_tasks_lwd.row(item))
            self.imports_from_wdg.expandAll()


if __name__ == "__main__":
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "props"
    Envars.entry_name = "red_knife"
    Envars.task_name = "modeling"

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = TasksImportFromCore()

    test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())