from origin.common_utils.date_time import DateTime
from origin.common_utils.users import Users
from origin.database.mongo_connection import MongoConnection
from origin.envars.origin_envars import ContextHandler
from origin.database.schemas.actions import EntityDefaultSchemas
from origin.common_utils import version_increment as vup

from origin.database.entities.operators import (DBAssetVersion,
                                                DBAsset,
                                                WorkFile,
                                                Project,
                                                Asset,
                                                Group,
                                                Task,
                                                DBAssetFileComponent, AssetBreakdown, AssetBreakdownVersion, AssetStack,
                                                AssetStackVersion, DCCBaseModel, DCCVersion)
from origin.database.mongo import CollectionOperators, DBSet


class DbConstructors:

    def __init__(self, context: ContextHandler = None):
        self.context_handler = context

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

            show_type=project_type,
            show_code=project_code,
            show_settings={},

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        project_db_doc = document.model_dump(by_alias=True)

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

            definition=EntityDefaultSchemas().entry_definition.skeleton_schema,
            tasks=tasks,
            assignees={},
            assigned_to={},

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        asset_db_doc = document.model_dump(by_alias=True)

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

            data={},

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        group_db_doc = document.model_dump(by_alias=True)

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

        task_db_doc = document.model_dump(by_alias=True)

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

            description="",
            parent_task="",
            version=version,
            session_content={},
            representation={},

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        work_file_doc = document.model_dump(by_alias=True)

        return work_file_doc

    def db_asset_stream_construct(self, name, entity_id, parent_id):
        set_display_name = "_".join([name, f"stream"])

        document = DBAsset(

            _id=entity_id,
            name=name,
            active=True,
            type="db_asset_stream",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="",

            label=set_display_name,
            master_task_type='',
            db_asset_type="db_asset__stream",
            stacks=[],

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_doc = document.model_dump(by_alias=True)

        return db_asset_doc

    def db_asset_construct(self, parent_id, publish_type, task_type):
        from origin.database.entities.operators import get_db_asset_class

        parent_doc = self.context_handler.database_handler().get_db_asset_stream_document()

        parent_name = parent_doc.id.rsplit('.', 1)[1]
        db_asset_class = get_db_asset_class(publish_type)
        compiled_id = ".".join([self.context_handler.entity_id, publish_type, parent_name])

        parent_doc.operations().add_child(db_collection=self.context_handler.project_publishes, child_id=compiled_id)

        document = db_asset_class(
            _id=compiled_id,
            name=parent_name,
            active=True,
            # type="db_asset",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="",

            label="",
            master_task_type=task_type,
            stack_slot=publish_type,
            db_asset_type="db_asset",

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_doc = document.model_dump(by_alias=True)

        return db_asset_doc

    def db_asset_version_construct(self,
                                   parent_id: str,
                                   comment: list,
                                   status: str,
                                   ):

        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        parent_data = data_ops.entity_document(doc_id=parent_id)
        parent_doc = DBAsset(**parent_data)

        version_string, version = vup.version_up(parent_doc.version_cnt)
        parent_doc.operations().update_version_count(1)

        set_display_name = "_".join(
            [self.context_handler.entity_name,
             f"_{self.context_handler.task_type}",
             f"_{parent_doc.name}",
             f"_{version_string}"])

        entity_id = ".".join([parent_id, version_string])
        resolve_db_asset_type = "__".join([parent_doc.type, "asset_version"])

        parent_doc.operations().add_child(db_collection=self.context_handler.project_publishes, child_id=entity_id)

        document = DBAssetVersion(

            _id=entity_id,
            name=entity_id,
            active=True,
            type="publish",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status=status,

            label=set_display_name,
            db_asset_type="db_asset__version",
            parent_task_type=self.context_handler.task_type,
            parent_task_id=self.context_handler.task_id,
            description="",
            comments=[comment],
            version=version_string,
            version_cnt=version,
            components=[],

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_version_doc = document.model_dump(by_alias=True)

        return db_asset_version_doc

    def asset_breakdown_construct(self, parent_id):
        parent_name = parent_id.rsplit(".", 1)[1]
        compiled_id = ".".join([parent_id, "breakdown"])
        compiled_name = "__".join([parent_name, "breakdown"])

        parent_doc_data = self.context_handler.database_handler().get_db_document_by_id(db_collection=self.context_handler.show_name, doc_id=parent_id)
        parent_doc = Asset(**parent_doc_data)

        document = AssetBreakdown(
            _id=compiled_id,
            name=compiled_name,
            active=True,
            type="breakdown",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,

            db_asset_type="db_asset__breakdown",

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_breakdown_doc = document.model_dump(by_alias=True)

        parent_doc.operations().set_asset_breakdown(breakdown_id=compiled_id)

        return db_asset_breakdown_doc

    def asset_breakdown_version_construct(self, input_data: dict):
        compiled_parent_id = ".".join([self.context_handler.entity_id, "breakdown"])
        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        parent_data = data_ops.entity_document(doc_id=compiled_parent_id)
        parent_doc = DBAsset(**parent_data)

        version_string, version = vup.version_up(parent_doc.version_cnt)
        parent_doc.operations().update_version_count(1)

        set_display_name = "_".join(
            [self.context_handler.entity_name,
             "_breakdown",
             f"_{version_string}"])

        entity_id = ".".join([compiled_parent_id, version_string])
        parent_doc.operations().add_child(db_collection=self.context_handler.project_publishes, child_id=entity_id)

        document = AssetBreakdownVersion(

            _id=entity_id,
            name=entity_id,
            active=True,
            type="breakdown__version",
            parent=compiled_parent_id,
            children=[],
            origin_db_path=compiled_parent_id,

            label=set_display_name,
            db_asset_type="breakdown__version",
            version=version_string,
            version_cnt=version,
            data=input_data,

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        asset_breakdown_version_doc = document.model_dump(by_alias=True)

        return asset_breakdown_version_doc

    def asset_stack_construct(self, parent_id):
        parent_name = parent_id.rsplit(".", 1)[1]
        compiled_id = ".".join([parent_id, "asset_stack"])
        compiled_name = "__".join([parent_name, "asset_stack"])

        parent_doc_data = self.context_handler.database_handler().get_db_document_by_id(
            db_collection=self.context_handler.project_publishes, doc_id=parent_id)
        parent_doc = DBAsset(**parent_doc_data)

        document = AssetStack(
            _id=compiled_id,
            name=compiled_name,
            active=True,
            type="db_asset__stack",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,

            db_asset_type="db_asset__stack",

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_stack_doc = document.model_dump(by_alias=True)

        return db_asset_stack_doc

    def asset_stack_version_construct(self, input_data: dict):
        compiled_parent_id = ".".join([self.context_handler.db_asset_stream_id, "asset_stack"])
        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        parent_data = data_ops.entity_document(doc_id=compiled_parent_id)
        parent_doc = DBAsset(**parent_data)

        version_string, version = vup.version_up(parent_doc.version_cnt)
        parent_doc.operations().update_version_count(1)

        set_display_name = "_".join(
            [self.context_handler.entity_name,
             "asset_stack",
             f"_{version_string}"])

        entity_id = ".".join([compiled_parent_id, version_string])
        parent_doc.operations().add_child(db_collection=self.context_handler.project_publishes, child_id=entity_id)

        document = AssetStackVersion(

            _id=entity_id,
            name=entity_id,
            active=True,
            type="db_asset__stack_version",
            parent=compiled_parent_id,
            children=[],
            origin_db_path=compiled_parent_id,

            label=set_display_name,
            db_asset_type="db_asset__stack_version",
            version=version_string,
            version_cnt=version,
            data=input_data,

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        asset_breakdown_version_doc = document.model_dump(by_alias=True)

        return asset_breakdown_version_doc

    def db_asset_file_component(self,
                                visibility: bool,
                                file_ext: str,
                                parent_id: str,
                                file_path: str,
                                ) -> dict:
        from origin.common_utils.generate_uuid import generate_uuid
        from origin.database.entities.operators import get_file_component_class

        gen_uuid = generate_uuid()
        entity_id = ".".join([parent_id, gen_uuid])

        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        parent_data = data_ops.entity_document(doc_id=parent_id)
        parent_doc = DBAssetVersion(**parent_data)

        parent_doc.operations().add_child(db_collection=self.context_handler.project_publishes, child_id=entity_id)

        file_component_class = get_file_component_class(file_ext)

        document = file_component_class(

            _id=entity_id,
            name='',
            active=True,
            type="db_asset_file_component",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="DONE",

            # label=file_component_class.label,
            file_extension=file_ext,
            file_path=file_path,
            visible=visibility,
            master_task_type=self.context_handler.task_type,
            db_asset_type="db_asset__file_component",

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_file_doc = document.dict(by_alias=True)

        return db_asset_file_doc

    def db_asset_application(self, name, app_icon):
        compiled_id = ".".join([name, "application"])

        document = DCCBaseModel(
            _id=compiled_id,
            name=name,
            active=True,
            type="application",
            versions={},
            icon_path=app_icon,

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        application_doc = document.model_dump(by_alias=True)

        return application_doc

    def db_asset_version_application(self, parent_id=None, active=None, version_id=None, exec_path=None, exec_python=None, envars=None):
        applications__db = MongoConnection().origin_setup_database()

        document = DCCVersion(
            active=active,
            version=version_id,
            exec_path=exec_path,
            exec_python=exec_python,
            envars=envars,
        )

        application_version_doc = document.model_dump(by_alias=True)

        DBSet(database=applications__db,
              db_collection="Applications",
              entry_id=parent_id,
              attribute=fr"versions.{str(version_id)}").attribute_value(application_version_doc)


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
