import os
import sys
from PySide2 import QtWidgets
from envars.envars import Envars
from functools import reduce
from database.entities.db_entities import DbTasks, DbAsset
from database.utils.db_q_entity import From, QEntity
from database.entities.db_attributes import DbProjectAttrPaths, DbEntityAttrPaths
from database.db_ids import DbIds
from common_utils.json_utils import write_json, open_json
from common_utils import version_increment as vin

from ui.custom_widgets.task_imports_from_core import TasksImportFromCore
from ui.custom_widgets.task_publishing_slots_core import PublishSlotsWidgetCore
from ui.custom_widgets.task_viewer_core import TaskViewerCore

import pprint
def dive_deep(key_attr_path, dict_data, delimiter="."):
    if delimiter in key_attr_path:
        get_keys = key_attr_path.split(delimiter)
        return [reduce(dict.get, get_keys, dict_data)]


class ProgressBar():
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)

        self.create_widgets()

    def create_widgets(self):
        self.progress_bar = QtWidgets.QProgressBar()


class TasksFromJson(object):
    def read_json_from_path(self, path_to_file) -> dict:
        file_json = open_json(source_file=path_to_file)
        return file_json
    def read_all_tasks_names(self, input_dict: dict) -> list:
        return list(input_dict["tasks_schema"].keys())


class TaskManagerCore(QtWidgets.QWidget):
    def __init__(self):
        super(TaskManagerCore, self).__init__()
        self.setMinimumHeight(1000)
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.get_tasks()

    def create_widgets(self):
        self.tasks_view_lwd = TaskViewerCore()
        self.tasks_imports_from_properties_wdg = TasksImportFromCore()
        self.tasks_pub_slots_properties_wdg = PublishSlotsWidgetCore()
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.to_category_btn = QtWidgets.QPushButton("...Propagate To Category")
        self.propagate_to_all_in_category_btn = QtWidgets.QPushButton("...Propagate To All Category Entries ")
        self.to_templates_btn = QtWidgets.QPushButton("...Propagate To Templates ")
        self.import_tasks_schema_btn = QtWidgets.QPushButton("Import Tasks Schema ")
        self.load_from_entity_tasks_schema_btn = QtWidgets.QPushButton("Load Tasks Schema From Entity")
        self.dump_tasks_schema_btn = QtWidgets.QPushButton("Save To Disk ")
        self.info_box_wdg = QtWidgets.QLabel("...")

    def create_layout(self):

        views_layout = QtWidgets.QHBoxLayout()
        views_layout.setContentsMargins(1, 1, 1, 1)
        views_layout.addWidget(self.tasks_view_lwd)
        views_layout.addWidget(self.tasks_imports_from_properties_wdg)
        views_layout.addWidget(self.tasks_pub_slots_properties_wdg)

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.to_category_btn)
        button_layout.addWidget(self.propagate_to_all_in_category_btn)
        button_layout.addWidget(self.to_templates_btn)
        button_layout.addWidget(self.dump_tasks_schema_btn)

        button_layout.addWidget(self.info_box_wdg)

        main_layout = QtWidgets.QVBoxLayout(self)
        # main_layout.addWidget(self.import_tasks_schema_btn)
        main_layout.addWidget(self.load_from_entity_tasks_schema_btn)

        main_layout.addLayout(views_layout)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.addLayout(button_layout)

    def update_info_label(self, message_in):
        self.info_box_wdg.setText(message_in)

    def create_connections(self):
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.tasks_pub_slots_properties_wdg.clear_selection)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_task_import_schema)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_pub_slots)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.get_selected_type)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.tasks_pub_slots_properties_wdg.change_label_pub_slots)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect( self.tasks_imports_from_properties_wdg.change_label_existing_tasks)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect( self.tasks_imports_from_properties_wdg.change_label_imports_from)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect( self.tasks_imports_from_properties_wdg.change_label_imports_from_assignments)

        self.to_category_btn.clicked.connect(self.save_schema_to_category)
        self.propagate_to_all_in_category_btn.clicked.connect(self.update_all_schemas_assets)
        self.to_templates_btn.clicked.connect(self.save_as_db_template)
        self.dump_tasks_schema_btn.clicked.connect(self.save_schema_to_disk)
        self.load_from_entity_tasks_schema_btn.clicked.connect(self.show_all_entries)

        self.refresh_btn.clicked.connect(self.populate_task_import_schema)
        self.refresh_btn.clicked.connect(self.populate_pub_slots)
        self.refresh_btn.clicked.connect(self.get_tasks)

    def extract_task_schema(self):
        current_task_schema = DbTasks().get_tasks_full()
        return current_task_schema["tasks"]

    def show_all_entries(self):
        self.update_info_label(message_in="Loading all Entries")

    def save_schema_to_disk(self):
        #TODO version control and file name composition
        category = Envars().category

        base_info = dict(
            category=category,
            tasks_schema=self.extract_task_schema()
        )
        path_to_write = os.path.join(os.environ["ORIGIN_PROJECTS_ROOT"], "Origin_Tasks_Templates", category)
        version = vin.next_file_version(path_to_write)
        file_name = "_".join([category, version])

        write_json(target_path=path_to_write, target_file=file_name, data=base_info)

        self.update_info_label(message_in="Saved {0} To {1} ".format(file_name, path_to_write))

    def save_schema_to_category(self):
        category_tasks_type = Envars().category + "_tasks"
        tasks_schema = self.extract_task_schema()

        QEntity(db_collection=From().projects,
                entry_id=DbIds.curr_project_id(),
                attribute_path=DbProjectAttrPaths.show_defaults()
                ).add_property(name=category_tasks_type,
                               add_data=tasks_schema)

        self.update_info_label(message_in="Saved To {0} Category For Future Assets To Inherit".format((Envars.category).upper()))

    def update_all_schemas_assets(self):
        tasks_schema = self.extract_task_schema()

        get_cat_assets_reference = DbAsset().get_all()

        for entity_ref in get_cat_assets_reference:
            entity_id = entity_ref.split(",")[1]
            QEntity(db_collection=From().entities,
                    entry_id=entity_id,
                    attribute_path=DbEntityAttrPaths.to_tasks()
                    ).update(data=tasks_schema)

        self.update_info_label(message_in="All Assets In {0} Category Have been Updated To Current Task Schema".format((Envars.category).upper()))

    def save_as_db_template(self):
        self.update_info_label(message_in="Current Task Schema is Saved As Show Template for {} Category".format((Envars.category).upper()))

    def get_task_type(self):
        task_name = self.tasks_view_lwd.get_selected_task()
        if task_name:
            task_type = "task"
            return task_type

    def populate_task_import_schema(self):
        self.tasks_imports_from_properties_wdg.populate_main_widget()

    def get_tasks(self):
        self.tasks_view_lwd.populate_tasks()

    def get_selected_type(self):
        task_selected = self.tasks_view_lwd.task_viewer_wdg.hasFocus()

        if task_selected:
            task_type = self.get_task_type()
            return task_type

    def populate_pub_slots(self):
        self.tasks_pub_slots_properties_wdg.populate_main_widget()


class TaskManagerMainUI(QtWidgets.QMainWindow):
    WINDOW_TITLE = "Origin Task Manager"

    def __init__(self, parent=None):
        super(TaskManagerMainUI, self).__init__(parent)
        self.setWindowTitle(self.window_context_details())
        central_widget = TaskManagerCore()
        self.setCentralWidget(central_widget)

    def window_context_details(self):
        show_name = (Envars().show_name).upper()
        branch_name = (Envars().branch_name).upper()
        category = (Envars().category).upper()
        entity_name = (Envars().entry_name).upper()

        window_name = " -> ".join([self.WINDOW_TITLE, show_name, branch_name, category, entity_name])
        return window_name

# TODO to implement Loading assignments from a given entity


if __name__ == "__main__":
    Envars.show_name = "Green"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "hulk"

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = TaskManagerMainUI()
    test_dialog.show()
    sys.exit(app.exec_())


