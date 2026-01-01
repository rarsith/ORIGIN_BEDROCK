from origin.common_utils.date_time import DateTime
from origin.common_utils.users import Users
from origin.database.mongo_connection import MongoConnection
from origin.database.priorities import DbPriorities
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
from origin.database.statuses import DbVersionStatuses, DbTaskStatuses


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
        creation_status = DbTaskStatuses.not_started
        creation_priority = DbPriorities.normal

        document = Task(

            _id=entity_id,
            name=name,
            active=True,
            type="task",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status=creation_status,

            task_type=task_type,
            priority=creation_priority,
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
            type="db_asset__stream",
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

        # try:
        parent_doc.operations().add_child(db_collection=self.context_handler.project_publishes, child_id=compiled_id)
        # except:
        #     pass

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
        publish_type = parent_doc.id.split(".")[-2]

        set_display_name = "_".join(
            [self.context_handler.entity_name,
             f"_{self.context_handler.task_name}",
             f"_{publish_type}",
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
        parent_name_split = parent_id.rsplit(".", 1)[0]
        compiled_id = ".".join([parent_name_split, "breakdown"])
        compiled_name = "__".join([parent_name, "breakdown"])

        parent_doc_data = self.context_handler.database_handler().get_db_document_by_id(
                                                                                        db_collection=self.context_handler.project_publishes,
                                                                                        doc_id=parent_id
                                                                                        )

        parent_doc = Asset(**parent_doc_data)

        document = AssetBreakdown(
            _id=compiled_id,
            name=compiled_name,
            active=True,
            type="db_asset__breakdown",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,

            db_asset_type="db_asset__breakdown",

            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users().curr_user(),
        )

        db_asset_breakdown_doc = document.model_dump(by_alias=True)

        parent_doc.operations().set_stream_breakdown(breakdown_id=compiled_id)

        return db_asset_breakdown_doc

    def asset_breakdown_version_construct(self, input_data: dict):
        compiled_parent_id = ".".join([self.context_handler.db_asset_stream_id, "breakdown"])
        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        parent_data = data_ops.entity_document(doc_id=compiled_parent_id)
        parent_doc = DBAsset(**parent_data)

        version_string, version = vup.version_up(parent_doc.version_cnt)
        parent_doc.operations().update_version_count(1)

        set_display_name = "_".join(
            [self.context_handler.db_asset_stream_id,
             "__breakdown",
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

    def compile_entity_stack_input_data(self):
        version_statuses = DbVersionStatuses()
        statuses_priority = [version_statuses.approved_internal, version_statuses.wip]

        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        all_breakdown_slots = self.context_handler.database_handler().get_asset_breakdown_latest_version()
        context_slots = all_breakdown_slots.data

        breakdown_data = []
        stack_resolved_data = {}
        if context_slots is not None:

            for db_stream in context_slots:
                stack_resolved_data[db_stream] = {}
                for slot, db_asset_id in context_slots["db_assets"].items():
                    stack_resolved_data[db_stream][slot] = ""

                    db_asset_db_doc = data_ops.entity_document(doc_id=db_asset_id)
                    db_asset_data = DBAsset(**db_asset_db_doc)

                    for status in statuses_priority:
                        latest_version_with_status = db_asset_data.operations().get_latest_version(with_status=status)
                        collected_version = latest_version_with_status[0] if latest_version_with_status else None
                        if collected_version is not None and stack_resolved_data[db_stream][slot] == "":
                            stack_resolved_data[db_stream].update({slot: collected_version["_id"]})

            return stack_resolved_data
        else:
            return None

    def compile_stack_input_data(self):
        from origin.database.statuses import DbVersionStatuses

        version_statuses = DbVersionStatuses()
        statuses_priority = [version_statuses.approved_internal, version_statuses.wip, ]

        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)

        context_slots = None

        if self.context_handler.db_asset_stream_id is not None:
            context_slots = self.context_handler.database_handler().get_asset_breakdown_context_slots()

        stack_resolved_data = {}
        if context_slots is not None:
            for slot, db_asset_id in context_slots.items():
                stack_resolved_data[slot] = ''

                db_asset_db_doc = data_ops.entity_document(doc_id=db_asset_id)
                db_asset_data = DBAsset(**db_asset_db_doc)

                for status in statuses_priority:
                    latest_version_with_status = db_asset_data.operations().get_latest_version(with_status=status)
                    collected_version = latest_version_with_status[0] if latest_version_with_status else None
                    if collected_version is not None and stack_resolved_data[slot] == "":
                        stack_resolved_data[slot] = collected_version["_id"]

            return stack_resolved_data
        else:
            return None

    def stack_same_data_check(self) -> bool:
        current_breakdown_resolve = self.compile_stack_input_data()
        from origin.database.statuses import DbVersionStatuses
        version_statuses = DbVersionStatuses()

        statuses_priority = [version_statuses.approved_internal,
                             version_statuses.wip, ]

        compile_stack_id = ".".join([self.context_handler.db_asset_stream_id, "asset_stack"])
        self.context_handler.stack_id = compile_stack_id

        stack_db_doc = self.context_handler.database_handler().get_stack_document()

        first_stack_version = stack_db_doc.version_cnt
        if first_stack_version == 0:
            return False

        gathered_stack_doc = {}
        if current_breakdown_resolve is not None:
            for status in statuses_priority:
                latest_version_with_status = stack_db_doc.operations().get_latest_version(with_status=status)
                collected_version = latest_version_with_status[0] if latest_version_with_status else None

                if collected_version is not None:
                    gathered_stack_doc.update(collected_version)
                    break
                else:
                    continue

            if gathered_stack_doc:
                return current_breakdown_resolve == gathered_stack_doc["data"]
            else:
                return False

        else:
            return False

    def asset_stack_version_construct(self, status, input_slots: dict = None):
        compiled_parent_id = ".".join([self.context_handler.db_asset_stream_id, "asset_stack"])
        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        parent_data = data_ops.entity_document(doc_id=compiled_parent_id)
        parent_doc = DBAsset(**parent_data)

        version_string, version = vup.version_up(parent_doc.version_cnt)
        parent_doc.operations().update_version_count(1)

        set_display_name = "__".join(
            [self.context_handler.entity_name,
             "stack",
             parent_doc.name,
             f"_{version_string}"])

        entity_id = ".".join([compiled_parent_id, version_string])
        parent_doc.operations().add_child(db_collection=self.context_handler.project_publishes, child_id=entity_id)

        if input_slots is None:
            input_data = self.compile_stack_input_data()
        else:
            input_data = input_slots

        document = AssetStackVersion(
            _id=entity_id,
            name=entity_id,
            active=True,
            type="db_asset__stack_version",
            parent=compiled_parent_id,
            children=[],
            status=status,
            origin_db_path=compiled_parent_id,
            parent_task_type="origin_pipe",

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
                                component_parent_id: str = None

                                ) -> dict:
        from origin.common_utils.generate_uuid import generate_uuid
        from origin.database.entities.operators import get_file_component_class

        gen_uuid = generate_uuid()
        entity_id = ".".join([parent_id, gen_uuid])

        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        parent_data = data_ops.entity_document(doc_id=parent_id)
        parent_doc = DBAssetVersion(**parent_data)

        parent_doc.operations().add_child(db_collection=self.context_handler.project_publishes, child_id=entity_id)

        if component_parent_id is not None:
            component_parent_data = data_ops.entity_document(doc_id=component_parent_id)
            component_parent_doc = DBAssetVersion(**component_parent_data)
            component_parent_doc.operations().add_component(component_id=entity_id)

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

    def db_asset_custom_file_component(self,
                                       visibility: bool,
                                       file_ext: str,
                                       parent_id: str,
                                       file_path: str,
                                       component_parent_id: str = None,
                                       label=None

                                       ) -> dict:
        from origin.common_utils.generate_uuid import generate_uuid

        gen_uuid = generate_uuid()
        entity_id = ".".join([parent_id, gen_uuid])

        data_ops = CollectionOperators(db_collection=self.context_handler.project_publishes)
        parent_data = data_ops.entity_document(doc_id=parent_id)
        parent_doc = DBAssetVersion(**parent_data)

        parent_doc.operations().add_child(db_collection=self.context_handler.project_publishes, child_id=entity_id)

        if component_parent_id is not None:
            component_parent_data = data_ops.entity_document(doc_id=component_parent_id)
            component_parent_doc = DBAssetVersion(**component_parent_data)
            component_parent_doc.operations().add_component(component_id=entity_id)

        document = DBAssetFileComponent(
            _id=entity_id,
            name='',
            active=True,
            type="db_asset_file_component",
            parent=parent_id,
            children=[],
            origin_db_path=parent_id,
            status="DONE",

            label=label,
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

    def db_asset_version_application(self, parent_id=None, active=None, version_id=None, exec_path=None,
                                     exec_python=None, envars=None):
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
    context_sample = {'show_name': 'Black_Rock',
                      'project_publishes': 'Black_Rock__PUBLISHES',
                      'project_work': 'Black_Rock__WORK',
                      'project_control': 'Black_Rock__CONTROL',
                      'origin_path_hierarchy': 'assets.characters',
                      'entity_name': 'tafar',
                      'entity_id': 'Black_Rock.assets.characters.tafar',
                      'asset_breakdown_id': 'Black_Rock.assets.characters.tafar.tafar_MAIN.breakdown',
                      'entity_type': 'asset',
                      'task_name': "modeling",
                      'task_type': "modeling",
                      'task_id': "Black_Rock.assets.characters.tafar.modeling",
                      'db_asset_id': 'Black_Rock.assets.characters.tafar.geometry.tafar_MAIN',
                      'db_asset_stream_id': 'Black_Rock.assets.characters.tafar.tafar_MAIN',
                      'stack_id': 'Black_Rock.assets.characters.tafar.tafar_MAIN.asset_stack',
                      }

    context_class = ContextHandler()
    context_class.load_session(session_data=context_sample)

    xx = DbConstructors(context=context_class)
    zzz = xx.asset_breakdown_construct(parent_id="Green_Rock.assets.characters.tafar.tafar_WWWW.asset_stack")
    print(zzz)
    # doc_data =
    # print(doc_data)
