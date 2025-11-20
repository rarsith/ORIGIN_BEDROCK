import os
import pprint

from PySide2 import QtWidgets, QtGui, QtCore

from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler
from origin.ui.project_tree_viewer_core import ProjectTreeViewerCore
from origin.ui.task_viewer_core import TaskViewerCore


class ContextManager(QtWidgets.QWidget):
    submit_pressed = QtCore.Signal()

    def __init__(self, parent=None):
        super(ContextManager, self).__init__(parent)

        self.context_handler = None
        self.project_tree_viewer = None
        self.task_viewer = None

        self.refresh_btn = None
        self.set_context_btn = None

        self.get_current_context()

        self.create_widgets()
        self.create_layout()

        self.populate_task_viewer()
        # self.select_active_task(self.task_viewer.task_viewer_wdg)

    def create_widgets(self):
        self.project_tree_viewer = ProjectTreeViewerCore(has_project_select_wdg=True,
                                                         has_create_new_proj=False,
                                                         has_context_menu=False)

        self.project_tree_viewer.set_show_to(self.context_handler.show_name)
        self.expand_tree_from_id(self.project_tree_viewer.project_tree_viewer_wdg)

        self.task_viewer = TaskViewerCore(context=self.context_handler)
        self.select_active_task(self.task_viewer.task_viewer_wdg)
        self.task_viewer_overrides()

        self.set_context_btn = QtWidgets.QPushButton("Set Context")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.project_tree_viewer)
        top_layout.addWidget(self.task_viewer)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.set_context_btn)
        main_layout.addWidget(self.refresh_btn)

        horizontal_splitter = QtWidgets.QSplitter()
        horizontal_splitter.setOrientation(QtCore.Qt.Horizontal)
        top_layout.addWidget(horizontal_splitter)

        horizontal_splitter.insertWidget(0, self.project_tree_viewer)
        horizontal_splitter.insertWidget(1, self.task_viewer)
        horizontal_splitter.setSizes([200, 200])

    def on_submit_pressed(self):
        self.submit_pressed.emit()

    def context_receiver(self, context):
        self.new_context = context

    def update_context_envars(self):
        current_session = self.new_context.snapshot_session()
        sys_envar_upper = self.new_context.convert_to_uppercases(current_session)
        cleaned_values = self.clean_values(data=sys_envar_upper, value_to_replace=None, value_to_assign='')
        path_handler = OriginOSPathHandler(context=self.new_context)
        path_handler.create_work_folders()

        self.update_envar(cleaned_values)
        self.populate_project_tree()
        self.populate_task_viewer()

    def clean_values(self, data, value_to_replace, value_to_assign):
        buffer = {}
        for key, value in data.items():
            if value == value_to_replace:
                value = value_to_assign
                buffer[key] = value
            else:
                buffer[key] = value
        return buffer

    def update_envar(self, env_dict):
        upper_envar_keys = {k.upper(): v for k, v in env_dict.items()}
        buffer = {}
        for key, value in upper_envar_keys.items():
            os.environ[key] = value
            buffer[key] = value
        # pprint.pprint(buffer)

    def get_current_context(self):
        context_env = {
            key: value
            for key, value in {
                "session_filename": os.getenv("SESSION_FILENAME"),
                "session_id": os.getenv("SESSION_ID"),
                "show_name": os.getenv("SHOW_NAME"),
                "project_publishes": os.getenv("PROJECT_PUBLISHES"),
                "project_work": os.getenv("PROJECT_WORK"),
                "project_control": os.getenv("PROJECT_CONTROL"),
                "origin_path_hierarchy": os.getenv("ORIGIN_PATH_HIERARCHY"),
                "entity_name": os.getenv("ENTITY_NAME"),
                "entity_type": os.getenv("ENTITY_TYPE"),
                "entity_id": os.getenv("ENTITY_ID"),
                "task_name": os.getenv("TASK_NAME"),
                "task_type": os.getenv("TASK_TYPE"),
                "task_id": os.getenv("TASK_ID"),
                "db_asset_stream_id": os.getenv("DB_ASSET_STREAM_ID"),
                "db_asset_type": os.getenv("DB_ASSET_TYPE"),
                "db_asset_id": os.getenv("DB_ASSET_ID"),
                "db_asset_version_id": os.getenv("DB_ASSET_VERSION_ID"),
                "asset_breakdown_id": os.getenv("ASSET_BREAKDOWN_ID"),
            }.items()
            if value is not None
        }
        self.context_handler = ContextHandler()
        self.context_handler.load_session(session_data=context_env)

        print("LOADING CURRENT SESSION: ", self.context_handler.snapshot_session())

        return context_env

    def populate_project_tree(self):
        self.get_current_context()
        self.project_tree_viewer.set_show_to(self.context_handler.show_name)
        self.expand_tree_from_id(self.project_tree_viewer.project_tree_viewer_wdg)

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

    def select_active_task(self, task_widget):
        print(self.context_handler.task_name)
        items = [task_widget.topLevelItem(i) for i in range(task_widget.topLevelItemCount())]

        for idx, item in enumerate(items):
            if item.text(0) == self.context_handler.task_name:
                task_widget.setCurrentItem(item)
                item.setSelected(True)

    def select_last_item(self):
        if self.project_tree_viewer.project_tree_viewer_wdg.topLevelItemCount() == 0:
            return
        else:
            item = self.project_tree_viewer.project_tree_viewer_wdg.topLevelItem(self.project_tree_viewer.project_tree_viewer_wdg.topLevelItemCount() - 1)

            while item.childCount() > 0:
                item = item.child(item.childCount() - 1)

            self.project_tree_viewer.project_tree_viewer_wdg.setCurrentItem(item)
            item.setSelected(True)

    def populate_task_viewer(self):
        has_selection = self.project_tree_viewer.get_selected()

        if len(has_selection) != 0:
            self.task_viewer.populate_widget()
            # self.select_active_task(self.task_viewer.task_viewer_wdg)
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

        self.task_viewer.task_viewer_wdg.setColumnWidth(0, 250)

        self.task_viewer.add_btn.setEnabled(False)
        self.task_viewer.add_btn.setVisible(False)
        self.task_viewer.save_changes_btn.setVisible(False)
        self.task_viewer.save_changes_btn.setVisible(False)
        self.task_viewer.export_btn.setVisible(False)
        self.task_viewer.export_btn.setVisible(False)
        self.task_viewer.refresh_btn.setVisible(False)
        self.task_viewer.refresh_btn.setVisible(False)


class ContextManagerMainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ContextManagerMainUI, self).__init__(parent)

        self.setMinimumWidth(850)
        self.central_widget = ContextManager()
        self.central_widget.get_current_context()
        self.central_widget.populate_task_viewer()
        self.central_widget.select_active_task(self.central_widget.task_viewer.task_viewer_wdg)
        self.setCentralWidget(self.central_widget)
        self.create_connections()
        self.compute_context()

    def create_connections(self):
        self.central_widget.project_tree_viewer.current_context.connect(self.central_widget.task_viewer.context_receiver)
        self.central_widget.project_tree_viewer.project_tree_viewer_wdg.itemSelectionChanged.connect(self.central_widget.populate_task_viewer)
        self.central_widget.project_tree_viewer.project_tree_viewer_wdg.itemClicked.connect(self.central_widget.populate_task_viewer)

        self.central_widget.task_viewer.current_context.connect(self.central_widget.context_receiver)

        self.central_widget.set_context_btn.clicked.connect(self.central_widget.update_context_envars)
        self.central_widget.set_context_btn.clicked.connect(self.compute_context)
        self.central_widget.set_context_btn.clicked.connect(self.central_widget.on_submit_pressed)
        self.central_widget.set_context_btn.clicked.connect(lambda: self.close())
        self.central_widget.refresh_btn.clicked.connect(self.central_widget.populate_project_tree)
        self.central_widget.refresh_btn.clicked.connect(self.central_widget.populate_task_viewer)

    def compute_context(self):
        # show_name = os.getenv("SHOW_NAME")  # self.central_widget.context_handler.show_name
        show_name = self.central_widget.context_handler.show_name
        # origin_path = os.getenv("ORIGIN_PATH_HIERARCHY")  # self.central_widget.context_handler.origin_path_hierarchy
        origin_path = self.central_widget.context_handler.origin_path_hierarchy
        # entity_name = os.getenv("ENTITY_NAME")  # self.central_widget.context_handler.entity_name
        entity_name = self.central_widget.context_handler.entity_name
        # task_name = os.getenv("TASK_NAME")  # self.central_widget.context_handler.task_name
        task_name = self.central_widget.context_handler.task_name
        # task_type = f"({os.getenv('TASK_TYPE')})"  # f"({self.central_widget.context_handler.task_type})"
        task_type = f"({self.central_widget.context_handler.task_type})"

        split_hierarchy_name = ">>".join(origin_path.split("."))
        compiled_name = ">>".join([show_name, split_hierarchy_name, entity_name, task_name, task_type])
        self.setWindowTitle(f"Context Manager - {compiled_name}")

        return compiled_name


if __name__ == "__main__":
    import sys

    origin_dev_root = os.getenv("ORIGIN_ROOT")
    qss_style_file = os.path.normpath(
        os.path.join(origin_dev_root, "origin/ui/style/stylesheets/dark_orange/dark_orange_style.qss"))

    context_sample = {'show_name': 'The_Rock',
                      'project_publishes': 'The_Rock__PUBLISHES',
                      'project_work': 'The_Rock__WORK',
                      'project_control': 'The_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.props',
                      'entity_name': 'rock',
                      'entity_id': 'The_Rock.assets.props.rock',
                      'asset_breakdown_id': 'The_Rock.assets.props.rock.breakdown',
                      'entity_type': 'asset',
                      'task_name': "modeling",
                      'task_type': "modeling",
                      'task_id': "The_Rock.assets.props.rock.modeling",
                      'db_asset_id': 'The_Rock.assets.props.knife.geometry.rock_main',
                      'db_asset_stream_id': 'The_Rock.assets.props.knife.rock_main',
                      'stack_id': 'The_Rock.assets.props.knife.rock_main.asset_stack',
                      }

    def update_envar(env_dict):
        for key, value in env_dict.items():
            os.environ[key] = value

    update_envar(context_sample)

    # context_obj = ContextHandler()
    # context_obj.load_session(session_data=context_sample)

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    test_dialog = ContextManagerMainUI()

    with open(qss_style_file, "r") as f:
        _style = f.read()
        test_dialog.setStyleSheet(_style)

    # test_dialog.populate_widget()
    test_dialog.show()
    sys.exit(app.exec_())
