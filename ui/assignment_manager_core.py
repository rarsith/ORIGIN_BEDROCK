from PySide2 import QtWidgets, QtGui
from ui.assignment_manager_UI import AssignmentManagerUI
from database.db_types import BranchTypes
from database.entities.db_entities import DbProject
from database.utils.db_q_entity import *
from database.db_ids import DbIds
from database.entities.db_structures import DbProjectBranch, DbAssetCategories
from database.entities.db_entities import DbAsset
from common_utils import get_deep_value as gdeepval
from common_utils.version_increment import number_increment as numup


class AssignmentManagerCore(AssignmentManagerUI):

    def __init__(self, parent=None):
        super(AssignmentManagerCore, self).__init__(parent)

        self.buffer_ids = {}
        self.populate_shots_widget()
        self.populate_assets_widget()
        self.create_connections()

    def create_connections(self):
        """Create the connections for the widget"""
        self.project_shots_viewer_wdg.itemClicked.connect(self.get_selected_name_and_parent)
        self.project_shots_viewer_wdg.itemClicked.connect(self.get_sel_data)
        self.project_shots_viewer_wdg.itemSelectionChanged.connect(self.get_sel_data)
        self.project_shots_viewer_wdg.itemClicked.connect(self.update_label)
        self.project_shots_viewer_wdg.itemClicked.connect(self.populate_assignments_widget)
        self.project_shots_viewer_wdg.itemClicked.connect(self.populate_assets_widget)
        self.move_to_right_btn.clicked.connect(self.get_selected_name_and_parent)
        self.move_to_right_btn.clicked.connect(self.move_to_assigned)
        self.save_btn.clicked.connect(self.commit_to_db)
        self.remove_btn.clicked.connect(self.remove_assigned)
        self.refresh_btn.clicked.connect(self.populate_assignments_widget)
        self.apply_to_all_in_category_btn.clicked.connect(self.update_all_schemas_assets)
        self.collapse_all_btn.clicked.connect(self.assignments_collapse_all)
        self.expand_all_btn.clicked.connect(self.assignments_expand_all)
        self.expand_all_btn.clicked.connect(self.get_assigned_ref_ids)

    def update_info_label(self, message_in):
        """Update the info label with the message_in"""
        self.info_box_wdg.setText(message_in)

    def get_buffer_ids(self):
        return self.buffer_ids

# POPULATE THE WIDGET -- START
    def populate_shots_widget(self):
        """Populate the shots widget with the shots in the project"""
        valid_shot_branch = BranchTypes.sequences()
        try:
            self.project_shots_viewer_wdg.clear()
            get_branches = DbProjectBranch.get_branches()

            for branch in get_branches:
                branch_type = DbProjectBranch().get_branch_type(branch)
                if branch_type == valid_shot_branch:
                    item = self.show_tree_create_item(branch)
                    self.project_shots_viewer_wdg.addTopLevelItem(item)
                    self.project_shots_viewer_wdg.expandAll()

        except ValueError as e:
            print (f"Something wrong in refresh_tree_widget: {e}")

    def populate_assets_widget(self):
        """Populate the assets widget with the assets in the project"""
        valid_build_branch = BranchTypes.build()
        try:
            self.project_assets_viewer_wdg.clear()
            get_branches = DbProjectBranch.get_branches()

            for branch in get_branches:
                branch_type = DbProjectBranch().get_branch_type(branch)
                if branch_type == valid_build_branch:
                    item = self.show_tree_create_item(branch)
                    self.project_assets_viewer_wdg.addTopLevelItem(item)
                    self.project_assets_viewer_wdg.expandAll()

        except ValueError as e:
            print (f"Something wrong in refresh_tree_widget: {e}")

    def populate_assignments_widget(self):
        """Populate the assignments widget with the assignments in the project"""
        assigned_entities_list = self.get_assigned_entities()
        self.assignment_tree_viewer_wdg.clear()
        self.add_to_assignments(assigned_entities_list)
        self.assignment_tree_viewer_wdg.setSortingEnabled(True)

    def add_to_assignments(self, source_data: dict):
        try:
            if source_data:
                items = []
                for slot_name, assigned_data in source_data.items():
                    item = QtWidgets.QTreeWidgetItem([slot_name])

                    # font settings
                    my_font = QtGui.QFont()
                    my_font.setBold(True)
                    item.setFont(0, my_font)
                    background_color = QtGui.QColor("#acc8d7")
                    item.setBackgroundColor(0, background_color)
                    item.setBackgroundColor(1, background_color)

                    button_test = QtWidgets.QPushButton("Delete")
                    self.assignment_tree_viewer_wdg.setItemWidget(item, 1, button_test)  # doesn't work

                    for attr, value in assigned_data.items():
                        child = QtWidgets.QTreeWidgetItem([attr, str(value)])

                        # font settings
                        my_font = QtGui.QFont()
                        my_font.setPixelSize(10)
                        child.setFont(0, my_font)
                        child.setFont(1, my_font)

                        item.addChild(child)
                    items.append(item)

                    self.assignment_tree_viewer_wdg.addTopLevelItems(items)

        except ValueError as e:
            print(f"Something wrong in add_to_assignments: {e}")

    def show_tree_create_item(self, name):
        iso_name = self.get_entry_name_from_id(name)
        item = QtWidgets.QTreeWidgetItem([iso_name])
        self.add_children(item)
        return item

    def get_entry_name_from_id(self, name: str, delimiter=".") -> str:
        if delimiter not in name:
            return name
        isolate_last = name.split(delimiter)[-1]
        return isolate_last

    def add_children(self, item):
        get_children = gdeepval.deep_values(item.text(0), self.get_show_structure())
        for children in get_children:
            for child in sorted(children):
                is_ref = self.is_entity_reference(child)
                if child != "type":
                    child_item = self.show_tree_create_item(child)
                    if is_ref:
                        get_seq = child.split(".")[-2]
                        self.buffer_ids[get_seq + "_" + child_item.text(0)] = child
                    item.addChild(child_item)

    def is_entity_reference(self, string_to_check, delimiter=","):
        if delimiter in string_to_check:
            return True

    def get_show_structure(self):
        try:
            entity = DbProject.get_structure()
            return entity
        except:
            print("shit Happened!! in GET_SHOW_STRUCTURE_FUNC")

    def get_assigned_entities(self) -> dict:
        current_entity_id = DbIds().curr_entry_id()
        assigned_entities_list = QEntity(db_collection=From().current_branch_type(),
                                         entry_id=current_entity_id,
                                         attribute_path=DbEntityAttrPaths.to_assignments()).get_attr_values()
        if assigned_entities_list:
            return assigned_entities_list

    def get_next_entry(self, list_to_iter, dict_to_iter):
        next_entries = []
        for categories, assets in dict_to_iter.items():
            for asset in assets:
                prefix_assigned = "_".join([categories, asset])
                list_existing = [assigned.split("_")[-1] for assigned in list_to_iter if
                                 assigned.startswith(prefix_assigned)]
                if list_existing:
                    next_numup = numup(list_existing)
                else:
                    next_numup = "0000"
                next_name = prefix_assigned + "_" + str(next_numup)
                next_entries.append(next_name)
        return next_entries

    def get_sel_data(self):
        branch = list()
        branch_type = str()
        category = list()
        entry = list()

        get_selected_objects = self.project_shots_viewer_wdg.currentItem()
        get_selected_show = Envars().show_name

        if get_selected_objects is None:
            return[]

        else:
            parent = self.get_parent()
            grandparent = self.get_grandparent()
            if not parent and not grandparent:
                branch.append(get_selected_objects.text(0))

            elif not grandparent:
                branch.append(parent)
                category.append(get_selected_objects.text(0))

            else:
                branch.append(grandparent)
                category.append(parent)
                entry.append(get_selected_objects.text(0))

        if get_selected_show:
            Envars.show_name = get_selected_show

        if branch:
            Envars.branch_name = branch[0]
        else:
            Envars.branch_name = None

        if category:
            Envars.category = category[0]
        else:
            Envars.category = None

        if entry:
            Envars.entry_name = entry[0]
        else:
            Envars.entry_name = None

        # print(Envars.show_name, Envars.branch_name, Envars.category, Envars.entry_name)

    def get_parent(self):
        get_selected_objects = self.project_shots_viewer_wdg.currentItem()
        parent = get_selected_objects.parent()
        if parent:
            return parent.text(0)

    def get_grandparent(self):
        get_selected_objects = self.project_shots_viewer_wdg.currentItem()
        parent = get_selected_objects.parent()
        try:
            grandparent = parent.parent()
            return grandparent.text(0)
        except:
            pass

    def get_selected_name_and_parent(self) -> dict:
        """returns a dict with parent as key and list of selected items as values"""

        get_selected_objects = self.project_assets_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return {}
        elif len(get_selected_objects) >= 1:
            names = {}
            for item in get_selected_objects:
                parent = item.parent().text(0)
                names[parent] = [x.text(0) for x in get_selected_objects if x.parent().text(0) == parent]
            return names

    def extract_wdg_content(self, wdg):
        root = wdg.invisibleRootItem()

        def tree_to_dict(parent):
            childCount = parent.childCount()
            if not childCount:
                return parent.text(1)
            content = {}
            for row in range(childCount):
                child = parent.child(row)
                content[child.text(0)] = tree_to_dict(child)
            return content

        existing_assignments = tree_to_dict(root)
        return existing_assignments

    def get_assigned_wdg_content(self) -> list:
        existing_assignments = []
        root = self.assignment_tree_viewer_wdg.invisibleRootItem()
        root_level = root.childCount()
        for idx in range(root_level):
            assigned_entities_names = root.child(idx)
            existing_assignments.append(assigned_entities_names.text(0))
        return existing_assignments

    def construct_entry(self, assignee_name, ref_id, active=True):
        data_to_add = dict({assignee_name: {"ref_id": ref_id, "slot": assignee_name, "active": active}})
        return data_to_add

    def move_to_assigned(self):
        selected_assets = self.get_selected_name_and_parent()
        existing_assignments = self.get_assigned_wdg_content()
        next_names = self.get_next_entry(existing_assignments, selected_assets)

        for name in next_names:
            base_name = "_".join(name.split("_")[:-1])
            entry_reference_path = self.buffer_ids[base_name]

            data_to_add = self.construct_entry(assignee_name=name, ref_id=entry_reference_path, active=True)
            self.add_to_assignments(data_to_add)

    def update_label(self):
        current_entity_name = Envars().entry_name
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.assignments_lb.clear()
        if current_entity_name:
            self.assignments_lb.setText("{0} Assigned Assets".format(current_entity_name.upper()))
            self.assignments_lb.setFont(my_font)
            self.assignments_lb.setStyleSheet("color: red")

    def get_assigned_ref_ids(self):
        assigned_ids = []
        existing_assignments = self.get_assigned_wdg_content()
        for name in existing_assignments:
            base_name = "_".join(name.split("_")[:-1])
            entry_reference_path = self.buffer_ids[base_name]
            assigned_ids.append(entry_reference_path)
        return set(assigned_ids)

    def get_assigned(self):
        existing_assignments = QEntity(db_collection=From().current_branch_type(),
                                       entry_id=DbIds.curr_entry_id(),
                                       attribute_path=DbEntityAttrPaths.to_assignments()).get_attr_values()
        return existing_assignments

    def get_db_assigned_ref_ids(self):
        assigned_ids = []
        existing_assignments = QEntity(db_collection=From().current_branch_type(),
                                       entry_id=DbIds.curr_entry_id(),
                                       attribute_path=DbEntityAttrPaths.to_assignments()).get_attr_values()

        for name in existing_assignments:
            base_name = "_".join(name.split("_")[:-1])
            entry_reference_path = self.buffer_ids[base_name]
            assigned_ids.append(entry_reference_path)
        return set(assigned_ids)

    def insert_assignee_entry(self, collection, entity_id, attr_path, data_to_add):
        QEntity(db_collection=collection,
                entry_id=entity_id,
                attribute_path=attr_path).add(data=data_to_add)

    def commit_to_db(self):
        """commits the current assignments to the database"""
        current_content = self.extract_wdg_content(wdg=self.assignment_tree_viewer_wdg)
        current_entity_id = DbIds.curr_entry_id()

        assigned_ref_ids = self.get_assigned_ref_ids()      # get assigned ids from wdg
        assigned_db_ref_ids = self.get_db_assigned_ref_ids()    # get assigned ids from db

        QEntity(db_collection=From().current_branch_type(),     # clear current assignments
                entry_id=current_entity_id,                # from db
                attribute_path=DbEntityAttrPaths.to_assignments()).clear()

        QEntity(db_collection=From().current_branch_type(),     # add current assignments
                entry_id=current_entity_id,               # to db
                attribute_path=DbEntityAttrPaths.to_assignments()).update(current_content)

        ref_parent = ",".join([From().current_branch_type(), DbIds().curr_entry_id()])  # add current entity to assigned_to

        for each_id in assigned_ref_ids:
            collection = each_id.split(",")[0]
            entry_id = each_id.split(",")[1]

            assigned_to_list = QEntity(db_collection=collection,
                                       entry_id=entry_id,
                                       attribute_path=DbEntityAttrPaths.to_assigned_to()).get_attr_values()
            if ref_parent not in assigned_to_list:
                DbReferences.add_db_id_reference(collection=collection,
                                                 parent_doc_id=entry_id,
                                                 destination_slot=DbEntityAttrPaths.to_assigned_to(),
                                                 id_to_add=DbIds().curr_entry_id(),
                                                 from_collection=From().current_branch_type())

        removed_wdg_ids = [diff_id for diff_id in assigned_db_ref_ids if diff_id not in assigned_ref_ids]

        for rem_wdg_id in removed_wdg_ids:
            collection = rem_wdg_id.split(",")[0]
            entry_id = rem_wdg_id.split(",")[1]
            QEntity(db_collection=collection,
                    entry_id=entry_id,
                    attribute_path=DbEntityAttrPaths.to_assigned_to()).remove_value(ref_parent)

    def remove_assigned(self):
        """removes the selected assignments from the list"""
        list_items = self.assignment_tree_viewer_wdg.selectedItems()
        for sel_item in list_items:
            selected_index = self.assignment_tree_viewer_wdg.indexFromItem(sel_item)
            remove_it = selected_index.row()
            self.assignment_tree_viewer_wdg.takeTopLevelItem(remove_it)

    def assignments_collapse_all(self):
        """collapses all the assignments in the list"""
        self.assignment_tree_viewer_wdg.collapseAll()

    def assignments_expand_all(self):
        """expands all the assignments in the list"""
        self.assignment_tree_viewer_wdg.expandAll()

    def update_all_schemas_assets(self):
        """updates the assets in the schema"""
        valid_build_branch = "assets"

        assigned_entities_schema = self.get_assigned()
        # print(assigned_entities_schema)

        get_cat_assets_reference = DbAsset().get_all()
        # print("get_cat_assets_reference", get_cat_assets_reference)

        assigned_db_ref_ids = self.get_db_assigned_ref_ids()
        print("assigned_db_ref_ids", assigned_db_ref_ids)

        get_assets_in_branch = QEntity(db_collection=From().builds,
                                       entry_id=DbIds.all_in_collection(),
                                       attribute_path=DbProjectAttrPaths.curr_show()
                                       ).get_all_ids_collection(condition={"show_name": Envars().show_name})

        all_assets_ids_in_branch = []
        for item in get_assets_in_branch:
            all_assets_ids_in_branch.append(item["_id"])

        print(all_assets_ids_in_branch)

        for entity_ref in get_cat_assets_reference:
            entity_id = entity_ref.split(",")[1]
            QEntity(db_collection=From().current_branch_type(),
                    entry_id=entity_id,
                    attribute_path=DbEntityAttrPaths.to_assignments()
                    ).update(data=assigned_entities_schema)

        for assigned_id in assigned_db_ref_ids:
            collection = assigned_id.split(",")[0]
            entry_id = assigned_id.split(",")[1]
            assigned_to_list = QEntity(db_collection=collection,
                                       entry_id=entry_id,
                                       attribute_path=DbEntityAttrPaths.to_assigned_to()).get_attr_values()
            for entity_ref in get_cat_assets_reference:
                if entity_ref not in assigned_to_list:
                    entity_id = entity_ref.split(",")[1]
                    DbReferences.add_db_id_reference(collection=collection,
                                                     parent_doc_id=entry_id,
                                                     destination_slot=DbEntityAttrPaths.to_assigned_to(),
                                                     id_to_add=entity_id,
                                                     from_collection=From().current_branch_type())



        self.update_info_label(message_in="All Assignments In {0} Category Have been Updated To Selected Assignment Schema".format((Envars.category).upper()))

    # TODO to implement Loading assignments from a given entity
    # TODO to implement Assignments to SEQ level to serve byt default all entities in the SEQ (temoplates, persistent assignemtns)

class AssignmentManagerMainUI(QtWidgets.QMainWindow):
    WINDOW_TITLE = "Shot Assignments Manager"

    def __init__(self, parent=None):
        super(AssignmentManagerMainUI, self).__init__(parent)
        self.setWindowTitle(self.window_context_details())
        central_widget = AssignmentManagerCore()
        self.setCentralWidget(central_widget)

    def window_context_details(self):
        show_name = (Envars().show_name).upper()
        branch_name = (Envars().branch_name).upper()

        window_name = " -> ".join([self.WINDOW_TITLE, show_name, branch_name])
        return window_name


if __name__ == '__main__':
    import sys

    Envars.show_name = "Green"
    Envars.branch_name = "sequences"
    Envars.category = "XPM"
    Envars.entry_name = "0150"
    Envars.task_name = "animation"

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = AssignmentManagerMainUI()
    test_dialog.centralWidget().populate_shots_widget()
    test_dialog.show()
    sys.exit(app.exec_())