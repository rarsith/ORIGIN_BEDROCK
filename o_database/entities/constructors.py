from dataclasses import dataclass, field
from typing import Any, Dict

from common_utils.date_time import DateTime
from common_utils.odb_output_paths import OutputPaths
from common_utils.users import Users
from database.db_statuses import DbStatuses
from envars.origin_envars import OriginEnvar
from o_database.entities.ids import DbIds
from o_database.schemas.actions import EntityDefaultSchemas
from o_database.collections.connections import ProjectCollections
from o_database.utils.version_increase import DBVersionIncrease


@dataclass
class PublishComponentConstructor:
    pass


@dataclass
class BaseConstructor:
    _id: str
    entry_name: str
    type: str
    visual_parent: str

    active: bool = field(init=False)
    children: list = field(init=False)
    visual_children: list = field(init=False)
    parent: str = field(init=False)

    definition: dict = field(init=False)
    origin_db_path: str = field(init=False)
    date: str = field(init=False)
    time: str = field(init=False)
    owner: str = field(init=False)

    def __post_init__(self):
        self.children: list = []
        self.visual_children: list = []
        self.active: bool = True
        self.data: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {}

        self.origin_db_path: str = OriginEnvar.resolve_to_base_context()
        self.parent: str = OriginEnvar.show_name
        self.definition: dict = EntityDefaultSchemas().entry_definition.skeleton_schema
        self.date: str = DateTime().curr_date
        self.time: str = DateTime().curr_time
        self.owner: str = Users().curr_user()


@dataclass
class ProjectConstructor(BaseConstructor):
    project_code: str
    project_type: str
    project_defaults: dict = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.project_defaults: dict = {}


@dataclass
class ProjectDefaultsConstructor:
    asset_definition: dict
    shots_definition: dict
    characters_tasks: dict
    props_tasks: dict
    environments_tasks: dict
    characters_definition: dict
    props_definition: dict
    environments_definition: dict
    shots_tasks: dict


@dataclass
class EntityConstructor(BaseConstructor):

    tasks: str
    status: str = field(init=False)
    assignment: dict = field(init=False)
    assigned_to: dict = field(init=False)
    components: dict = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.status: str = "NOT STARTED"
        self.assignment: dict = {}
        self.assigned_to: dict = {}
        self.components: dict = {}

@dataclass
class TaskConstructor:
    active: bool
    type: str
    status: str
    artist: str
    priority: str
    description: str
    imports_from: dict
    bid_days: str
    end_date: str
    milestones: dict
    start_date: str
    worked_days: str
    previous_artists: list


class DbConstructors:

    def _project_defaults(self):
        project_default_constructor = ProjectDefaultsConstructor(
            asset_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
            shots_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
            characters_tasks=EntityDefaultSchemas().tasks.character_schema,
            props_tasks=EntityDefaultSchemas().tasks.prop_schema,
            environments_tasks=EntityDefaultSchemas().tasks.environment_schema,
            characters_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
            props_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
            environments_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
            shots_tasks=EntityDefaultSchemas().tasks.shot_schema
        )

        return  project_default_constructor.__dict__

    @staticmethod
    def project_construct(name: str, entity_id: str, project_code: str, project_type="vfx"):

        entity_constructor = ProjectConstructor(_id=entity_id,
                                                entry_name=name,
                                                project_code='project_code',
                                                project_type=project_type,
                                                visual_parent="root",
                                                type="project"
                                                )

        entity_constructor.origin_db_path = "root"
        entity_constructor.parent = "root"

        entity_attributes = entity_constructor.__dict__
        return entity_id, entity_attributes

    @staticmethod
    def asset_construct(name, entity_id, task_schema=None):
        if task_schema is None:
            tasks = {}
        else:
            tasks = task_schema

        v_parent = OriginEnvar.resolve_to_base_context()

        entity_constructor = EntityConstructor(_id=entity_id,
                                               entry_name=name,
                                               type="asset",
                                               tasks=tasks,
                                               visual_parent=v_parent
                                               )

        entity_attributes = entity_constructor.__dict__

        return entity_id, entity_attributes, v_parent

    @staticmethod
    def group_construct(name, entity_id, task_schema=None):
        if task_schema is None:
            tasks = {}
        else:
            tasks = task_schema

        v_parent = OriginEnvar.resolve_to_base_context()

        entity_constructor = EntityConstructor(_id=entity_id,
                                               entry_name=name,
                                               type="group",
                                               tasks=tasks,
                                               visual_parent=v_parent
                                               )

        entity_attributes = entity_constructor.__dict__

        return entity_id, entity_attributes, v_parent

    @staticmethod
    def task_construct(task_type):
        task_constructor = TaskConstructor(
                                            active=True,
                                            type=task_type,
                                            status="READY TO START",
                                            artist="None",
                                            priority="NORMAL",
                                            description="",
                                            imports_from={},
                                            bid_days="",
                                            end_date="",
                                            milestones={},
                                            start_date="",
                                            worked_days="",
                                            previous_artists=[]
                                            )
        task_attributes = task_constructor.__dict__

        return task_attributes

    @staticmethod
    def work_session_construct(file_name):
        version = DBVersionIncrease().db_wip_files_version_increase(
            ProjectCollections().project_work_files_collection())

        set_base_name = "_".join([OriginEnvar.entry_name, OriginEnvar.task_name])
        set_display_name = "__".join([set_base_name, "work_file", Users.curr_user(), version])

        common_id = DbIds.get_wip_file_id(version)

        save_content = dict(
            _id=common_id,
            entry_name=set_display_name,
            type="work_file",
            description=[],
            task_name=OriginEnvar.task_name,
            status=None,
            version=version,
            components=dict(main_path=OutputPaths(version, output_file_name=file_name).wip_file_path()),
            session_content={"inputs": []},
            origin_db_path=OriginEnvar.resolve_to_full_context(),
            children=None,
            visual_children=None,
            parent=OriginEnvar.entry_name,
            visual_parent=None,
            representation={},
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user())

        return common_id, save_content

    @staticmethod
    def stack_construct():
        status = DbStatuses.pending_rev
        version = DBVersionIncrease().db_master_bundle_ver_increase()
        common_id = DbIds.get_master_bundle_id(version)
        set_display_name = "_".join([OriginEnvar.entry_name, "stack", version])

        entity_attributes = dict(
            _id=common_id,
            entry_name=set_display_name,
            type="stack",
            description=[],
            status=status,
            version=version,
            components="compute slots order and names from tasks outputs dependency resolve",  # TODO
            origin_db_path=OriginEnvar.resolve_to_full_context(),
            children=[],
            visual_children=[],
            parent=OriginEnvar.entry_name,
            visual_parent=None,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user())

        return common_id, entity_attributes

    @staticmethod
    def task_publish_construct(version=None):
        if version is None:
            version = DBVersionIncrease().db_main_pub_ver_increase()

        set_display_name = "_".join([OriginEnvar.entry_name, OriginEnvar.task_name,"main_publish", version])
        common_id = DbIds.get_main_pub_id(version)

        save_content = dict(
            _id=common_id,
            entry_name=set_display_name,
            type="publish",
            asset_type="Dummy",
            task=OriginEnvar.task_name,
            task_type=OriginEnvar.task_type,
            parent_task=OriginEnvar.resolve_to_full_context(),
            description=[],
            status="PENDING REVIEW",
            version=version,
            version_cnt=int(version),
            components="Needs to be a separate compute that is inked to the task type",  # TODO
            origin_db_path=OriginEnvar.resolve_to_full_context(),
            parent=OriginEnvar.resolve_to_master(),
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user())

        return common_id, save_content, set_display_name


if __name__ == "__main__":
    data = {
        "stack_streams": ["main"],
        "variant_sets": {"geo_var_sets": {}
                         },
        "groom_var_sets": {},
        "mtl_var_sets": {}}