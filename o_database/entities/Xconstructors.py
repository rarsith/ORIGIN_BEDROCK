from common_utils.date_time import DateTime
from common_utils.users import Users
from origin.envars.origin_envars import OriginEnvar
from origin.envars.Xorigin_envars import ContextHandler
from o_database.entities.Xids import DbIds
from o_database.schemas.actions import EntityDefaultSchemas

from o_database.utils.version_increase import DBVersionIncrease

from o_database.entities.Xoperators import (Project,
                                            Asset,
                                            Group,
                                            Task,
                                            WorkFile,
                                            DBAsset,
                                            DBAssetFileComponent,
                                            DBAssetVersion)


class DbConstructors:

    def __init__(self, context=None):
        self.context = context
        if self.context is not None:
            self.context_handler = ContextHandler()
            self.context_handler.load_session(session_data=self.context)

    @staticmethod
    def project_construct(name: str, entity_id: str, project_code: str, project_type="vfx"):

        document = Project(

            _id=entity_id,
            name=name,
            active=True,
            type="project",
            parent="root",
            children=[],
            origin_db_path="root",
            status="NOT STARTED",
            components={},

            show_type=project_type,
            show_code=project_code,
            show_settings={},

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        project_db_doc = document.dict(by_alias=True)

        return project_db_doc

    @staticmethod
    def asset_construct(name, entity_id, parent_id, task_schema=None):
        if task_schema is None:
            tasks = {}
        else:
            tasks = task_schema

        document = Asset(

            _id=entity_id,
            name=name,
            active=True,
            type="asset",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="NOT STARTED",
            components={},

            definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
            tasks=tasks,
            assignees={},
            assigned_to={},

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        asset_db_doc = document.dict(by_alias=True)

        return asset_db_doc

    @staticmethod
    def group_construct(name, entity_id, parent_id):

        document = Group(

            _id=entity_id,
            name=name,
            active=True,
            type="group",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="",
            components={},

            data={},

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        group_db_doc = document.dict(by_alias=True)

        return group_db_doc

    @staticmethod
    def task_construct(name, entity_id, task_type, parent_id):

        document = Task(

            _id=entity_id,
            name=name,
            active=True,
            type="task",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="",
            components={},

            task_type=task_type,
            artist="None",
            imports_from={},
            bid_days="",
            start_date="",
            end_date="",
            milestones={},
            worked_days="",
            previous_artists=[],

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        task_db_doc = document.dict(by_alias=True)

        return task_db_doc

    @staticmethod
    def work_session_construct(name, entity_id, version, parent_id):
        set_display_name = "__".join([parent_id, "work_file", Users.curr_user(), version])

        document = WorkFile(

            _id=entity_id,
            name=name,
            active=True,
            type="work_file",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="",
            components={},

            description="",
            parent_task="",
            version=version,
            session_content={},
            representation={},

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        work_file_doc = document.dict(by_alias=True)

        return work_file_doc

    def db_asset_construct(self, name, entity_id, parent_id, task_type):
        set_display_name = "_".join([name, f"_{task_type}"])

        document = DBAsset(

            _id=entity_id,
            name=name,
            active=True,
            type="db_asset",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="",
            components={},

            label=set_display_name,
            master_task_type=task_type,

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_doc = document.dict(by_alias=True)

        return db_asset_doc

    def db_asset_version_construct(self,
                                   name,
                                   entity_id: str,
                                   parent_id: str,
                                   version: str,
                                   status: str,
                                   ):

        set_display_name = "_".join(
            [self.context_handler.entity_name, f"_{self.context_handler.task_type}", f"_{version}"])

        document = DBAssetVersion(

            _id=entity_id,
            name=name,
            active=True,
            type="db_asset_file_component",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status=status,
            components={},

            label=set_display_name,
            db_asset_type="",
            description="",
            comments=[],
            version="",
            version_cnt=int(),

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_version_doc = document.dict(by_alias=True)

        return db_asset_version_doc

    def db_asset_file_component(self,
                                entity_id,
                                display_name: str,
                                visibility: bool,
                                file_ext: str,
                                parent_id: str,
                                output_file_path: str,
                                ) -> dict:

        document = DBAssetFileComponent(

            _id=entity_id,
            name=display_name,
            active=True,
            type="db_asset_file_component",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="",
            components={},

            label=display_name,
            file_extension=file_ext,
            file_path=output_file_path,
            visible=visibility,
            master_task_type=self.context_handler.task_type,

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_file_doc = document.dict(by_alias=True)

        return db_asset_file_doc

    def task_publish_construct(self, version: str = None):
        if version is None:
            version = DBVersionIncrease().db_main_pub_ver_increase()

        set_display_name = "_".join([self.context_handler.entity_name, self.context_handler.task_name, "main_publish", version])
        common_id = DbIds(context=self.context).get_main_pub_id(version)

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
