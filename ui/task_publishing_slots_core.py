import sys
from PySide2 import QtWidgets, QtCore, QtGui
from ui.task_publishing_slots_UI import PublishSlotsWidgetUI
from database.entities.db_entities import DbTasks, DbPubSlot
from common_utils.users import Users
from envars.envars import Envars


SLOTS_TYPES = ['abc', 'tex', 'vdb', 'bgeo', 'ptc', 'rend', 'exr', 'mat', 'pbr','img','scn', 'geo', 'csh', 'cfg']
SLOTS_SCOPE = ["local", "shots"]
SLOT_MODE = ["layer", "non_layer"]
SLOT_ARTISTS =["unassigned", Users().curr_user()]
SLOTS_METHODS = {'m1':'sf_csh',
                 'm2':'mf_csh',
                 'm3':'sf_geo',
                 'm4':'geo_bake',
                 'm5':'geo_sim',
                 'm6':'scn_exp',
                 'm7':'img_exp',
                 'm8':'anm_crv',
                 'm9':'scatter',
                 'm10':'p_exp',
                 'm11':'assign_exp',
                 'm12':'cfg_scn_exp',
                 'm13':'cfg_exp'}


class PublishSlotsWidgetCore(PublishSlotsWidgetUI):
    def __init__(self, parent=None):
        super(PublishSlotsWidgetCore, self).__init__(parent)

        self.create_connections()
        self.populate_main_widget()

    def create_connections(self):
        self.delete_list_item_btn.clicked.connect(self.remove_pub_slot)
        self.save_btn.clicked.connect(self.db_commit)
        self.refresh_btn.clicked.connect(self.populate_main_widget)
        self.refresh_btn.clicked.connect(self.populate_all_pub_slots)
        self.add_pub_slot_btn.clicked.connect(self.add_to_pub_list)
        self.publish_slots_wdg.cellClicked.connect(self.populate_all_pub_slots)
        self.publish_slots_wdg.cellClicked.connect(self.change_label_used_by)
        self.publish_slots_wdg.itemSelectionChanged.connect(self.selected_items_show)
        # self.dependent_pub_slots_wdg.itemClicked.connect(self.test_action)

    def clear_selection(self):
        self.publish_slots_wdg.clearSelection()

    def selected_items_show(self):
        selected_items_list = self.publish_slots_wdg.selectedItems()
        if len(selected_items_list) == 0:
            self.dependent_pub_slots_wdg.clear()
            self.all_pub_slots_lb.setText("--select slot--")
        for item in selected_items_list:
            return item.text()

    def test_action(self):
        self.write_wdg_checked_items()
        self.populate_all_pub_slots()

    def return_slot_name(self):
        button = self.sender()
        current_row = self.publish_slots_wdg.currentRow()

        if button:
            slot_name = self.get_slot_name(current_row, 0)
            return slot_name

    def change_label_used_by(self):
        slot_name = self.return_slot_name()
        my_font = QtGui.QFont()
        my_font.setBold(True)

        self.all_pub_slots_lb.clear()
        self.all_pub_slots_lb.setText("{0} -> used by".format(slot_name))
        self.all_pub_slots_lb.setFont(my_font)
        self.all_pub_slots_lb.setStyleSheet("color: red")

    def change_label_pub_slots(self):
        pub_slot_name = Envars().task_name
        my_font = QtGui.QFont()
        my_font.setBold(True)

        self.tasks_pub_slots_properties_lb.clear()
        self.tasks_pub_slots_properties_lb.setText("{0} -> Publishing Slots".format(pub_slot_name))
        self.tasks_pub_slots_properties_lb.setFont(my_font)
        self.tasks_pub_slots_properties_lb.setStyleSheet("color: red")

    def get_all_tasks(self):
        tasks = DbTasks().get_tasks()
        if tasks is not None:
            return tasks

    def populate_all_pub_slots(self):
        get_entry_tasks_names = self.get_all_tasks()
        get_active_tasks = []

        self.dependent_pub_slots_wdg.clear()

        for task in get_entry_tasks_names:
            is_active = DbTasks().is_active(task=task)

            if is_active:
                get_active_tasks.append(task)

        current_task = Envars().task_name
        get_active_tasks.remove(current_task)
        self.add_tasks_to_list(get_active_tasks)

    def add_tasks_to_list(self, tasks_list):
        for active_task in tasks_list:
            imp_from_pub_slots_schema = DbPubSlot().get_pub_slots(task_name=active_task)
            item = QtWidgets.QTreeWidgetItem([active_task])
            self.dependent_pub_slots_wdg.addTopLevelItem(item)

            slot_used_by = self.get_pub_used_by(self.return_slot_name())
            self.dependent_pub_slots_wdg.expandAll()

            try:
                for pub_slot, pub_slot_content in imp_from_pub_slots_schema.items():
                    pub_slot_item = QtWidgets.QTreeWidgetItem([pub_slot])
                    item.addChild(pub_slot_item)

                    used_by_data_format = ".".join([active_task, pub_slot_item.text(0)])

                    if used_by_data_format in slot_used_by:
                        pub_slot_item.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        pub_slot_item.setCheckState(0, QtCore.Qt.Unchecked)

            except:
                pass

    def get_wdg_checked_items(self):
        checked = dict()
        root = self.dependent_pub_slots_wdg.invisibleRootItem()
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
        root = self.dependent_pub_slots_wdg.invisibleRootItem()
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
        current_task = Envars().task_name
        checked_items = self.get_wdg_checked_items()
        unchecked_items = self.get_wdg_unchecked_items()
        current_pub_slot = self.return_slot_name()

        for task_name, task_pub_slots in checked_items.items():
            for pub_slot in task_pub_slots:
                used_by_data_format  = ".".join([task_name, pub_slot])
                DbPubSlot().set_used_by(task_name=current_task,
                                        pub_slot=current_pub_slot,
                                        used_by_data=used_by_data_format)

        for task_name, task_pub_slots in unchecked_items.items():
            for pub_slot in task_pub_slots:
                used_by_data_format = ".".join([task_name, pub_slot])
                DbPubSlot().set_used_by(task_name=current_task,
                                        pub_slot=current_pub_slot,
                                        used_by_data=used_by_data_format,
                                        remove_action=True)

    def get_pub_used_by(self, pub_slot):
        rel_task = DbPubSlot().get_used_by(pub_slot=pub_slot)
        return rel_task

    def get_properties(self):
        pub_slots = DbPubSlot().get_pub_slots()
        return pub_slots

    def populate_main_widget(self):
        properties = self.get_properties()
        if not properties is None:
            rows_cnt = len(properties)
            self.publish_slots_wdg.setRowCount(rows_cnt)
            cnt = 0
            for name in properties:
                self.create_pub_slots(name, cnt)
                self.publish_slots_wdg.resizeRowsToContents()
                cnt += 1
        return properties

    def create_pub_slots(self, name, row):
        item = QtWidgets.QTableWidgetItem(name)
        self.publish_slots_wdg.setItem(row, 0, item)

        self.set_type_cb = QtWidgets.QComboBox()
        self.set_type_cb.wheelEvent = lambda event: None
        self.set_type_cb.addItems(SLOTS_TYPES)

        self.set_method_cb = QtWidgets.QComboBox()
        self.set_method_cb.wheelEvent = lambda event: None
        self.set_method_cb.addItems(list(SLOTS_METHODS.values()))

        self.set_source_cb = QtWidgets.QComboBox()
        self.set_source_cb.wheelEvent = lambda event: None
        self.set_source_cb.addItems(self.get_current_pub_slots())

        self.set_scope_cb = QtWidgets.QComboBox()
        self.set_scope_cb.wheelEvent = lambda event: None
        self.set_scope_cb.addItems(SLOTS_SCOPE)

        self.set_mode_cb = QtWidgets.QComboBox()
        self.set_mode_cb.wheelEvent = lambda event: None
        self.set_mode_cb.addItems(SLOT_MODE)

        self.set_artists_cb = QtWidgets.QComboBox()
        self.set_artists_cb.wheelEvent = lambda event: None
        self.set_artists_cb.addItems(SLOT_ARTISTS)

        self.set_reviewable_ckb = QtWidgets.QCheckBox()
        self.set_active_ckb = QtWidgets.QCheckBox()

        try:
            self.set_type_cb.setCurrentText(str(self.get_db_pub_attr(name, "type")))
            self.set_method_cb.setCurrentText(str(self.get_db_pub_attr(name, 'method')))
            self.set_source_cb.setCurrentText(str(self.get_db_pub_attr(name, 'source')))
            self.set_scope_cb.setCurrentText(str(self.get_db_pub_attr(name, 'scope')))
            self.set_mode_cb.setCurrentText(str(self.get_db_pub_attr(name, 'mode')))
            self.set_artists_cb.setCurrentText(str(self.get_db_pub_attr(name, 'artists')))
            self.set_reviewable_ckb.setChecked(bool(self.get_db_pub_attr(name, 'reviewable')))
            self.set_active_ckb.setChecked(bool(self.get_db_pub_attr(name, 'active')))

        except:
            pass

        self.publish_slots_wdg.setCellWidget(row, 1, self.set_type_cb)
        self.publish_slots_wdg.setCellWidget(row, 2, self.set_method_cb)
        self.publish_slots_wdg.setCellWidget(row, 3, self.set_source_cb)
        self.publish_slots_wdg.setCellWidget(row, 4, self.set_scope_cb)
        self.publish_slots_wdg.setCellWidget(row, 5, self.set_mode_cb)
        self.publish_slots_wdg.setCellWidget(row, 6, self.set_artists_cb)
        self.publish_slots_wdg.setCellWidget(row, 7, self.set_reviewable_ckb)
        self.publish_slots_wdg.setCellWidget(row, 8, self.set_active_ckb)

    def get_db_pub_attr(self, slot, attr):
        properties = self.get_properties()
        to_attr = properties[slot]
        if attr not in to_attr.keys():
            return ["--NA--"]

        pub_attr = properties[slot][attr]
        return pub_attr

    def get_slot_name(self, row, column):
        slot_name = self.publish_slots_wdg.item(row, column)
        return slot_name.text()

    def get_cell_pub_cb(self, row, column):
        slot_artists = self.publish_slots_wdg.cellWidget(row, column)
        return slot_artists.currentText()

    def is_checked_chkb(self, row, column):
        rev_checked = self.publish_slots_wdg.cellWidget(row, column)
        return rev_checked.isChecked()

    def get_pub_buffer_content(self):
        items = []
        rows = self.publish_slots_wdg.rowCount()

        for r in range(rows):
            get_slot_name = self.get_slot_name(r, 0)
            get_existing_properties = self.get_properties()
            if get_slot_name in get_existing_properties:
                get_used_by = self.get_db_slot_used_by(get_slot_name)
            else:
                get_used_by = []

            dictionary_build = {self.get_slot_name(r, 0) : {'type':self.get_cell_pub_cb(r, 1),
                                                            'method':self.get_cell_pub_cb(r, 2),
                                                            'used_by':get_used_by,
                                                            'source':self.get_cell_pub_cb(r, 3),
                                                            'scope':self.get_cell_pub_cb(r, 4),
                                                            'mode':self.get_cell_pub_cb(r, 5),
                                                            'artists':self.get_cell_pub_cb(r, 6),
                                                            'reviewable':self.is_checked_chkb(r, 7),
                                                            'active':self.is_checked_chkb(r, 8)}}

            items.append(dictionary_build)



        return items

    def get_db_slot_used_by(self, slot):
        properties = self.get_properties()
        pub_is_used_by = properties[slot]['used_by']
        return pub_is_used_by

    def get_current_pub_slots(self):
        complete_list = list()
        pub_slots = DbPubSlot().get_pub_slots()
        if pub_slots:
            complete_list.append('root')
            for each in list(pub_slots.keys()):
                complete_list.append(each)

        return complete_list

    def insert_pub_slot_row(self, name):
        self.publish_slots_wdg.insertRow(0)
        self.create_pub_slots(name, 0)

    def remove_pub_slot(self):
        listItems = self.publish_slots_wdg.currentItem()
        selected_index = self.publish_slots_wdg.indexFromItem(listItems)
        self.publish_slots_wdg.removeRow(selected_index.row())

    def db_commit(self):
        get_wdg_content = self.get_pub_buffer_content()
        DbPubSlot().remove_all()
        DbPubSlot().add_dict(pub_slot=get_wdg_content)
        self.write_wdg_checked_items()

# PublishSlotsWidget -- END

    def add_to_pub_list(self):
        if self.add_pub_slot_le.text():
            self.insert_pub_slot_row(self.add_pub_slot_le.text())
            self.add_pub_slot_le.clear()
        else:
            return

if __name__ == "__main__":
    # from envars.envars import Envars

    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "props"
    Envars.entry_name = "red_knife"
    Envars.task_name = "sculpting"



    app = QtWidgets.QApplication(sys.argv)

    test_dialog = PublishSlotsWidgetCore()

    test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())