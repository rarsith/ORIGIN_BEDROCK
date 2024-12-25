import os.path
from typing import List

from PySide2 import QtWidgets, QtGui, QtCore

from origin.database.mongo import CollectionOperators
from origin.envars.origin_envars import ContextHandler
from origin.ui.loaders_ui.color_settings import match_color_scheme
from origin.ui.project_tree_viewer_core import ProjectTreeViewerCore
from origin.ui.stream_viewer_UI import StreamViewerUI
from origin.ui.task_viewer_core import TaskViewerCore
from origin.database.entities.registries import registry
from origin.dcc.dispachers.loaders import get_loader_class


class VersionThumbnail(QtWidgets.QLabel):
    def __init__(self, label, parent=None):
        super().__init__(label, parent)
        self.data = None

    def set_data(self, data):
        self.data = data


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
        self.setMinimumWidth(65)
        self.setMaximumWidth(65)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.setExclusive(True)

        self.button_container = QtWidgets.QVBoxLayout()
        self.button_container.setSpacing(0)
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
        self.init_loader = None

        self.context_menu()
        self.main_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def context_menu(self):
        self.main_widget.customContextMenuRequested.connect(self.context_menu_build)

    def context_menu_build(self, point):
        sender_widget = self.sender()
        if sender_widget:
            context_menu = QtWidgets.QMenu(sender_widget)

            for file_component in sender_widget.data:
                for file_component_name, file_path in file_component.items():
                    origin_projects_root = os.getenv("ORIGIN_PROJECTS_ROOT")

                    absolute_path = file_path
                    if not os.path.isabs(file_path):
                        absolute_path = os.path.join(origin_projects_root, file_path)

                    if os.path.exists(absolute_path):
                        loader = get_loader_class("maya")
                        init_loader = loader(file_path=absolute_path)
                        file_extension, file_ops = init_loader.get_file_types_ops()

                        if file_ops:
                            for file_op in file_ops:
                                file_op_nice_name = file_op.capitalize()
                                context_import_action = QtWidgets.QAction(f"{file_op_nice_name} {file_component_name} ...", self)
                                context_import_action.setData([file_op, absolute_path])
                                context_import_action.triggered.connect(self.get_action_data)
                                context_menu.addAction(context_import_action)
                context_menu.addSeparator()

            context_menu.exec_(self.main_widget.mapToGlobal(point))

    def get_action_data(self):
        action = self.sender()
        if action:
            file_data = action.data()
            loader = get_loader_class("maya")
            init_loader = loader(file_path=file_data[1])
            init_loader.execute_file_ops(operation=file_data[0])


class VersionLoaderWidget(QtWidgets.QWidget):
    def __init__(self, context: ContextHandler = None, db_asset_data=None, parent=None):
        super(VersionLoaderWidget, self).__init__(parent)

        self.context_handler = context
        self.db_asset_data = db_asset_data
        self.db_asset_id = None
        self.db_asset_versions = None
        self.db_asset_versions_status = None
        self.db_versions_file_components = None
        self.ver_sel_btn = None

        self.process_asset_data()

        self.setFixedSize(300, 150)

        # create_widgets
        self.db_asset_name_lb = QtWidgets.QLabel()
        self.db_asset_name_lb.setText(self.get_db_asset())
        self.thumbnail = VersionThumbnail(label="Thumbnail")
        self.thumbnail.setStyleSheet("background-color: gray;")
        self.thumbnail.setAlignment(QtCore.Qt.AlignCenter)
        self.thumbnail.setText("Thumbnail")

        self.context_menu = VersionLoaderContextMenuWidget(main_widget=self.thumbnail)

    # create_layout
        existing_versions = self.get_existing_versions()
        self.scrollable_buttons = ScrollableButtonArea()

        for version in existing_versions:
            self.scrollable_buttons.add_button(version)

        first_button = existing_versions[0]
        first_button.setChecked(True)

        self.set_thumbnail_data(first_button.data)

        mid_layout = QtWidgets.QHBoxLayout()
        mid_layout.addWidget(self.thumbnail)
        mid_layout.addWidget(self.scrollable_buttons)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.db_asset_name_lb)
        main_layout.addLayout(mid_layout)


    # create_connections
        ...

    def process_asset_data(self):
        for db_asset_id, db_asset_versions in self.db_asset_data.items():
            self.db_asset_id = db_asset_id
            self.db_asset_versions = db_asset_versions

    def get_selected_button(self):
        checked_button = self.scrollable_buttons.button_group.checkedButton()
        return checked_button.data

    def get_db_asset(self):
        db_asset_name = self.db_asset_id
        name_elements = db_asset_name.split(".")
        wdg_name = "__".join(name_elements[-3:])
        return wdg_name

    def get_existing_versions(self):
        sel_ver_btns = []
        for db_asset_version, db_file_components in reversed(self.db_asset_versions.items()):
            version_cnt = db_asset_version.rsplit(".", 1)[1]
            self.ver_sel_btn = VersionButton(version_cnt, data=db_file_components["versions_components"])
            self.ver_sel_btn.setFixedSize(40, 20)
            ver_btn_color = match_color_scheme(db_file_components["status"])
            self.ver_sel_btn.setStyleSheet(ver_btn_color)
            self.ver_sel_btn.clicked.connect(self.get_button_data)
            self.ver_sel_btn.clicked.connect(lambda checked=False, data=db_file_components["versions_components"]: self.set_thumbnail_data(data))

            sel_ver_btns.append(self.ver_sel_btn)

        return sel_ver_btns

    def get_button_data(self):
        button = self.sender()
        return button.data

    def set_thumbnail_data(self, data):
        self.thumbnail.set_data(data)

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
        exceptions = ["asset_stack_breakdown",
                      "asset_stack",
                      "shot_stack",
                      "shot_stack_breakdown",
                      "db_asset_breakdown"]

        for db_type in self.db_asset_type:
            if db_type not in exceptions:
                select_db_asset_type = QtWidgets.QPushButton(db_type.capitalize())
                select_db_asset_type.setCheckable(True)
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

    def context_receiver(self, context: ContextHandler):
        self.context_handler = context
        self.populate_versions()

    def resolve_extra_filters(self, default_filter: List[dict] = None, filters_input: List[dict] = None):
        extra_filters = default_filter
        if filters_input:
            for extra_filter in filters_input:
                extra_filters.append(extra_filter)
        return extra_filters

    def get_existing_db_assets(self):
        q_filters = [{"db_asset_type": "db_asset"},
                     {"parent": self.context_handler.db_asset_stream_id},
                     {"master_task_type": self.context_handler.task_type}]

        resolved_filters = [{key: value for key, value in q_filter.items() if value is not None}
                            for q_filter in q_filters
                            ]

        if self.context_handler.entity_name is not None:
            fetch_ent = CollectionOperators(db_collection=self.context_handler.project_publishes)
            publishes_docs = fetch_ent.entities_attr_value_starts_with(attr_field="_id",
                                                                       val_starts_with=self.context_handler.resolve_to_base_context(),
                                                                       extra_filters=resolved_filters,
                                                                       ids_only=True
                                                                       )

        return publishes_docs

    def get_asset_breakdown_data(self):
        pass


    def get_db_data(self):
        if not self.context_handler.entity_type == "group":
            db_assets_ids = self.get_existing_db_assets()
            db_data = []

            doc_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
            for db_asset_id in db_assets_ids:
                db_asset_doc = doc_ops.entity_document(doc_id=db_asset_id["_id"])
                versions = {}
                for db_version_id in db_asset_doc["children"]:
                    db_version_doc = doc_ops.entity_document(doc_id=db_version_id)
                    db_file_components = doc_ops.children_with_parent_id(parent_id=db_version_id)
                    file_components = []
                    for db_file_component in db_file_components:
                        file_components.append({db_file_component["label"]: db_file_component["file_path"]})

                    versions[db_version_id] = {"versions_components":file_components, "status": db_version_doc["status"]}
                db_data.append({db_asset_id["_id"]: versions})

            return db_data
        else:
            return None

    def clear_versions_wdg(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().deleteLater()

    def populate_versions(self):
        self.clear_versions_wdg()
        db_data = self.get_db_data()

        if db_data is not None:
            for idx, db_asset in enumerate(db_data):
                db_asset_widget = VersionLoaderWidget(context=self.context_handler,
                                                      db_asset_data=db_asset)
                self.grid_layout.addWidget(db_asset_widget, idx // 2, idx % 2)


class TaskViewerCoreOverride(TaskViewerCore):
    def __init__(self, context: ContextHandler = None, parent=None):
        super().__init__(context, parent)

    def get_task_list_current_selected(self):
        get_selected_task = self.task_viewer_wdg.selectedItems()
        if len(get_selected_task) != 0:
            for item in get_selected_task:
                get_task_data = item.data(11, 0)

                self.context_handler.task_name = get_task_data.name
                self.context_handler.task_type = get_task_data.task_type
                self.context_handler.task_id = get_task_data.id
                self.current_context.emit(self.context_handler)

                return get_task_data
        else:
            self.context_handler.task_name = None
            self.context_handler.task_type = None
            self.context_handler.task_id = None
            self.current_context.emit(self.context_handler)


class Loader(QtWidgets.QWidget):
    def __init__(self, context: ContextHandler = None, parent=None):
        super(Loader, self).__init__(parent)

        self.project_tree_viewer = None
        self.task_viewer = None
        self.stream_viewer_wdg = None
        self.db_asset_type_btn = None
        self.db_asset_versions_wdg = None
        self.context_menu = None
        self.refresh_btn = None

        self.context_handler = context

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.populate_versions_viewer()
        self.populate_stream_viewer()
        self.populate_task_viewer()

    def create_widgets(self):
        self.project_tree_viewer = ProjectTreeViewerCore(has_project_select_wdg=True,
                                                         has_create_new_proj=False,
                                                         has_context_menu=False)

        self.project_tree_viewer.set_show_to(self.context_handler.show_name)
        self.expand_tree_from_id(self.project_tree_viewer.project_tree_viewer_wdg)

        self.task_viewer = TaskViewerCoreOverride(context=self.context_handler)
        self.task_viewer_overrides()

        self.stream_viewer_wdg = StreamViewerUI(context=self.context_handler)

        self.db_asset_type_btn = AssetTypesButtonsSelectors()

        self.db_asset_versions_wdg = VersionLoader(context=self.context_handler)

        self.streams_lb = QtWidgets.QLabel("Streams")
        self.tasks_lb = QtWidgets.QLabel("Tasks")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        stream_wdg = QtWidgets.QWidget()
        stream_layout = QtWidgets.QVBoxLayout()
        stream_layout.addWidget(self.streams_lb)
        stream_layout.addWidget(self.stream_viewer_wdg)
        stream_wdg.setLayout(stream_layout)

        tasks_wdg = QtWidgets.QWidget()
        tasks_layout = QtWidgets.QVBoxLayout()
        tasks_layout.addWidget(self.tasks_lb)
        tasks_layout.addWidget(self.task_viewer)
        tasks_wdg.setLayout(tasks_layout)

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.project_tree_viewer)
        top_layout.addWidget(stream_wdg)
        top_layout.addWidget(tasks_wdg)
        top_layout.addWidget(self.db_asset_type_btn)
        top_layout.addWidget(self.db_asset_versions_wdg)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.refresh_btn)

        horizontal_splitter = QtWidgets.QSplitter()
        horizontal_splitter.setOrientation(QtCore.Qt.Horizontal)
        top_layout.addWidget(horizontal_splitter)

        horizontal_splitter.insertWidget(0, self.project_tree_viewer)
        horizontal_splitter.insertWidget(1, stream_wdg)
        horizontal_splitter.insertWidget(2, tasks_wdg)
        horizontal_splitter.insertWidget(3, self.db_asset_type_btn)
        horizontal_splitter.insertWidget(4, self.db_asset_versions_wdg)
        horizontal_splitter.setSizes([350, 30, 500, 40, 1200])

    def create_connections(self):
        self.project_tree_viewer.current_context.connect(self.task_viewer.context_receiver)
        self.project_tree_viewer.current_context.connect(self.db_asset_versions_wdg.context_receiver)
        self.project_tree_viewer.current_context.connect(self.stream_viewer_wdg.context_receiver)

        self.project_tree_viewer.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_task_viewer)
        self.project_tree_viewer.project_tree_viewer_wdg.itemClicked.connect(self.populate_task_viewer)

        self.project_tree_viewer.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_versions_viewer)
        self.project_tree_viewer.project_tree_viewer_wdg.itemClicked.connect(self.populate_versions_viewer)

        self.project_tree_viewer.project_tree_viewer_wdg.itemSelectionChanged.connect(self.populate_stream_viewer)
        self.project_tree_viewer.project_tree_viewer_wdg.itemClicked.connect(self.populate_stream_viewer)

        self.task_viewer.current_context.connect(self.db_asset_versions_wdg.context_receiver)
        self.task_viewer.task_viewer_wdg.itemSelectionChanged.connect(self.populate_versions_viewer)

        self.stream_viewer_wdg.current_context.connect(self.db_asset_versions_wdg.context_receiver)
        self.stream_viewer_wdg.stack_stream_lw.itemClicked.connect(self.populate_versions_viewer)
        self.stream_viewer_wdg.stack_stream_lw.itemSelectionChanged.connect(self.populate_versions_viewer)

        # self.refresh_btn.clicked.connect(self.populate_task_viewer)
        self.refresh_btn.clicked.connect(self.populate_versions_viewer)
        # self.refresh_btn.clicked.connect(self.project_tree_viewer.refresh_tree_widget)

    def expand_tree_from_id(self, tree_widget):
        parts = self.context_handler.entity_id.split(".")
        parent = None

        for part in parts:
            if parent:
                items = [parent.child(i) for i in range(parent.childCount())]
            else:
                items = [tree_widget.topLevelItem(i) for i in range(tree_widget.topLevelItemCount())]

            for item in items:
                if item.text(0) == part:
                    item.setExpanded(True)
                    tree_widget.setUpdatesEnabled(False)
                    stored_data = item.data(0, QtCore.Qt.UserRole)
                    tree_widget.setUpdatesEnabled(True)
                    if stored_data.type == "asset":
                        tree_widget.setCurrentItem(item)
                        item.setSelected(True)

                    parent = item
                    break

    def select_last_item(self):
        if self.project_tree_viewer.project_tree_viewer_wdg.topLevelItemCount() == 0:
            return

        # Start from the last top-level item
        item = self.project_tree_viewer.project_tree_viewer_wdg.topLevelItem(self.project_tree_viewer.project_tree_viewer_wdg.topLevelItemCount() - 1)

        # Traverse down to the deepest last child
        while item.childCount() > 0:
            item = item.child(item.childCount() - 1)

        # Set the last item as selected
        self.project_tree_viewer.project_tree_viewer_wdg.setCurrentItem(item)
        item.setSelected(True)  # Optionally, highlight the item

    def populate_task_viewer(self):
        has_selection = self.project_tree_viewer.get_selected()
        if len(has_selection) != 0:
            self.task_viewer.populate_widget()
        else:
            self.project_tree_viewer.project_tree_viewer_wdg.clearSelection()
            self.task_viewer.task_viewer_wdg.clear()

    def populate_stream_viewer(self):
        has_selection = self.project_tree_viewer.get_selected()
        if len(has_selection) != 0:
            self.stream_viewer_wdg.populate_widget()
        else:
            self.stream_viewer_wdg.stack_stream_lw.clearSelection()
            self.stream_viewer_wdg.stack_stream_lw.clear()

    def populate_versions_viewer(self):
        has_selection = self.project_tree_viewer.get_selected()
        if len(has_selection) != 0:
            self.db_asset_versions_wdg.populate_versions()
        else:
            self.db_asset_versions_wdg.clear_versions_wdg()

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

        # self.setMinimumHeight(850)
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
                      'entity_name': 'tafer',
                      'entity_id': 'The_Rock.assets.chr.tafer',
                      'entity_type': 'asset',}
    # 'db_asset_id': 'The_Rock.assets.chr.tafer.geometry.tafer',
    # 'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer',

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
