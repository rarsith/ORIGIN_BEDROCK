import sys
from PySide2 import QtWidgets, QtCore

from origin_data_base import xcg_db_actions as xac
from RND import xcg_task_imports_from_wdg


class SetTaskImportsFromUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(SetTaskImportsFromUI, self).__init__(parent)

        self.setWindowTitle("Task Imports From")
        self.setMinimumWidth(750)
        self.setMaximumWidth(750)

        self.setMinimumHeight(900)
        self.setMaximumHeight(900)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.populate_existing_assignments()

    def create_widgets(self):
        self.show_name_cb = QtWidgets.QComboBox()
        self.show_name_cb.addItems(self.get_shows())

        self.show_branch_cb = QtWidgets.QComboBox()
        self.show_branch_cb.addItems(self.get_show_branches())

        self.category_cb = QtWidgets.QComboBox()
        self.category_cb.addItems(self.get_categories())

        self.entry_name_cb = QtWidgets.QComboBox()
        self.entry_name_cb.addItems(self.get_entries())


        self.task_name_cb = QtWidgets.QComboBox()
        self.task_name_cb.addItems(self.get_all_tasks())

        self.imports_from_lwd = xcg_task_imports_from_wdg.TasksImportFromUI()

        self.existing_tasks_lb = QtWidgets.QLabel("Existing Tasks")
        self.imports_from_lb = QtWidgets.QLabel("Imports From")

        self.create_and_close_btn = QtWidgets.QPushButton("Create and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name ", self.show_name_cb)
        form_layout.addRow("Show Branch", self.show_branch_cb)
        form_layout.addRow("Category", self.category_cb)
        form_layout.addRow("Entry Name", self.entry_name_cb)
        form_layout.addRow("Task Name", self.task_name_cb)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        form_layout.setLabelAlignment(QtCore.Qt.AlignLeft)

        imports_from_label_layout = QtWidgets.QVBoxLayout()
        imports_from_label_layout.addWidget(self.imports_from_lwd)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(imports_from_label_layout)
        main_layout.addSpacing(30)

    def create_connections(self):
        self.show_name_cb.currentIndexChanged.connect(self.comboBox_shows)
        self.show_name_cb.currentIndexChanged.connect(self.populate_show_branches)
        self.show_name_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_name_cb.currentIndexChanged.connect(self.populate_entries)
        self.show_name_cb.currentIndexChanged.connect(self.populate_existing_assignments)

        self.show_branch_cb.currentIndexChanged.connect(self.comboBox_show_branches)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_existing_tasks_cb)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_entries)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_existing_assignments)

        self.category_cb.currentIndexChanged.connect(self.comboBox_categories)
        self.category_cb.currentIndexChanged.connect(self.populate_existing_tasks_cb)
        self.category_cb.currentIndexChanged.connect(self.populate_entries)
        self.category_cb.currentIndexChanged.connect(self.populate_existing_assignments)

        self.entry_name_cb.currentIndexChanged.connect(self.comboBox_entries)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_existing_tasks_cb)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_existing_assignments)

        self.task_name_cb.currentIndexChanged.connect(self.populate_existing_assignments)

        self.cancel_btn.clicked.connect(self.close)

    def comboBox_shows(self):
        text = self.show_name_cb.currentText()
        return text

    def comboBox_show_branches(self):
        show_branch_text = self.show_branch_cb.currentText()
        return show_branch_text

    def comboBox_categories(self):
        category_text = self.category_cb.currentText()
        return category_text

    def comboBox_entries(self):
        entry_text = self.entry_name_cb.currentText()
        return entry_text

    def combobox_tasks(self):
        task_text = self.task_name_cb.currentText()
        return task_text

    def populate_show_branches(self):
        self.show_branch_cb.clear()
        self.show_branch_cb.addItems(self.get_show_branches())

    def populate_categories(self):
        self.category_cb.clear()
        self.category_cb.addItems(self.get_categories())

    def populate_entries(self):
        self.entry_name_cb.clear()
        self.entry_name_cb.addItems(self.get_entries())

    def populate_existing_tasks_cb(self):
        self.task_name_cb.clear()
        all_tasks = self.get_all_tasks()
        if all_tasks == None:
            return []
        else:
            self.task_name_cb.addItems(self.get_all_tasks())

    def get_current_path(self):
        self.imports_from_lwd.imports_from_wdg.show_name = self.show_name_cb.currentText()
        self.imports_from_lwd.imports_from_wdg.branch_name = self.show_branch_cb.currentText()
        self.imports_from_lwd.imports_from_wdg.category_name = self.category_cb.currentText()
        self.imports_from_lwd.imports_from_wdg.entry_name = self.entry_name_cb.currentText()
        self.imports_from_lwd.imports_from_wdg.task_name = self.task_name_cb.currentText()

        self.imports_from_lwd.existing_tasks_lwd.show_name = self.show_name_cb.currentText()
        self.imports_from_lwd.existing_tasks_lwd.branch_name = self.show_branch_cb.currentText()
        self.imports_from_lwd.existing_tasks_lwd.category_name = self.category_cb.currentText()
        self.imports_from_lwd.existing_tasks_lwd.entry_name = self.entry_name_cb.currentText()
        self.imports_from_lwd.existing_tasks_lwd.task_name = self.task_name_cb.currentText()

        self.imports_from_lwd.populate()

    def populate_existing_assignments(self):
        self.get_current_path()
        self.imports_from_lwd.populate()

    def get_shows(self):
        shows = xac.get_all_active_shows()
        return shows

    def get_show_branches(self):
        show_branches = xac.get_show_branches_structure(self.show_name_cb.currentText())
        return show_branches

    def get_categories(self):
        sequences = xac.get_sub_branches(self.show_name_cb.currentText(), self.show_branch_cb.currentText())
        return sequences

    def get_entries(self):
        entries = xac.get_sub_branches_content(self.show_name_cb.currentText(), self.show_branch_cb.currentText(), self.category_cb.currentText())
        if entries != None:
            return entries
        else:
            return ["--empty category--"]

    def get_all_tasks(self):
        tasks = xac.get_tasks(self.show_name_cb.currentText(), self.show_branch_cb.currentText(),
                              self.category_cb.currentText(), self.entry_name_cb.currentText())
        if tasks != None:
            return tasks
        else:
            return ["-- no tasks --"]

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        self.imports_from_lwd.save_to_database()

        self.populate_existing_tasks_list()
        self.populate_existing_assignments()
        self.remove_self_task()

        self.remove_already_assigned()


if __name__ == "__main__":

    create_shot = SetTaskImportsFromUI()
    create_shot.show()
    sys.exit(app.exec_())