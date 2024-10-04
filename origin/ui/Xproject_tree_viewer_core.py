from PySide2 import QtWidgets, QtGui, QtCore

from origin.envars.Xorigin_envars import ContextHandler
from origin.ui.Xproject_tree_viewer_UI import ProjectTreeViewerUI
from o_database.entities.Xoperators import get_entity_class, Group, Project, Projects

from origin.ui import odb_task_manager_core, Xcreate_asset_ui, Xcreate_show_ui, Xcreate_group_ui, \
    assignment_manager_core


class ProjectTreeViewerCore(ProjectTreeViewerUI):
    entity_selection = QtCore.Signal(object)
    project_selection = QtCore.Signal(object)
    current_context = QtCore.Signal(object)

    def __init__(self, has_project_select_wdg=True, has_context_menu=True, has_create_new_proj=True, parent=None):
        super(ProjectTreeViewerCore, self).__init__(parent)

        ########################################################
        # Class attributes
        ########################################################
        self.context_handler = ContextHandler()

        self.has_project_select_wdg = has_project_select_wdg
        self.has_context_menu = has_context_menu
        self.has_create_new_proj = has_create_new_proj

        if not self.has_project_select_wdg:
            self.show_select_cb.setEnabled(False)
            self.show_select_cb.setVisible(False)

        if not self.has_create_new_proj:
            self.create_project_btn.setEnabled(False)
            self.create_project_btn.setVisible(False)

        if self.has_context_menu:
            self.context_actions()
            self.context_menu()
            self.create_context_menu_connections()

        self.populate_shows_cb()
        self.refresh_tree_widget()

        ########################################################
        # Connect signals
        ########################################################
        self.create_project_btn.clicked.connect(self.create_show_menu)

        self.show_select_cb.currentIndexChanged.connect(self.curr_sel_show)
        self.show_select_cb.currentIndexChanged.connect(self.get_current_index_data)
        self.show_select_cb.currentIndexChanged.connect(self.refresh_tree_widget)

        self.project_tree_viewer_wdg.itemClicked.connect(self.get_selected_entry_name)
        self.project_tree_viewer_wdg.itemClicked.connect(self.resolve_context)
        self.project_tree_viewer_wdg.itemSelectionChanged.connect(self.resolve_context)
        self.project_tree_viewer_wdg.itemExpanded.connect(self.on_item_expanded)

        # self.about_action.triggered.connect(self.about)

    def create_context_menu_connections(self):
        self.create_group_action.triggered.connect(self.create_group_menu)
        self.create_asset_action.triggered.connect(self.create_asset_menu)
        self.save_task_schema_action.triggered.connect(self.task_manager_menu)
        self.assignment_manager_action.triggered.connect(self.assignment_manager_menu)
        self.remove_selected_action.triggered.connect(self.remove_selected_menu)

    def get_shows(self):
        """Returns a list of all shows in the database"""
        get_all_shows = Projects().names()
        if get_all_shows is None:
            return

        all_shows = [Project(**show) for show in get_all_shows]
        return all_shows

    def refresh_shows(self):
        """Refreshes the combobox with the current shows in the database"""
        store = []
        current_selected_show, current_data = self.curr_sel_show()
        self.show_select_cb.clear()
        self.populate_shows_cb()
        self.show_select_cb.setCurrentText(current_selected_show)

    def curr_sel_show(self):
        """Returns the current selected show in the combobox"""
        text = self.show_select_cb.currentText()
        data = self.get_current_index_data()
        self.context_handler.show_name = text

        return text, data

    def populate_shows_cb(self):
        get_shows = self.get_shows()
        cnt = 0
        for show in get_shows:
            self.show_select_cb.addItem(show.name)
            self.show_select_cb.setItemData(cnt, show, role=QtCore.Qt.UserRole)
            cnt += 1

    def set_show_to(self):
        """Sets the show to the current show in the combobox"""
        self.show_select_cb.setCurrentText(self.show_name)

    def get_current_index_data(self):
        curr_index = self.show_select_cb.currentIndex()
        if curr_index is not None:
            user_data = self.show_select_cb.itemData(curr_index, role=QtCore.Qt.UserRole)
            return user_data

    def refresh_tree_widget(self):
        """Refreshes the tree widget with the current show selected in the combobox"""
        self.project_tree_viewer_wdg.clear()
        curr_proj_data = self.get_current_index_data()
        if curr_proj_data:
            get_branches = curr_proj_data.get_children()

            if get_branches:
                for branch in get_branches:
                    asset = Group(**branch)
                    doc_visual_children = asset.children

                    item = QtWidgets.QTreeWidgetItem([asset.name])
                    item.setData(0, QtCore.Qt.UserRole, asset)

                    if len(doc_visual_children) != 0:
                        item.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)
                    self.project_tree_viewer_wdg.addTopLevelItem(item)

    def on_item_expanded(self, item):
        if item.childCount() == 0:
            parent_doc_data = item.data(0, QtCore.Qt.UserRole)
            children_docs = parent_doc_data.get_children()

            for child_doc in children_docs:
                if child_doc["type"] != "task":
                    check_type = get_entity_class(child_doc["type"])
                    asset = check_type(**child_doc)
                    doc_visual_children = asset.children
                    child_item = QtWidgets.QTreeWidgetItem([asset.name])
                    child_item.setData(0, QtCore.Qt.UserRole, asset)

                    if len(doc_visual_children) != 0:
                        child_item.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)
                    item.addChild(child_item)

    def get_selected_item(self):
        selected = self.project_tree_viewer_wdg.selectedItems()
        if selected:
            return selected[0]

    def get_selected(self):
        selected = self.project_tree_viewer_wdg.selectedItems()
        return selected

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
        current_selection = self.get_selected_item()
        if not current_selection:
            return

        group_selection = []

        sel_data = current_selection.data(0, QtCore.Qt.UserRole)
        get_sel_type = sel_data.type

        if get_sel_type == "group":
            sel_id = sel_data.id
            orig_path = sel_id.split(".", 1)[1]
            group_selection.clear()
            group_selection.append(orig_path)
        elif get_sel_type == "asset":
            sel_id = sel_data.id
            exclude_project = sel_id.split(".", 1)[1]
            exclude_asset = exclude_project.rsplit(".", 1)[0]
            group_selection.clear()
            group_selection.append(exclude_asset)
        proj_data = self.get_current_index_data()

        self.context_handler.show_name = proj_data.name
        if len(group_selection) != 0:
            self.context_handler.origin_path_hierarchy = group_selection[0]
        self.context_handler.entity_name = sel_data.name
        self.context_handler.entity_type = sel_data.type
        self.context_handler.entity_id = sel_data.id
        context_snapshot = self.context_handler.snapshot_session()

        self.current_context.emit(context_snapshot)

    def context_menu_build(self, point):
        """Shows the context menu for the project tree viewer"""
        self.resolve_context()

        context_menu = QtWidgets.QMenu()
        context_menu.addAction(self.create_group_action)
        current_selection = self.get_selected()

        if len(current_selection) != 0:
            context_menu.addAction(self.create_asset_action)
            context_menu.addAction(self.edit_entry_definition)
            context_menu.addSeparator()
            context_menu.addAction(self.save_task_schema_action)
            context_menu.addAction(self.assignment_manager_action)
            context_menu.addSeparator()
            context_menu.addAction(self.remove_selected_action)

        context_menu.exec_(self.mapToGlobal(point))

    def resolve_parent_id(self):
        current_selection = self.get_selected_item()
        if current_selection:
            sel_doc_data = current_selection.data(0, QtCore.Qt.UserRole)
            if sel_doc_data.type == "group":
                doc_id = sel_doc_data.id
                return doc_id
            else:
                doc_id = sel_doc_data.parent
                return doc_id
        else:
            doc_id = None
            return doc_id

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

    def remove_selected_menu(self):
        """Remove entry from the database."""
        custom_dialog = QtWidgets.QMessageBox()
        custom_dialog.setText("Operation is not undoable!")
        custom_dialog.setInformativeText("Do you want to continue?")
        custom_dialog.setStandardButtons(custom_dialog.Yes | custom_dialog.Cancel)
        custom_dialog.setDefaultButton(custom_dialog.Save)
        btn_pressed = custom_dialog.exec_()

    def create_show_menu(self):
        """Create show menu."""
        self.ui = Xcreate_show_ui.CreateShowUI()
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.refresh_shows)
        self.ui.create_and_close_btn.clicked.connect(self.refresh_shows)

    def create_group_menu(self):
        """Create group menu."""
        doc_id = self.resolve_parent_id()
        context = self.context_handler.snapshot_session()
        self.ui = Xcreate_group_ui.CreateGroupUI(context=context, group_parent=doc_id)
        self.ui.show()
        self.ui.create_btn.clicked.connect(self.refresh_tree_widget)
        self.ui.create_and_close_btn.clicked.connect(self.refresh_tree_widget)

    def create_asset_menu(self):
        """Create asset menu."""
        doc_id = self.resolve_parent_id()
        context = self.context_handler.snapshot_session()
        self.ui = Xcreate_asset_ui.CreateAssetUI(context=context, asset_parent=doc_id)
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

    test_dialog = ProjectTreeViewerCore()
    # test_dialog.isolate_to_context(asset_id)
    test_dialog.show()
    sys.exit(app.exec_())
