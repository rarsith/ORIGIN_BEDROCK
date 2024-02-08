import sys
from PySide2 import QtWidgets, QtCore, QtGui

from origin_data_base import xcg_db_actions as xac
from origin_config import xcg_validation as xval
from origin_config import xcg_slot_methods as xslop



class CreateTaskPubSlotsUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(CreateTaskPubSlotsUI, self).__init__(parent)

        self.setWindowTitle("Edit Task Publish Slots")
        self.setMinimumSize(550, 650)
        self.setMaximumSize(550, 650)

        self.setMinimumHeight(900)
        self.setMaximumHeight(900)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

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

        self.publish_slots_lb = QtWidgets.QLabel("Definition Builder")
        self.publish_slots_le = QtWidgets.QLineEdit()

        self.add_btn = QtWidgets.QPushButton("Add Attr")
        self.refresh_list_btn = QtWidgets.QPushButton("Refresh")
        self.delete_list_item_btn = QtWidgets.QPushButton("Remove")

        self.definition_wdg = QtWidgets.QTableWidget()
        self.definition_wdg.setColumnCount(2)
        self.definition_wdg.setHorizontalHeaderLabels(["Attribute Name", "Attribute Value"])
        self.definition_wdg.setShowGrid(False)
        self.definition_wdg.setAlternatingRowColors(True)
        header = self.definition_wdg.verticalHeader()
        header.hide()
        self.definition_wdg.setColumnWidth(0, 250)
        self.definition_wdg.setColumnWidth(1, 150)


        self.populate_definition_slots()

        self.create_btn = QtWidgets.QPushButton("Apply")
        self.create_and_close_btn = QtWidgets.QPushButton("Apply and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Show_name ", self.show_name_cb)
        form_layout.addRow("Show Branch", self.show_branch_cb)
        form_layout.addRow("Category", self.category_cb)
        form_layout.addRow("Entry Name", self.entry_name_cb)
        form_layout.addRow("Task Name", self.task_name_cb)
        form_layout.setSpacing(5)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)

        add_button_layout = QtWidgets.QHBoxLayout()
        add_button_layout.addWidget(self.publish_slots_le)
        add_button_layout.addWidget(self.add_btn)

        main_list_buttons_layout = QtWidgets.QVBoxLayout()
        main_list_buttons_layout.addWidget(self.refresh_list_btn)
        main_list_buttons_layout.addWidget(self.delete_list_item_btn)
        main_list_buttons_layout.addStretch()

        pub_slots_main_layout = QtWidgets.QHBoxLayout()
        pub_slots_main_layout.addWidget(self.definition_wdg)
        pub_slots_main_layout.addLayout(main_list_buttons_layout)
        # pub_slots_main_layout.addStretch()

        pub_slots_layout = QtWidgets.QVBoxLayout()
        pub_slots_layout.addWidget(self.publish_slots_lb)
        pub_slots_layout.addLayout(add_button_layout)

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(30)
        main_layout.addLayout(pub_slots_layout)
        main_layout.addLayout(pub_slots_main_layout)
        main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.show_name_cb.currentIndexChanged.connect(self.comboBox_shows)
        self.show_name_cb.currentIndexChanged.connect(self.populate_show_branches)
        self.show_name_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_name_cb.currentIndexChanged.connect(self.populate_entries)
        self.show_name_cb.currentIndexChanged.connect(self.populate_tasks)
        self.show_name_cb.currentIndexChanged.connect(self.populate_definition_slots)

        self.show_branch_cb.currentIndexChanged.connect(self.comboBox_show_branches)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_categories)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_entries)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_tasks)
        self.show_branch_cb.currentIndexChanged.connect(self.populate_definition_slots)

        self.category_cb.currentIndexChanged.connect(self.comboBox_categories)
        self.category_cb.currentIndexChanged.connect(self.populate_entries)
        self.category_cb.currentIndexChanged.connect(self.populate_tasks)
        self.category_cb.currentIndexChanged.connect(self.populate_definition_slots)

        self.entry_name_cb.currentIndexChanged.connect(self.comboBox_entries)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_tasks)
        self.entry_name_cb.currentIndexChanged.connect(self.populate_definition_slots)

        self.task_name_cb.currentIndexChanged.connect(self.comboBox_tasks)
        self.task_name_cb.currentIndexChanged.connect(self.populate_definition_slots)


        self.refresh_list_btn.clicked.connect(self.populate_definition_slots)
        self.delete_list_item_btn.clicked.connect(self.remove_pub_slot)
        self.add_btn.clicked.connect(self.add_to_pub_list)

        self.create_btn.clicked.connect(self.db_commit)
        self.create_and_close_btn.clicked.connect(self.db_commit_close)
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

    def comboBox_tasks(self):
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

    def populate_tasks(self):
        self.task_name_cb.clear()
        all_tasks = self.get_all_tasks()
        if all_tasks == None:
            return[]
        else:
            self.task_name_cb.addItems(self.get_all_tasks())

    def populate_definition_slots(self):
        properties = self.get_current_definition()
        rows_cnt = len(properties)
        self.definition_wdg.setRowCount(rows_cnt)
        cnt = 0
        for name in properties:
            self.create_pub_slots(name, cnt)
            cnt += 1

    def create_pub_slots(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)
        self.definition_wdg.setItem(row, 0, item)




    def insert_pub_slot_row(self, name):
        self.definition_wdg.insertRow(0)
        self.create_pub_slots(name, 0)

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
        return  entries

    def get_all_tasks(self):
        tasks = xac.get_tasks(self.show_name_cb.currentText(), self.show_branch_cb.currentText(),
                              self.category_cb.currentText(), self.entry_name_cb.currentText())
        j = ["--empty--"]

        if tasks != None:
            self.entry_name_cb.setDisabled(False)
            return tasks
        elif tasks == None:
            self.entry_name_cb.setDisabled(True)
            return j

    def get_current_definition(self):
        definition_data = xac.get_entry_definition(self.show_name_cb.currentText(),
                              self.show_branch_cb.currentText(),
                              self.category_cb.currentText(),
                              self.entry_name_cb.currentText())
        j = ["Empty"]

        if definition_data != None:
            self.publish_slots_le.setDisabled(False)
            self.definition_wdg.setDisabled(False)

            return definition_data
        elif definition_data == None:

            self.publish_slots_le.setDisabled(True)
            self.definition_wdg.setDisabled(True)
            self.task_name_cb.setDisabled(False)
            return j

    def remove_pub_slot(self):
        listItems = self.definition_wdg.currentItem()
        selected_index = self.definition_wdg.indexFromItem(listItems)
        self.definition_wdg.removeRow(selected_index.row())

    def get_slot_name(self, row, column):
        slot_name = self.definition_wdg.item(row, column)
        return slot_name.text()

    def get_slot_type(self, row, column):
        slot_type = self.definition_wdg.cellWidget(row, column)
        return slot_type.currentText()

    def active_is_checked(self, row, column):
        act_is_checked = self.definition_wdg.cellWidget(row, column)
        return act_is_checked.isChecked()

    def selected_is_checked(self, row, column):
        sel_is_checked = self.definition_wdg.cellWidget(row, column)
        return sel_is_checked.isChecked()

    def get_pub_buffer_content(self):
        items = []
        rows = self.definition_wdg.rowCount()
        for r in range(rows):
            dictionary_build = {self.get_slot_name(r, 0):{'type':self.get_slot_type(r, 1),'method':self.get_pub_method(r, 2),'reviewable':self.reviewable_is_checked(r, 3), 'active':self.active_is_checked(r, 4)}}
            items.append(dictionary_build)
        return items

    def insert_item(self, row, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        self.definition_wdg.setItem(row, column, item)
        self.definition_wdg.setCellWidget(row, 1, self.set_type_cb)
        self.definition_wdg.setCellWidget(row, 2, self.set_reviewable_ckb)
        self.definition_wdg.setCellWidget(row, 3, self.set_active_ckb)
        self.definition_wdg.setCellWidget(row, 4, self.set_select_ckb)

    def add_to_pub_list(self):
        if self.publish_slots_le.text():
            self.insert_pub_slot_row(self.publish_slots_le.text())
            self.publish_slots_le.clear()
        else:
            return

    def db_commit_close(self):
        self.db_commit()
        self.close()

    def db_commit(self):
        xac.remove_all_task_pub_slots(self.show_name_cb.currentText(),
                              self.show_branch_cb.currentText(),
                              self.category_cb.currentText(),
                              self.entry_name_cb.currentText(),
                              self.task_name_cb.currentText())

        xac.update_task_pub_slot_dict(self.show_name_cb.currentText(),
                                      self.show_branch_cb.currentText(),
                                      self.category_cb.currentText(),
                                      self.entry_name_cb.currentText(),
                                      self.task_name_cb.currentText(),
                                      pub_slot=self.get_pub_buffer_content())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    create_shot = CreateTaskPubSlotsUI()
    create_shot.show()
    sys.exit(app.exec_())