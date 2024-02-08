from PySide2 import QtWidgets, QtGui
from envars.envars import Envars
from ui.project_tree_viewer_UI import ProjectTreeViewerUI
from database.entities.db_entities import DbProject
from database.entities.db_structures import DbProjectBranch
from common_utils import get_deep_value as gdeepval
from ui import create_asset_ui, create_asset_category_ui, task_manager_core, assignment_manager_core, create_branch_ui, \
    create_seq_ui, create_show_ui, create_shot_ui


class ProjectTreeViewerCore(ProjectTreeViewerUI):
    def __init__(self, parent=None):
        super(ProjectTreeViewerCore, self).__init__(parent)

        self.create_show_actions()
        self.create_connections()
        self.populate_shows_cb()
        self.refresh_tree_widget()
        self.context_menu()

    def create_connections(self):
        """Creates all the connections for the UI"""
        self.show_select_cb.currentIndexChanged.connect(self.curr_sel_show)
        self.show_select_cb.currentIndexChanged.connect(self.refresh_tree_widget)

        self.project_tree_viewer_wdg.itemClicked.connect(self.get_selected_entry_name)
        self.project_tree_viewer_wdg.itemClicked.connect(self.get_sel_show_branch_category)
        self.project_tree_viewer_wdg.itemClicked.connect(self.get_sel_data)
        self.project_tree_viewer_wdg.itemSelectionChanged.connect(self.get_sel_data)

        self.about_action.triggered.connect(self.about)
        self.create_show_action.triggered.connect(self.create_show_menu)
        self.create_show_branch_action.triggered.connect(self.create_show_branches_menu)

        self.create_seq_action.triggered.connect(self.create_seq_menu)
        self.create_shot_action.triggered.connect(self.create_shot_menu)
        self.create_asset_action.triggered.connect(self.create_asset_menu)
        self.create_asset_category_action.triggered.connect(self.create_asset_category_menu)
        self.save_task_schema_action.triggered.connect(self.task_manager_menu)
        self.assignment_manager_action.triggered.connect(self.assignment_manager_menu)
        self.remove_entry_action.triggered.connect(self.remove_entry_menu)

    def get_shows(self):
        """Returns a list of all shows in the database"""
        get_all_shows = DbProject().get_all()
        return sorted(get_all_shows)

    def refresh_shows(self):
        """Refreshes the combobox with the current shows in the database"""
        store = []
        current_selected_show = self.curr_sel_show()
        get_versions = DbProject().get_all()

        for show in get_versions:
            store.append(show)
        self.show_select_cb.clear()
        self.show_select_cb.addItems(store)
        self.show_select_cb.setCurrentText(current_selected_show)

        return sorted(store)

    def curr_sel_show(self):
        """Returns the current selected show in the combobox"""
        text = self.show_select_cb.currentText()
        Envars.show_name = text
        return text

    def populate_shows_cb(self):
        self.show_select_cb.addItems(self.get_shows())

    def set_show_to(self):
        """Sets the show to the current show in the combobox"""
        self.show_select_cb.setCurrentText(self.show_name)

    def refresh_tree_widget(self):
        """Refreshes the tree widget with the current show selected in the combobox"""
        try:
            self.project_tree_viewer_wdg.clear()
            get_branches = DbProjectBranch.get_branches()
            for branch in sorted(get_branches):
                item = self.show_tree_create_item(branch)
                self.project_tree_viewer_wdg.addTopLevelItem(item)
            self.project_tree_viewer_wdg.expandAll()
        except:
            print ("Something wrong in refresh_tree_widget")

    def show_tree_create_item(self, name):
        """Creates a tree widget item with the name passed in"""
        iso_name = self.get_entry_name_from_id(name)
        item = QtWidgets.QTreeWidgetItem([iso_name])
        self.add_children(item)
        return item

    def get_entry_name_from_id(self, name: str, delimiter=".") -> str:
        """Returns the last item in a string separated by a delimiter"""
        if delimiter not in name:
            return name
        isolate_last = name.split(delimiter)[-1]
        return isolate_last

    def add_children(self, item):
        """Adds children to the tree widget item passed in"""
        get_children = gdeepval.deep_values(item.text(0), self.get_show_structure())
        for children in get_children:
            for child in sorted(children):
                if child != "type":
                    child_item = self.show_tree_create_item(child)
                    item.addChild(child_item)

    def get_show_structure(self):
        """Returns the structure of the show selected in the combobox"""
        try:
            entity = DbProject.get_structure()
            return entity
        except:
            print ("shit Happened!! in GET_SHOW_STRUCTURE_FUNC")

    def get_selected_show(self):
        return self.show_select_cb.currentText()

    def get_selected(self):
        selected = self.project_tree_viewer_wdg.selectedItems()
        return selected

    def get_selected_entry(self):
        names = []
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text(0))
            return names[0]

    def get_sel_show_branch_category(self):
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                try:
                    parent = item.parent()
                    grand_parent = parent.parent()
                    return grand_parent.text(0)
                except:
                    pass

    def get_sel_show_branch(self):
        """Returns the branch of the selected item in the tree widget"""
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                try:
                    parent = item.parent()
                    grand_parent = parent.parent()
                    return grand_parent.text(0)
                except:
                    pass

    def get_parent(self):
        """Returns the parent of the selected item in the tree widget"""
        get_selected_objects = self.project_tree_viewer_wdg.currentItem()
        parent = get_selected_objects.parent()
        if parent:
            return parent.text(0)

    def get_grandparent(self):
        """Returns the grandparent of the selected item in the tree widget"""
        get_selected_objects = self.project_tree_viewer_wdg.currentItem()
        parent = get_selected_objects.parent()
        try:
            grandparent = parent.parent()
            return grandparent.text(0)
        except:
            pass

    def get_sel_data(self):
        """Returns the selected data in the tree widget"""
        branch = list()
        branch_type = str()
        category = list()
        entry = list()

        get_selected_objects = self.project_tree_viewer_wdg.currentItem()
        get_selected_show = self.curr_sel_show()

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

    def get_selected_entry_name(self):
        """Returns the name of the current selection"""
        names = []
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text(0))
            return names[0]

    def get_sel_parent(self):
        """Returns the parent of the current selection"""
        get_selected_entry_objects = self.project_tree_viewer_wdg.selectedItems()
        if len(get_selected_entry_objects) == 0:
            return []
        elif len(get_selected_entry_objects) >= 1:
            for item in get_selected_entry_objects:
                try:
                    parent = item.parent()
                    return parent.text(0)
                except:
                    return []

    def get_selection_type(self):
        """Returns the type of the current selection"""
        curr_selected_items = self.project_tree_viewer_wdg.selectedItems()
        if curr_selected_items:
            curr_sel_type = DbProjectBranch().get_current_branch_type
            return curr_sel_type

    def context_menu(self):
        """Creates the context menu for the project tree viewer"""
        self.project_tree_viewer_wdg.customContextMenuRequested.connect(self.show_tree_con_menu)

    def show_tree_con_menu(self, point):
        """Shows the context menu for the project tree viewer"""
        self.get_sel_data()

        context_menu = QtWidgets.QMenu()
        context_parent = self.get_sel_parent()
        selected = self.get_selected_entry_name()

        sel_type = self.get_selection_type()

        if selected == []:
            context_menu.addAction(self.create_show_action)
            context_menu.addAction(self.create_show_branch_action)
            context_menu.exec_(self.mapToGlobal(point))

        elif selected == Envars.branch_name and sel_type == "shots":
            context_menu.addAction(self.create_seq_action)
            context_menu.exec_(self.mapToGlobal(point))

        elif context_parent == Envars.branch_name and sel_type == "shots":
            context_menu.addAction(self.create_shot_action)
            context_menu.exec_(self.mapToGlobal(point))

        elif context_parent == Envars.branch_name and sel_type == "build":
            context_menu.addAction(self.create_asset_action)
            context_menu.exec_(self.mapToGlobal(point))

        elif selected == Envars.branch_name and sel_type == "build":
            context_menu.addAction(self.create_asset_category_action)
            context_menu.exec_(self.mapToGlobal(point))

        else:
            context_menu.addAction(self.edit_entry_definition)
            context_menu.addAction(self.edit_bundle)
            context_menu.addSeparator()
            context_menu.addAction(self.save_task_schema_action)
            context_menu.addAction(self.assignment_manager_action)

            context_menu.addSeparator()
            context_menu.addAction(self.remove_entry_action)
            context_menu.exec_(self.mapToGlobal(point))

    def create_show_actions(self):
        """Create actions for the context menu."""
        self.about_action = QtWidgets.QAction("About", self)
        self.create_show_action = QtWidgets.QAction("Create Show...", self)
        self.create_show_branch_action = QtWidgets.QAction("Create Show Branch...", self)
        self.create_seq_action = QtWidgets.QAction("Create Seq...", self)
        self.create_shot_action = QtWidgets.QAction("Create Shot...", self)
        self.create_asset_action = QtWidgets.QAction("Create Asset...", self)
        self.create_asset_category_action = QtWidgets.QAction("Create Asset Category...", self)
        self.remove_entry_action = QtWidgets.QAction("Remove Entry...", self)
        self.edit_entry_definition = QtWidgets.QAction("Edit Definition...", self)
        self.save_task_schema_action = QtWidgets.QAction("Task Manager...", self)
        self.assignment_manager_action = QtWidgets.QAction("Assignment Manager...", self)
        self.edit_bundle = QtWidgets.QAction("Edit Bundle...", self)

    def about(self):
        QtWidgets.QMessageBox.about(self, "About Simple Stuff", "Add About Text Here")

    def remove_entry_menu(self):
        """Remove entry from the database."""
        custom_dialog = QtWidgets.QMessageBox()
        custom_dialog.setText("Operation is not undoable!")
        custom_dialog.setInformativeText("Do you want to continue?")
        custom_dialog.setStandardButtons(custom_dialog.Yes | custom_dialog.Cancel)
        custom_dialog.setDefaultButton(custom_dialog.Save)
        btn_pressed = custom_dialog.exec_()

        if btn_pressed == custom_dialog.Yes:
            xac.remove_entry(self.show_select_cb.currentText(),
                             self.get_sel_show_branch(),
                             self.get_sel_category(),
                             self.get_selected_entry_name())
            self.refresh_tree_widget()
        else:
            custom_dialog.close()

    def create_show_menu(self):
        """Create show menu."""
        self.ui = create_show_ui.CreateShowUI()
        self.ui.show()

    def create_show_branches_menu(self):
        """Create show branches menu."""
        self.ui = create_branch_ui.CreateShowBranchUI()
        self.ui.show_name_cb.setDisabled(True)
        self.ui.show()

    def create_seq_menu(self):
        """Create seq menu."""
        self.ui = create_seq_ui.CreateSeqUI()
        self.ui.show()

    def create_shot_menu(self):
        """Create shot menu."""
        self.ui = create_shot_ui.CreateShotUI()
        self.ui.show()

    def create_asset_menu(self):
        """Create asset menu."""
        self.ui = create_asset_ui.CreateAssetUI()
        self.ui.show()

    def create_asset_category_menu(self):
        """Create asset category menu."""
        self.ui = create_asset_category_ui.CreateAssetCategoryUI()
        self.ui.show_name_cb.setCurrentText(self.show_select_cb.currentText())
        self.ui.show_name_cb.setDisabled(True)
        self.ui.show()

    def task_manager_menu(self):
        """Task manager menu."""
        self.ui = task_manager_core.TaskManagerMainUI()
        self.ui.show()

    def assignment_manager_menu(self):
        """Assignment manager menu."""
        self.ui = assignment_manager_core.AssignmentManagerMainUI()
        self.ui.show()

if __name__ == '__main__':
    import sys
    # from envars.envars import Envars
    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    # Envars.show_name = "Test"
    # Envars.branch_name = "sequences"
    # Envars.category = "GooGoo"
    # Envars.entry_name = "circle"
    # Envars.task_name = "rigging"

    test_dialog = ProjectTreeViewerCore()

    # test_dialog.current_show()
    # test_dialog.comboBox_shows()
    # test_dialog.set_show_to()
    test_dialog.show()
    sys.exit(app.exec_())