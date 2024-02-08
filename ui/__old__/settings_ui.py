import sys
from PySide2 import QtWidgets

from origin_data_base import xcg_db_actions as xac
from origin_config import xcg_validation as xval
from origin_config import xcg_slot_methods as xslop
from origin_database_custom_widgets import xcg_task_imports_from_core, xcg_task_publishing_slots_core


class CreateTasksSchema(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CreateTasksSchema, self).__init__(parent)

        self.setWindowTitle("Xchange Create Tasks Schemas")

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.impots_from_wdg = xcg_task_imports_from_core.TasksImportFromUI()
        self.publish_slots_wdg = xcg_task_publishing_slots_core.PublishSlotsWidgetUI()

        self.defined_categories_cb  = QtWidgets.QComboBox()
        self.defined_categories_cb.addItems(self.get_defined_categories())



        self.exiting_schema_lwd = QtWidgets.QListWidget()
        self.exiting_schema_lwd.addItem('schema001.json')


        self.task_add_btn = QtWidgets.QPushButton("Add")
        self.task_import_btn = QtWidgets.QPushButton("Import Schema")
        self.task_le = QtWidgets.QLineEdit()
        self.task_le.setPlaceholderText("Enter Task Name to Create")
        self.tasks_wdg = QtWidgets.QListWidget()

        self.pub_slots_le = QtWidgets.QLineEdit()
        self.pub_slots_btn = QtWidgets.QPushButton('Add')
        self.pub_slots_wdg = QtWidgets.QTableWidget()
        self.pub_slots_wdg.setColumnCount(1)
        self.pub_slots_wdg.setHorizontalHeaderLabels(["Name"])
        self.pub_slots_wdg.setShowGrid(False)
        self.pub_slots_wdg.setAlternatingRowColors(True)
        header = self.pub_slots_wdg.verticalHeader()
        header.hide()
        self.pub_slots_wdg.setColumnWidth(0, 150)
        self.pub_slots_wdg.setColumnWidth(1, 150)

    def create_layout(self):

        create_task_btn_lay = QtWidgets.QHBoxLayout()
        create_task_btn_lay.addWidget(self.task_le)
        create_task_btn_lay.addWidget(self.task_add_btn)
        create_task_btn_lay.addWidget(self.task_import_btn)

        create_task_layout = QtWidgets.QVBoxLayout()
        create_task_layout.addWidget(self.defined_categories_cb)
        create_task_layout.addLayout(create_task_btn_lay)
        create_task_layout.addWidget(self.tasks_wdg)

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.exiting_schema_lwd)
        main_layout.addLayout(create_task_layout)
        main_layout.addWidget(self.impots_from_wdg)
        main_layout.addWidget(self.publish_slots_wdg)

    def create_connections(self):
        pass

    def get_defined_categories(self):
        print ('TODO')
        return (['Test Category'])


class XchangeHierarchyUI(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(XchangeHierarchyUI, self).__init__(parent)

        self.setWindowTitle("Xchange Hierarchy")
        self.setMinimumWidth(950)


        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.root_types_twg = QtWidgets.QTableWidget()
        self.root_types_twg.setColumnCount(1)
        self.root_types_twg.setHorizontalHeaderLabels(["Name"])
        self.root_types_twg.setShowGrid(False)
        self.root_types_twg.setAlternatingRowColors(True)
        header = self.root_types_twg.verticalHeader()
        header.hide()
        self.root_types_twg.setColumnWidth(0, 150)
        self.root_types_twg.setColumnWidth(1, 150)
        self.root_types_le = QtWidgets.QLineEdit()
        self.root_types_le.setPlaceholderText('Enter Name')

        self.root_types_add_btn = QtWidgets.QPushButton("Add")
        self.root_types_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.root_types_delete_item_btn = QtWidgets.QPushButton("Remove")
        self.root_types_commit_btn = QtWidgets.QPushButton("Commit")

        self.branch_types_twg = QtWidgets.QTableWidget()
        self.branch_types_twg.setColumnCount(1)
        self.branch_types_twg.setHorizontalHeaderLabels(["Name"])
        self.branch_types_twg.setShowGrid(False)
        self.branch_types_twg.setAlternatingRowColors(True)
        header = self.branch_types_twg.verticalHeader()
        header.hide()
        self.branch_types_twg.setColumnWidth(0, 150)
        self.branch_types_twg.setColumnWidth(1, 150)
        self.branch_types_le = QtWidgets.QLineEdit()
        self.branch_types_le.setPlaceholderText('Enter Name')

        self.branch_types_add_btn = QtWidgets.QPushButton("Add")
        self.branch_types_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.branch_types_delete_item_btn = QtWidgets.QPushButton("Remove")
        self.branch_types_commit_btn = QtWidgets.QPushButton("Commit")

        self.categories_twg = QtWidgets.QTableWidget()
        self.categories_twg.setColumnCount(2)
        self.categories_twg.setHorizontalHeaderLabels(["Name", "Type"])
        self.categories_twg.setShowGrid(False)
        self.categories_twg.setAlternatingRowColors(True)
        header = self.categories_twg.verticalHeader()
        header.hide()
        self.categories_twg.setColumnWidth(0, 150)
        self.categories_twg.setColumnWidth(1, 150)
        self.categories_le = QtWidgets.QLineEdit()
        self.categories_le.setPlaceholderText('Enter Name')

        self.categories_add_btn = QtWidgets.QPushButton("Add")
        self.categories_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.categories_delete_item_btn = QtWidgets.QPushButton("Remove")
        self.categories_commit_btn = QtWidgets.QPushButton("Commit")

        self.root_types_lb = QtWidgets.QLabel("Xchange Root Types")
        self.branches_types_lb = QtWidgets.QLabel("Xchange Branches Types")
        self.categories_types_lb = QtWidgets.QLabel("Xchange Categories Types")
        self.subcategories_types_lb = QtWidgets.QLabel("Xchange Library Tags")

        self.subcategories_twg = QtWidgets.QTableWidget()
        self.subcategories_twg.setColumnCount(1)
        self.subcategories_twg.setHorizontalHeaderLabels(["Name"])
        self.subcategories_twg.setShowGrid(False)
        self.subcategories_twg.setAlternatingRowColors(True)
        header = self.subcategories_twg.verticalHeader()
        header.hide()
        self.subcategories_twg.setColumnWidth(0, 150)
        self.subcategories_twg.setColumnWidth(1, 150)
        self.subcategories_le = QtWidgets.QLineEdit()
        self.subcategories_le.setPlaceholderText('Enter Name')

        self.subcategories_add_btn = QtWidgets.QPushButton("Add")
        self.subcategories_refresh_btn = QtWidgets.QPushButton("Refresh")
        self.subcategories_delete_item_btn = QtWidgets.QPushButton("Remove")
        self.subcategories_commit_btn = QtWidgets.QPushButton("Commit")
        # self.populate_all()

        self.create_and_close_btn = QtWidgets.QPushButton("Save and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        root_types_btn_lay = QtWidgets.QHBoxLayout()
        root_types_btn_lay.addWidget(self.root_types_le)
        root_types_btn_lay.addWidget(self.root_types_add_btn)

        root_types_layout = QtWidgets.QVBoxLayout()
        root_types_layout.addWidget(self.root_types_lb)
        root_types_layout.addLayout(root_types_btn_lay)
        root_types_layout.addWidget(self.root_types_twg)
        root_types_layout.addWidget(self.root_types_refresh_btn)
        root_types_layout.addWidget(self.root_types_delete_item_btn)
        root_types_layout.addWidget(self.root_types_commit_btn)

        branches_types_btn_lay = QtWidgets.QHBoxLayout()
        branches_types_btn_lay.addWidget(self.branch_types_le)
        branches_types_btn_lay.addWidget(self.branch_types_add_btn)

        branches_types_layout = QtWidgets.QVBoxLayout()
        branches_types_layout.addWidget(self.branches_types_lb)
        branches_types_layout.addLayout(branches_types_btn_lay)
        branches_types_layout.addWidget(self.branch_types_twg)
        branches_types_layout.addWidget(self.branch_types_refresh_btn)
        branches_types_layout.addWidget(self.branch_types_delete_item_btn)
        branches_types_layout.addWidget(self.branch_types_commit_btn)



        categories_types_btn_lay = QtWidgets.QHBoxLayout()
        categories_types_btn_lay.addWidget(self.categories_le)
        categories_types_btn_lay.addWidget(self.categories_add_btn)

        categories_types_layout = QtWidgets.QVBoxLayout()
        categories_types_layout.addWidget(self.categories_types_lb)

        categories_types_layout.addLayout(categories_types_btn_lay)
        categories_types_layout.addWidget(self.categories_twg)
        categories_types_layout.addWidget(self.categories_refresh_btn)
        categories_types_layout.addWidget(self.categories_delete_item_btn)
        categories_types_layout.addWidget(self.categories_commit_btn)

        subcategories_types_btn_lay = QtWidgets.QHBoxLayout()
        subcategories_types_btn_lay.addWidget(self.subcategories_le)
        subcategories_types_btn_lay.addWidget(self.subcategories_add_btn)

        subcategories_types_layout = QtWidgets.QVBoxLayout()
        subcategories_types_layout.addWidget(self.subcategories_types_lb)

        subcategories_types_layout.addLayout(subcategories_types_btn_lay)
        subcategories_types_layout.addWidget(self.subcategories_twg)
        subcategories_types_layout.addWidget(self.subcategories_refresh_btn)
        subcategories_types_layout.addWidget(self.subcategories_delete_item_btn)
        subcategories_types_layout.addWidget(self.subcategories_commit_btn)

        all_windows_layout = QtWidgets.QHBoxLayout()
        all_windows_layout.addLayout(root_types_layout)
        all_windows_layout.addLayout(branches_types_layout)
        all_windows_layout.addLayout(categories_types_layout)
        all_windows_layout.addLayout(subcategories_types_layout)


        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.create_and_close_btn)
        buttons_layout.addWidget(self.cancel_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(all_windows_layout)
        main_layout.addSpacing(30)

    def create_connections(self):
        pass

    def comboBox_shows(self):
        pass

    def comboBox_show_branches(self):
        pass

    def comboBox_categories(self):
        pass

    def comboBox_entries(self):
        pass

    def comboBox_tasks(self):
        pass

    def populate_all(self):
        self.show_branch_cb.clear()
        self.show_branch_cb.addItems(self.get_show_branches())

    def populate_pub_slots(self):
        properties = self.get_current_pub_slots()
        rows_cnt = len(properties)
        self.task_pub_slots_wdg.setRowCount(rows_cnt)
        cnt = 0
        for name in properties:
            self.create_pub_slots(name, cnt)
            cnt += 1

    def create_pub_slots(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)
        self.task_pub_slots_wdg.setItem(row, 0, item)

        self.set_type_cb = QtWidgets.QComboBox()
        self.set_type_cb.addItems(xval.SLOTS_TYPES)
        self.set_method_cb = QtWidgets.QComboBox()
        self.set_method_cb.addItems(list(xslop.SLOTS_METHODS.values()))

        self.set_reviewable_ckb = QtWidgets.QCheckBox()
        self.set_active_ckb = QtWidgets.QCheckBox()

        try:
            self.set_type_cb.setCurrentText(self.get_db_pub_type(name))
            self.set_method_cb.setCurrentText(self.get_db_pub_method(name))
            self.set_reviewable_ckb.setChecked(self.get_db_pub_reviewable(name))
            self.set_active_ckb.setChecked(self.get_db_pub_active(name))
            # self.set_select_ckb.setChecked(self.get_db_pub_selected(name))
        except:
            pass

        self.task_pub_slots_wdg.setCellWidget(row, 1, self.set_type_cb)
        self.task_pub_slots_wdg.setCellWidget(row, 2, self.set_method_cb)
        self.task_pub_slots_wdg.setCellWidget(row, 3, self.set_reviewable_ckb)
        self.task_pub_slots_wdg.setCellWidget(row, 4, self.set_active_ckb)

    def insert_pub_slot_row(self, name):
        self.task_pub_slots_wdg.insertRow(0)
        self.create_pub_slots(name, 0)

    def remove_pub_slot(self):
        listItems = self.task_pub_slots_wdg.currentItem()
        selected_index = self.task_pub_slots_wdg.indexFromItem(listItems)
        self.task_pub_slots_wdg.removeRow(selected_index.row())

    def get_slot_name(self, row, column):
        slot_name = self.task_pub_slots_wdg.item(row, column)
        return slot_name.text()

    def get_slot_type(self, row, column):
        slot_type = self.task_pub_slots_wdg.cellWidget(row, column)
        return slot_type.currentText()

    def get_db_pub_type(self, slot):
        state = xac.get_pub_type(self.show_name_cb.currentText(),
                          self.show_branch_cb.currentText(),
                          self.category_cb.currentText(),
                          self.entry_name_cb.currentText(),
                          self.task_name_cb.currentText(),
                              slot)
        return state[0]

    def get_pub_method(self, row, column):
        slot_method = self.task_pub_slots_wdg.cellWidget(row, column)
        return slot_method.currentText()

    def get_db_pub_method(self, slot):
        state = xac.get_pub_method(self.show_name_cb.currentText(),
                          self.show_branch_cb.currentText(),
                          self.category_cb.currentText(),
                          self.entry_name_cb.currentText(),
                          self.task_name_cb.currentText(),
                              slot)
        return state[0]

    def reviewable_is_checked(self, row, column):
        rev_checked = self.task_pub_slots_wdg.cellWidget(row, column)
        return rev_checked.isChecked()

    def get_db_pub_reviewable(self, slot):
        state = xac.get_pub_is_reviewable(self.show_name_cb.currentText(),
                              self.show_branch_cb.currentText(),
                              self.category_cb.currentText(),
                              self.entry_name_cb.currentText(),
                              self.task_name_cb.currentText(),
                                 slot)
        return state[0]

    def active_is_checked(self, row, column):
        act_is_checked = self.task_pub_slots_wdg.cellWidget(row, column)
        return act_is_checked.isChecked()

    def get_db_pub_active(self, slot):
        state = xac.get_pub_is_active(self.show_name_cb.currentText(),
                              self.show_branch_cb.currentText(),
                              self.category_cb.currentText(),
                              self.entry_name_cb.currentText(),
                              self.task_name_cb.currentText(),
                                 slot)
        return state[0]

    def selected_is_checked(self, row, column):
        sel_is_checked = self.task_pub_slots_wdg.cellWidget(row, column)
        return sel_is_checked.isChecked()

    def get_pub_buffer_content(self):
        items = []
        rows = self.task_pub_slots_wdg.rowCount()
        for r in range(rows):
            dictionary_build = {self.get_slot_name(r, 0):{'type':self.get_slot_type(r, 1),'method':self.get_pub_method(r, 2),'reviewable':self.reviewable_is_checked(r, 3), 'active':self.active_is_checked(r, 4)}}
            items.append(dictionary_build)
        return items

    def insert_item(self, row, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        self.task_pub_slots_wdg.setItem(row, column, item)
        self.task_pub_slots_wdg.setCellWidget(row, 1, self.set_type_cb)
        self.task_pub_slots_wdg.setCellWidget(row, 2, self.set_reviewable_ckb)
        self.task_pub_slots_wdg.setCellWidget(row, 3, self.set_active_ckb)
        self.task_pub_slots_wdg.setCellWidget(row, 4, self.set_select_ckb)

    def add_to_pub_list(self):
        if self.publish_slots_le.text():
            self.insert_pub_slot_row(self.publish_slots_le.text())
            self.publish_slots_le.clear()
        else:
            return

    def db_commit_close(self):
        self.db_commit()
        self.close()

    # def db_commit(self):
        # xac.remove_all_task_pub_slots(self.show_name_cb.currentText(),
        #                       self.show_branch_cb.currentText(),
        #                       self.category_cb.currentText(),
        #                       self.entry_name_cb.currentText(),
        #                       self.task_name_cb.currentText())
        #
        # xac.update_task_pub_slot_dict(self.show_name_cb.currentText(),
        #                               self.show_branch_cb.currentText(),
        #                               self.category_cb.currentText(),
        #                               self.entry_name_cb.currentText(),
        #                               self.task_name_cb.currentText(),
        #                               pub_slot=self.get_pub_buffer_content())


class XchangeSettingsUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(XchangeSettingsUI, self).__init__(parent)

        self.setWindowTitle("Xchange Setup")
        self.setMinimumWidth(950)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.xcg_hierachy_tvw = XchangeHierarchyUI()
        self.xcg_tasks_schema_tvw = CreateTasksSchema()

        self.middle_tabmenu_tab = QtWidgets.QTabWidget()
        self.middle_tabmenu_tab.addTab(self.xcg_tasks_schema_tvw, "Tasks Schemas")
        self.middle_tabmenu_tab.addTab(self.xcg_hierachy_tvw, "Hierarchies")
        self.middle_tabmenu_tab.setTabPosition(QtWidgets.QTabWidget.West)

        self.create_and_close_btn = QtWidgets.QPushButton("Save and Close")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.middle_tabmenu_tab)

    def create_connections(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    create_shot = XchangeSettingsUI()
    create_shot.show()
    sys.exit(app.exec_())