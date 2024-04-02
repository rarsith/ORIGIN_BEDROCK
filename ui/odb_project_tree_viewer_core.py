from PySide2 import QtWidgets, QtGui, QtCore
from envars.origin_envars import OriginEnvar
from ui.odb_project_tree_viewer_UI import ProjectTreeViewerUI
from o_database.entities.actions import Query, Fetch
from ui import odb_create_asset_ui, odb_task_manager_core, assignment_manager_core, odb_create_show_ui, odb_create_group_ui


class ProjectTreeViewerCore(ProjectTreeViewerUI):
    selection_data = QtCore.Signal(dict)

    def __init__(self, parent=None):
        super(ProjectTreeViewerCore, self).__init__(parent)

        self.context_actions()
        self.create_connections()
        self.populate_shows_cb()
        self.refresh_tree_widget()
        self.context_menu()

    def create_connections(self):
        """Creates all the connections for the UI"""
        self.create_project_btn.clicked.connect(self.create_show_menu)

        self.show_select_cb.currentIndexChanged.connect(self.curr_sel_show)
        self.show_select_cb.currentIndexChanged.connect(self.refresh_tree_widget)

        self.project_tree_viewer_wdg.itemClicked.connect(self.get_selected_entry_name)
        self.project_tree_viewer_wdg.itemClicked.connect(self.resolve_context)
        self.project_tree_viewer_wdg.itemSelectionChanged.connect(self.resolve_context)
        self.project_tree_viewer_wdg.itemExpanded.connect(self.on_item_expanded)

        self.about_action.triggered.connect(self.about)

        self.create_group_action.triggered.connect(self.create_group_menu)
        self.create_asset_action.triggered.connect(self.create_asset_menu)
        self.save_task_schema_action.triggered.connect(self.task_manager_menu)
        self.assignment_manager_action.triggered.connect(self.assignment_manager_menu)
        self.remove_selected_action.triggered.connect(self.remove_selected_menu)

    def get_shows(self):
        """Returns a list of all shows in the database"""
        get_all_shows = Query().projects().names()
        return sorted(get_all_shows)

    def refresh_shows(self):
        """Refreshes the combobox with the current shows in the database"""
        store = []
        current_selected_show = self.curr_sel_show()
        get_projects = self.get_shows()

        for show in get_projects:
            store.append(show)
        self.show_select_cb.clear()
        self.show_select_cb.addItems(store)
        self.show_select_cb.setCurrentText(current_selected_show)

        return sorted(store)

    def curr_sel_show(self):
        """Returns the current selected show in the combobox"""
        text = self.show_select_cb.currentText()
        # project = Project(name=text).select()
        OriginEnvar.show_name = text
        OriginEnvar.project_publishes = "__".join([text, "PUBLISHES"])
        OriginEnvar.project_work = "__".join([text, "WORK"])
        OriginEnvar.project_control = "__".join([text, "CONTROL"])

        return text

    def populate_shows_cb(self):
        self.show_select_cb.addItems(self.get_shows())

    def set_show_to(self):
        """Sets the show to the current show in the combobox"""
        self.show_select_cb.setCurrentText(self.show_name)

    def refresh_tree_widget(self):
        """Refreshes the tree widget with the current show selected in the combobox"""

        self.project_tree_viewer_wdg.clear()
        get_branches = Fetch().structure_entities().project_root_children()

        if get_branches:
            for branch in get_branches:
                doc_name = branch["entry_name"]
                doc_id = branch["_id"]
                doc_visual_children = branch["visual_children"]
                doc_type = branch["type"]

                item = QtWidgets.QTreeWidgetItem([doc_name])
                item.setData(0, QtCore.Qt.UserRole, doc_id)
                item.setData(1, QtCore.Qt.UserRole, doc_type)

                if len(doc_visual_children) != 0:
                    item.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)
                self.project_tree_viewer_wdg.addTopLevelItem(item)

    def on_item_expanded(self, item):
        if item.childCount() == 0:
            parent_doc_id = item.data(0, QtCore.Qt.UserRole)
            children_ids = Fetch().structure_entities().entity_children_ids(parent_doc_id)

            for child_id in children_ids:
                child_full_doc = Fetch().structure_entities().entity_by_id(child_id)
                child_name = child_full_doc["entry_name"]
                child_type = child_full_doc["type"]
                doc_visual_children = child_full_doc["visual_children"]

                child_item = QtWidgets.QTreeWidgetItem([child_name])
                child_item.setData(0, QtCore.Qt.UserRole, child_id)
                child_item.setData(1, QtCore.Qt.UserRole, child_type)

                if len(doc_visual_children) != 0:
                    child_item.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)
                item.addChild(child_item)

    def get_selected(self):
        selected = self.project_tree_viewer_wdg.selectedItems()
        if selected:
            return selected[0]

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

    def resolve_context(self):
        group_items = []
        asset_items = []

        current_selection = self.get_selected()

        def get_parents(current_item):
            sel_parent = current_item.parent()
            if sel_parent:
                group_items.append(sel_parent.text(0))
                return get_parents(sel_parent)

        if current_selection:
            sel_type = current_selection.data(1, QtCore.Qt.UserRole)
            sel_id = current_selection.data(0, QtCore.Qt.UserRole)

            if sel_type == "asset":
                asset_items.append(current_selection.text(0))
                self.selection_data.emit({"sel_id": sel_id, "sel_type": sel_type})

            elif sel_type == "group":
                group_items.append(current_selection.text(0))
                asset_items.clear()

            get_parents(current_selection)

        reversed_group_list = group_items[::-1]
        OriginEnvar().origin_path_hierarchy = reversed_group_list

        if len(asset_items) != 0:
            OriginEnvar().entry_name = asset_items[0]
        else:
            OriginEnvar().entry_name = ""

    def context_menu_build(self, point):
        """Shows the context menu for the project tree viewer"""
        self.resolve_context()

        context_menu = QtWidgets.QMenu()
        context_menu.addAction(self.create_group_action)
        context_menu.addAction(self.create_asset_action)
        context_menu.addAction(self.edit_entry_definition)

        context_menu.addSeparator()
        context_menu.addAction(self.save_task_schema_action)
        context_menu.addAction(self.assignment_manager_action)

        context_menu.addSeparator()
        context_menu.addAction(self.remove_selected_action)
        context_menu.exec_(self.mapToGlobal(point))

    def context_menu(self):
        """Creates the context menu for the project tree viewer"""
        self.project_tree_viewer_wdg.customContextMenuRequested.connect(self.context_menu_build)

    def context_actions(self):
        """Create actions for the context menu."""
        self.about_action = QtWidgets.QAction("About", self)
        self.create_group_action = QtWidgets.QAction("Create Group...", self)
        self.create_asset_action = QtWidgets.QAction("Create Asset...", self)
        self.remove_selected_action = QtWidgets.QAction("Remove Selection...", self)
        self.edit_entry_definition = QtWidgets.QAction("Edit Definition...", self)
        self.save_task_schema_action = QtWidgets.QAction("Task Manager...", self)
        self.assignment_manager_action = QtWidgets.QAction("Assignment Manager...", self)
        # self.edit_bundle = QtWidgets.QAction("Edit Bundle...", self)

    def about(self):
        QtWidgets.QMessageBox.about(self, "About Simple Stuff", "Add About Text Here")

    def remove_selected_menu(self):
        """Remove entry from the database."""
        custom_dialog = QtWidgets.QMessageBox()
        custom_dialog.setText("Operation is not undoable!")
        custom_dialog.setInformativeText("Do you want to continue?")
        custom_dialog.setStandardButtons(custom_dialog.Yes | custom_dialog.Cancel)
        custom_dialog.setDefaultButton(custom_dialog.Save)
        btn_pressed = custom_dialog.exec_()

        # if btn_pressed == custom_dialog.Yes:
        #     xac.remove_entry(self.show_select_cb.currentText(),
        #                      self.get_sel_show_branch(),
        #                      self.get_sel_category(),
        #                      self.get_selected_entry_name())
        #     self.refresh_tree_widget()
        # else:
        #     custom_dialog.close()

    def create_show_menu(self):
        """Create show menu."""
        self.ui = odb_create_show_ui.CreateShowUI()
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.refresh_shows)
        self.ui.create_and_close_btn.clicked.connect(self.refresh_shows)

    def create_group_menu(self):
        """Create group menu."""
        self.ui = odb_create_group_ui.CreateGroupUI()
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.refresh_tree_widget)
        self.ui.create_and_close_btn.clicked.connect(self.refresh_tree_widget)

    def create_asset_menu(self):
        """Create asset menu."""
        self.ui = odb_create_asset_ui.CreateAssetUI()
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.refresh_tree_widget)
        self.ui.create_and_close_btn.clicked.connect(self.refresh_tree_widget)

    def task_manager_menu(self):
        """Task manager menu."""
        self.ui = odb_task_manager_core.TaskManagerMainUI()
        self.ui.show()

    def assignment_manager_menu(self):
        """Assignment manager menu."""
        self.ui = assignment_manager_core.AssignmentManagerMainUI()
        self.ui.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    OriginEnvar.show_name = "GREEN"
    test_dialog = ProjectTreeViewerCore()
    test_dialog.show()
    sys.exit(app.exec_())