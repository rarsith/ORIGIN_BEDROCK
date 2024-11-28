from typing import List

from PySide2 import QtWidgets, QtGui, QtCore

from origin.database.mongo import CollectionOperators
from origin.envars.origin_envars import ContextHandler
from origin.ui.project_tree_viewer_core import ProjectTreeViewerCore
from origin.ui.task_viewer_core import TaskViewerCore
from origin.database.entities.registries import registry


class VersionButton(QtWidgets.QPushButton):
    def __init__(self, label, data, parent=None):
        super().__init__(label, parent)
        self.data = data


class ScrollableButtonArea(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)  # Hide vertical scroll bar
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setMinimumWidth(55)
        self.setMaximumWidth(55)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.setExclusive(True)

        self.button_container = QtWidgets.QVBoxLayout()
        self.button_container.addStretch(1)

        container_widget = QtWidgets.QWidget()
        container_widget.setLayout(self.button_container)

        self.setWidget(container_widget)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def wheelEvent(self, event):
        self.verticalScrollBar().setValue(self.verticalScrollBar().value() - event.angleDelta().y() // 2)

    def add_button(self, button):
        button.setCheckable(True)
        button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.button_group.addButton(button)
        self.button_container.insertWidget(self.button_container.count() - 1, button)


class VersionLoaderContextMenuWidget(QtWidgets.QWidget):
    def __init__(self, main_widget,  parent=None):
        super(VersionLoaderContextMenuWidget, self).__init__(parent)

        self.main_widget = main_widget

        self.context_actions()
        self.context_menu()
        # self.create_context_menu_connections()

    #     self.create_widgets()
    #     self.create_layout()
    #     self.create_connections()
    #
    # def create_widgets(self):
    #     pass
    #
    # def create_layout(self):
    #     pass
    #
    # def create_connections(self):
    #     pass

    def context_menu(self):
        """Creates the context menu for the project tree viewer"""
        self.main_widget.customContextMenuRequested.connect(self.context_menu_build)

    def context_actions(self):
        """Create actions for the context menu."""
        self.about_action = QtWidgets.QAction("About", self)
        self.create_group_action = QtWidgets.QAction("Create Group...", self)
        self.create_asset_action = QtWidgets.QAction("Create Asset...", self)
        self.remove_selected_action = QtWidgets.QAction("Remove Selection...", self)
        self.edit_entry_definition = QtWidgets.QAction("Edit Definition...", self)
        self.save_task_schema_action = QtWidgets.QAction("Task Manager...", self)
        self.assignment_manager_action = QtWidgets.QAction("Assignment Manager...", self)

    def create_context_menu_connections(self):
        pass
        # self.create_group_action.triggered.connect(self.create_group_menu)
        # self.create_asset_action.triggered.connect(self.create_asset_menu)
        # self.save_task_schema_action.triggered.connect(self.task_manager_menu)
        # self.assignment_manager_action.triggered.connect(self.assignment_manager_menu)
        # self.remove_selected_action.triggered.connect(self.remove_selected_menu)


    def context_menu_build(self, point):
        """Shows the context menu for the project tree viewer"""

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


class VersionLoaderWidget(QtWidgets.QWidget):
    def __init__(self, context: ContextHandler = None, db_asset_data=None, parent=None):
        super(VersionLoaderWidget, self).__init__(parent)

        self.context_handler = context
        self.db_asset_data = db_asset_data

        self.setFixedSize(300, 150)

    # create_widgets
        self.db_asset_name_lb = QtWidgets.QLabel()
        self.db_asset_name_lb.setText(self.get_db_asset())
        self.thumbnail = QtWidgets.QLabel(self)
        self.thumbnail.setStyleSheet("background-color: gray;")
        self.thumbnail.setAlignment(QtCore.Qt.AlignCenter)
        self.thumbnail.setText("Thumbnail")



    # create_layout
        existing_versions = self.get_existing_versions()
        self.scrollable_buttons = ScrollableButtonArea()

        for version in existing_versions:
            self.scrollable_buttons.add_button(version)

        first_button = existing_versions[0]
        first_button.setChecked(True)

        mid_layout = QtWidgets.QHBoxLayout()
        mid_layout.addWidget(self.thumbnail)
        mid_layout.addWidget(self.scrollable_buttons)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.db_asset_name_lb)
        main_layout.addLayout(mid_layout)

        self.context_menu = VersionLoaderContextMenuWidget(main_widget=self.scrollable_buttons)
    # create_connections
        ...

    def get_db_asset(self):
        db_asset_name = list(self.db_asset_data.keys())[0]
        name_elements = db_asset_name.split(".")
        wdg_name = "__".join(name_elements[-3:])
        return wdg_name

    def get_existing_versions(self):
        sel_ver_btns = []
        for db_asset_ids in self.db_asset_data:
            db_asset_versions = self.db_asset_data[db_asset_ids]
            for db_version in reversed(db_asset_versions):
                version_cnt = db_version.rsplit(".", 1)[1]
                ver_sel_btn = VersionButton(version_cnt, data={db_version})
                ver_sel_btn.clicked.connect(self.get_button_data)
                sel_ver_btns.append(ver_sel_btn)

        return sel_ver_btns

    def get_button_data(self):
        button = self.sender()
        print(button.data)

    def get_thumbnail(self):
        pass


class AssetTypesButtonsSelectors(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AssetTypesButtonsSelectors, self).__init__(parent)

        self.type_sel_btn = None
        self.db_asset_type = registry.get_all_types()

        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        exceptions = ["asset_stack_breakdown", "asset_stack", "shot_stack", "shot_stack_breakdown"]
        for db_type in self.db_asset_type:
            if db_type not in exceptions:
                select_db_asset_type = QtWidgets.QPushButton(db_type.capitalize())
                select_db_asset_type.setFixedSize(120, 20)
                self.main_layout.addWidget(select_db_asset_type)

    def create_layout(self):
        pass

    def create_connections(self):
        pass


class VersionLoader(QtWidgets.QWidget):
    def __init__(self, context: ContextHandler = None, parent=None):
        super(VersionLoader, self).__init__(parent)

        self.context_handler = context

        self.version_loader_sra = None
        self.container = None
        self.grid_layout = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.version_loader_sra = QtWidgets.QScrollArea()
        self.version_loader_sra.setWidgetResizable(True)
        self.version_loader_sra.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.container = QtWidgets.QWidget()
        self.version_loader_sra.setWidget(self.container)

    def create_layout(self):
        self.grid_layout = QtWidgets.QGridLayout(self.container)
        self.grid_layout.setSpacing(5)
        self.grid_layout.setAlignment(QtCore.Qt.AlignTop)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.version_loader_sra)

    def create_connections(self):
        pass

    def resolve_extra_filters(self, default_filter: List[dict] = None, filters_input: List[dict] = None):
        extra_filters = default_filter
        if filters_input:
            for extra_filter in filters_input:
                extra_filters.append(extra_filter)
        return extra_filters

    def get_existing_db_assets(self):
        extra_filters = self.resolve_extra_filters(default_filter=[{"db_asset_type": "db_asset"}])
        publishes_docs = None

        if self.context_handler.task_id is not None:
            extra_filters = self.resolve_extra_filters(default_filter=[{"db_asset_type": "db_asset",
                                                                        "master_task_type": self.context_handler.task_type}])
        if self.context_handler.entity_name is not None:
            fetch_ent = CollectionOperators(db_collection=self.context_handler.project_publishes)
            publishes_docs = fetch_ent.entities_attr_value_starts_with(attr_field="_id",
                                                                       val_starts_with=self.context_handler.resolve_to_base_context(),
                                                                       extra_filters=extra_filters,
                                                                       ids_only=True
                                                                       )

        return publishes_docs

    def get_db_data(self):
        db_assets_ids = self.get_existing_db_assets()
        db_data = []

        doc_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        for db_asset_id in db_assets_ids:
            db_asset_doc = doc_ops.entity_document(doc_id=db_asset_id["_id"])
            compiled_data = {db_asset_doc["_id"]: db_asset_doc["children"]}
            db_data.append(compiled_data)

        return db_data

    def clear_versions_wdg(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().deleteLater()

    def populate_versions(self):
        self.clear_versions_wdg()
        db_data = self.get_db_data()

        for idx, db_asset in enumerate(db_data):
            db_asset_widget = VersionLoaderWidget(context=self.context_handler,
                                                  db_asset_data=db_asset)
            self.grid_layout.addWidget(db_asset_widget, idx // 2, idx % 2)


class Loader(QtWidgets.QWidget):
    def __init__(self, context: ContextHandler = None, parent=None):
        super(Loader, self).__init__(parent)

        self.project_tree_viewer = None
        self.task_viewer = None
        self.db_asset_type_btn = None
        self.db_asset_versions_wdg = None
        self.context_menu = None

        self.context_handler = context

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.project_tree_viewer = ProjectTreeViewerCore(has_project_select_wdg=True,
                                                         has_create_new_proj=False,
                                                         has_context_menu=False)

        self.project_tree_viewer.set_show_to(self.context_handler.show_name)

        self.task_viewer = TaskViewerCore()
        self.task_viewer.populate_widget()
        self.task_viewer_overrides()

        self.db_asset_type_btn = AssetTypesButtonsSelectors()

        self.db_asset_versions_wdg = VersionLoader(context=self.context_handler)
        self.db_asset_versions_wdg.populate_versions()

        self.context_menu = VersionLoaderContextMenuWidget(main_widget=self.db_asset_versions_wdg)

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.project_tree_viewer)
        main_layout.addWidget(self.task_viewer)
        main_layout.addWidget(self.db_asset_type_btn)
        main_layout.addWidget(self.db_asset_versions_wdg)

        vertical_splitter = QtWidgets.QSplitter()
        vertical_splitter.setOrientation(QtCore.Qt.Horizontal)
        main_layout.addWidget(vertical_splitter)

        vertical_splitter.insertWidget(0, self.project_tree_viewer)
        vertical_splitter.insertWidget(1, self.task_viewer)
        vertical_splitter.insertWidget(2, self.db_asset_type_btn)
        vertical_splitter.insertWidget(3, self.db_asset_versions_wdg)
        vertical_splitter.setSizes([200, 250, 40, 850])

    def create_connections(self):
        self.project_tree_viewer.current_context.connect(self.task_viewer.context_receiver)
        self.project_tree_viewer.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_task_viewer)
        self.project_tree_viewer.project_tree_viewer_wdg.itemClicked.connect(self.populate_task_viewer)

    def populate_task_viewer(self):
        has_selection = self.project_tree_viewer.get_selected()
        if len(has_selection) != 0:
            self.task_viewer.populate_widget()
        else:
            self.project_tree_viewer.project_tree_viewer_wdg.clearSelection()
            self.task_viewer.task_viewer_wdg.clear()

    def task_viewer_overrides(self):
        self.task_viewer.task_viewer_wdg.setObjectName("Task Viewer Override")
        self.task_viewer.task_viewer_wdg.setColumnHidden(10, True)
        self.task_viewer.task_viewer_wdg.setColumnHidden(9, True)
        self.task_viewer.task_viewer_wdg.setColumnHidden(8, True)
        self.task_viewer.task_viewer_wdg.setColumnHidden(7, True)
        self.task_viewer.task_viewer_wdg.setColumnHidden(6, True)
        self.task_viewer.task_viewer_wdg.setColumnHidden(5, True)
        self.task_viewer.task_viewer_wdg.setColumnHidden(4, True)
        self.task_viewer.task_viewer_wdg.setColumnHidden(3, True)
        self.task_viewer.task_viewer_wdg.setColumnHidden(2, True)
        self.task_viewer.add_btn.setEnabled(False)
        self.task_viewer.add_btn.setVisible(False)
        self.task_viewer.save_changes_btn.setVisible(False)
        self.task_viewer.save_changes_btn.setVisible(False)
        self.task_viewer.export_btn.setVisible(False)
        self.task_viewer.export_btn.setVisible(False)
        self.task_viewer.refresh_btn.setVisible(False)
        self.task_viewer.refresh_btn.setVisible(False)


class LoaderMainUI(QtWidgets.QMainWindow):
    def __init__(self, context: ContextHandler = None, parent=None):
        super(LoaderMainUI, self).__init__(parent)

        self.setMinimumHeight(850)
        self.setMinimumWidth(1500)
        self.central_widget = Loader(context=context)

        self.setWindowTitle(f"Assets Loader")

        self.setCentralWidget(self.central_widget)
        self.show()


if __name__ == "__main__":
    import sys

    qss_style_file = "C:\\Users\\arsithra\\PycharmProjects\\ORIGIN_BEDROCK\\origin\\ui\\style\\stylesheets\\dark_orange\\dark_orange_style.qss"

    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'tafer', }
    # 'db_asset_id': 'The_Rock.assets.chr.tafer.geometry.tafer',
    # 'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer',
    # 'entity_type': 'asset',
    # 'entity_id': 'The_Rock.assets.chr.tafer',
    # 'task_name': "modeling",
    # 'task_type': "modeling",
    # 'task_id': "The_Rock.assets.chr.tafer.modeling"}

    context_obj = ContextHandler()
    context_obj.load_session(session_data=context_sample)

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = LoaderMainUI(context=context_obj)

    with open(qss_style_file, "r") as f:
        _style = f.read()
        test_dialog.setStyleSheet(_style)

    # test_dialog.populate_widget()
    test_dialog.show()
    sys.exit(app.exec_())
