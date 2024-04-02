from common_utils.date_time import DateTime
from common_utils.odb_output_paths import OutputPaths
from common_utils.users import Users
from database.db_statuses import DbStatuses
from envars.origin_envars import OriginEnvar
from o_database.entities.ids import DbIds
from o_database.schemas.actions import EntityDefaultSchemas
from o_database.collections.connections import ProjectCollections
from o_database.utils.version_increase import DBVersionIncrease


class DbConstructors:

    def _project_defaults(self):
        proj_defaults = dict(asset_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
                             shots_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
                             characters_tasks=EntityDefaultSchemas().tasks.character_schema,
                             props_tasks=EntityDefaultSchemas().tasks.prop_schema,
                             environments_tasks=EntityDefaultSchemas().tasks.environment_schema,
                             characters_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
                             props_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
                             environments_definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
                             shots_tasks=EntityDefaultSchemas().tasks.shot_schema)

        return proj_defaults

    @staticmethod
    def project_construct(name: str, entity_id: str, project_code: str, project_type="vfx"):
        entity_attributes = dict(
            _id=entity_id,
            entry_name=name,
            type='project',
            project_code=project_code,
            project_type_type=project_type,
            data={},
            config={},
            children=[],
            visual_children=[],
            parent=None,
            visual_parent=None,
            project_defaults={},
            active=True,
            origin_db_path='',
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user())

        return entity_id, entity_attributes

    @staticmethod
    def asset_construct(name, entity_id, task_schema=None):
        if task_schema is None:
            tasks = {}
        else:
            tasks = task_schema

        v_parent = OriginEnvar().resolve_context_to_base()

        entity_attributes = dict(
            _id=entity_id,
            entry_name=name,
            type='asset',
            status="",
            active=True,
            origin_db_path=v_parent,
            assignment={},
            assigned_to=[],
            definition={},
            tasks=tasks,
            components={},
            config={},
            data={
                "stack_streams": ["main"],
                "variant_sets": {"geo_var_sets": {

                }
                },
                "groom_var_sets": {

                },
                "mtl_var_sets": {

                }
            },
            children=[],
            visual_children=[],
            parent=OriginEnvar().show_name,
            visual_parent=v_parent,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()

        )
        return entity_id, entity_attributes, v_parent

    @staticmethod
    def group_construct(name, entity_id, task_schema=None):
        if task_schema is None:
            tasks = {}
        else:
            tasks = task_schema

        v_parent = OriginEnvar().resolve_context_to_base()

        entity_attributes = dict(
            _id=entity_id,
            entry_name=name,
            type='group',
            status=None,
            active=True,
            origin_db_path=OriginEnvar().resolve_context_to_base(),
            assignment=None,
            assigned_to=None,
            definition={},
            tasks=tasks,
            components=None,
            config='',
            data={},
            children=[],
            visual_children=[],
            parent=OriginEnvar().resolve_context_to_base(),
            visual_parent=v_parent,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()
        )
        return entity_id, entity_attributes, v_parent

    @staticmethod
    def task_construct(task_type):

        task_attributes = dict(
            active=True,
            type=task_type,
            status="NOT-STARTED",
            artist="None",
            priority="",
            description="",
            imports_from={},
            bid_days="",
            end_date="",
            milestones={},
            start_date="",
            worked_days="",
            previous_artists=[]
        )
        return task_attributes

    @staticmethod
    def work_session_construct(file_name):
        version = DBVersionIncrease().db_wip_files_version_increase(ProjectCollections().project_work_files_collection())

        set_base_name = "_".join([OriginEnvar().entry_name, OriginEnvar().task_name])
        set_display_name = "__".join([set_base_name, "work_file", Users.curr_user(),version])

        common_id = DbIds.get_wip_file_id(version)

        save_content = dict(
            _id=common_id,
            entry_name=set_display_name,
            type="work_file",
            description=[],
            task_name=OriginEnvar().task_name,
            status=None,
            version=version,
            components=dict(main_path=OutputPaths(version, output_file_name=file_name).wip_file_path()),
            session_content={"inputs": []},
            origin_db_path=OriginEnvar().resolve_current_context(),
            children=None,
            visual_children=None,
            parent=OriginEnvar().entry_name,
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
        set_display_name = "_".join([OriginEnvar().entry_name, "stack", version])

        entity_attributes = dict(
            _id=common_id,
            entry_name=set_display_name,
            type="stack",
            description=[],
            status=status,
            version=version,
            components="compute slots order and names from tasks outputs dependency resolve",        # TODO
            origin_db_path=OriginEnvar().resolve_current_context(),
            children=[],
            visual_children=[],
            parent=OriginEnvar().entry_name,
            visual_parent=None,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user())

        return common_id, entity_attributes

    @staticmethod
    def task_publish_construct():
        version = DBVersionIncrease().db_main_pub_ver_increase()
        set_display_name = "_".join([OriginEnvar().entry_name, "main_publish"])
        common_id = DbIds.get_main_pub_id(version)

        save_content = dict(
            _id=common_id,
            entry_name=set_display_name,
            type="publish",
            description=[],
            status="PENDING_REVIEW",
            version=version,
            components="Needs to be a separate compute that is inked to the task type",   #TODO
            origin_db_path=OriginEnvar().resolve_current_context(),
            children=[],
            visual_children=[],
            parent=OriginEnvar().entry_name,
            visual_parent=None,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user())

        return common_id, save_content, set_display_name
