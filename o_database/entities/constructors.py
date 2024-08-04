from pydantic import BaseModel, Field
from typing import Optional
from common_utils.date_time import DateTime
from common_utils.odb_output_paths import OutputPaths
from common_utils.users import Users
from envars.origin_envars import OriginEnvar
from envars.origin_envars import ContextHandler
from o_database.entities.ids import DbIds
from o_database.schemas.actions import EntityDefaultSchemas
from o_database.collections.connections import ProjectCollections
from o_database.utils.version_increase import DBVersionIncrease


class BaseConstructor(BaseModel):
    id: Optional[str] = Field(alias='_id')
    entry_name: Optional[str] = None
    type: Optional[str] = None
    visual_parent: Optional[str] = None
    active: Optional[bool] = None
    children: Optional[list] = None
    visual_children: Optional[list] = None
    parent: Optional[str] = None
    definition: Optional[dict] = None
    origin_db_path: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    owner: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }


class ProjectConstructor(BaseConstructor):
    project_code: Optional[str] = None
    project_type: Optional[str] = None
    project_defaults: Optional[dict] = None


class ProjectDefaultsConstructor(BaseModel):
    asset_definition: Optional[dict] = None
    shots_definition: Optional[dict] = None
    characters_tasks: Optional[dict] = None
    props_tasks: Optional[dict] = None
    environments_tasks: Optional[dict] = None
    characters_definition: Optional[dict] = None
    props_definition: Optional[dict] = None
    environments_definition: Optional[dict] = None
    shots_tasks: Optional[dict] = None


class EntityConstructor(BaseConstructor):
    tasks: Optional[dict] = None
    status: Optional[str] = None
    assignment: Optional[dict] = None
    assigned_to: Optional[dict] = None
    components: Optional[dict] = None


class TaskConstructor(BaseModel):
    active: Optional[bool] = None
    type: Optional[str] = None
    status: Optional[str] = None
    artist: Optional[str] = None
    priority: Optional[str] = None
    description: Optional[str] = None
    imports_from: Optional[dict] = None
    db_assets: Optional[list] = None
    bid_days: Optional[str] = None
    end_date: Optional[str] = None
    milestones: Optional[dict] = None
    start_date: Optional[str] = None
    worked_days: Optional[str] = None
    previous_artists: Optional[list] = None


class DBAssetConstruct(BaseModel):
    id: Optional[str] = Field(alias='_id')
    label: Optional[str] = None
    show_name: Optional[str] = None
    entry_name: Optional[str] = None
    type: Optional[str] = None
    task_type: Optional[str] = None
    task_name: Optional[str] = None
    content_type: Optional[str] = None
    origin_db_path: Optional[str] = None
    server_path: Optional[str] = None
    parent: Optional[str] = None
    children: Optional[list] = None
    date: Optional[str] = None
    time: Optional[str] = None
    owner: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }


class DBAssetVersionConstruct(BaseModel):
    id: Optional[str] = Field(alias='_id')
    label: Optional[str] = None
    entry_name: Optional[str] = None
    show_name: Optional[str] = None
    asset_type: Optional[str] = None
    task_type: Optional[str] = None
    description: Optional[str] = None
    comments: Optional[list[str]] = None
    status: Optional[str] = None
    version: Optional[str] = None
    version_cnt: Optional[int] = None
    server_path: Optional[str] = None
    origin_db_path: Optional[str] = None
    type: Optional[str] = None
    parent: Optional[str] = None
    children: Optional[list] = None
    date: Optional[str] = None
    time: Optional[str] = None
    owner: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }


class DBFileComponentConstruct(BaseModel):
    id: Optional[str] = Field(alias='_id')
    label: Optional[str] = None
    entry_name: Optional[str] = None
    show_name: Optional[str] = None
    server_path: Optional[str] = None
    origin_db_path: Optional[str] = None
    type: Optional[str] = None
    parent: Optional[str] = None
    file_extension: Optional[list[str]] = None
    file_path: Optional[str] = None
    visible: Optional[bool] = None
    date: Optional[str] = None
    time: Optional[str] = None
    owner: Optional[str] = None

    model_config = {
        "from_attributes": True,
    }


class DbConstructors:

    @staticmethod
    def _project_defaults():
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

        entity_constructor = ProjectConstructor(
            _id=entity_id,
            entry_name=name,
            project_code=project_code,
            project_type=project_type,
            visual_parent="root",
            type="project"
        )

        entity_constructor.origin_db_path = "root"
        entity_constructor.parent = "root"

        entity_attributes = entity_constructor.dict(by_alias=True)
        return entity_id, entity_attributes

    @staticmethod
    def asset_construct(name, entity_id, task_schema=None):
        if task_schema is None:
            tasks = {}
        else:
            tasks = task_schema

        v_parent = OriginEnvar.resolve_to_base_context()

        entity_constructor = EntityConstructor(
            _id=entity_id,
            active=True,
            entry_name=name,
            type="asset",
            tasks=tasks,
            visual_parent=v_parent,
            children=[],
            status="NOT STARTED",
            assignment={},
            assigned_to={},
            components={},
            visual_children=[],
            data={},
            config={},
            origin_db_path=OriginEnvar.resolve_to_base_context(),
            parent=OriginEnvar.show_name,
            definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        entity_attributes = entity_constructor.dict(by_alias=True)
        return entity_id, entity_attributes, v_parent

    @staticmethod
    def group_construct(name, entity_id, task_schema=None):
        if task_schema is None:
            tasks = {}
        else:
            tasks = task_schema

        v_parent = OriginEnvar.resolve_to_base_context()

        entity_constructor = EntityConstructor(
            _id=entity_id,
            active=True,
            entry_name=name,
            type="group",
            tasks=tasks,
            visual_parent=v_parent,
            children=[],
            status="NOT STARTED",
            assignment={},
            assigned_to={},
            components={},
            visual_children=[],
            data={},
            config={},
            origin_db_path=OriginEnvar.resolve_to_base_context(),
            parent=OriginEnvar.show_name,
            definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        entity_attributes = entity_constructor.dict(by_alias=True)
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
            db_assets=[],
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
    def db_asset_construct(entity_id: str, parent_id: str, name: str, context: ContextHandler):
        get_task_type = context.task_type
        get_task_name = context.task_name
        set_display_name = "_".join([name, f"_{get_task_type}"])

        entity_attributes = DBAssetConstruct(
            _id=entity_id,
            label=set_display_name,
            show_name=context.show_name,
            entry_name=context.entry_name,
            type='db_asset',
            content_type='to be defined',
            task_type=get_task_type,
            task_name=get_task_name,
            origin_db_path=context.resolve_to_full_context(),
            parent=parent_id,
            children=[],
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()
        )

        return entity_attributes.dict(by_alias=True)

    @staticmethod
    def db_asset_version_construct(entity_id: str,
                                   parent_id: str,
                                   version: str,
                                   pub_comment: str,
                                   status: str,
                                   context: ContextHandler):
        import os
        set_display_name = "_".join([context.entry_name, f"_{context.task_type}", f"_{version}"])
        get_server_root_path = context.server_root_path()
        project_path = os.path.join(get_server_root_path, set_display_name)
        version_compile = ''.join(["v", str(version)])

        entity_attributes = DBAssetVersionConstruct(
            _id=entity_id,
            label=context.entry_name,
            entry_name=set_display_name,
            show_name=context.show_name,
            asset_type='',
            task_type=context.task_type,
            description=pub_comment,
            comments=[],
            status=status,
            version=version_compile,
            version_cnt=version,
            server_path=project_path,
            origin_db_path=context.resolve_to_full_context(),
            type='',
            parent=parent_id,
            children=[],
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()
        )

        return entity_attributes.dict(by_alias=True)

    @staticmethod
    def db_asset_file_component(entity_id: str,
                                display_name: str,
                                visibility: bool,
                                file_ext: str,
                                parent_id: str,
                                output_file_path: str,
                                context: ContextHandler
                                ) -> dict:

        entity_attributes = DBFileComponentConstruct(
            _id=entity_id,
            label=display_name,
            show_name=context.show_name,
            type='',
            parent=parent_id,
            file_extension=file_ext,
            file_path=output_file_path,
            visible=visibility,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()
        )

        return entity_attributes.dict(by_alias=True)

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

    xx = DBAssetConstruct()
    xx.label = "label"
    xx.show_name = "DUDU"
    print(xx.dict())