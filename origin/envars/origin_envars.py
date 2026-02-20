import os
import pprint
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

from origin.common_utils.json_utils import save_json
from origin.database.entities.operators import Project, Asset, Task, DBAsset, Group, AssetBreakdown, \
    AssetBreakdownVersion, AssetStack, AssetStackVersion, DBAssetVersion
from origin.database.mongo import CollectionOperators
from origin.database.mongo_connection import MongoConnection


class SessionContext(BaseModel):
    show_name: Optional[str] = None

    project_publishes: Optional[str] = None
    project_work: Optional[str] = None
    project_control: Optional[str] = None

    origin_path_hierarchy: Optional[str] = None
    entity_name: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    task_name: Optional[str] = None
    task_type: Optional[str] = None
    task_id: Optional[str] = None
    publish_id: Optional[str] = None

    db_asset_stream_id: Optional[str] = None

    db_asset_id: Optional[str] = None
    db_asset_type: Optional[str] = None
    db_asset_version_id: Optional[str] = None

    asset_breakdown_id: Optional[str] = None
    asset_breakdown_version_id: Optional[str] = None

    stack_id: Optional[str] = None
    stack_version_id: Optional[str] = None


class ContextHandler:

    def __init__(self):

        self.session_context = SessionContext()
        # self.set_session()

    def resolve_server_path(self):
        origin_dev_root = os.getenv("ORIGIN_PROJECTS_ROOT")
        save_path = os.path.join(origin_dev_root, self.show_name, self.origin_path_hierarchy, self.entity_name)
        return save_path

    def load_session(self, session_data):
        conform_lower_case = {k.lower(): v for k, v in session_data.items()}
        self.session_context = SessionContext(**conform_lower_case)
        self.session_context.entity_id = session_data['entity_id']

    def snapshot_session(self) -> dict:
        context_data = self.session_context.model_dump(by_alias=True)
        return context_data

    def session_to_disk(self):
        session_file = "last_session.json"

        origin_root = Path(os.getenv("ORIGIN_ROOT"))
        session_file_path = origin_root / Path("origin/config/sessions") / session_file

        session_data = self.snapshot_session()
        get_root_path = os.path.split(session_file_path)[0]

        save_json(get_root_path, data=session_data, target_file=session_file)


    ######################################################
    # Getters and setters for session context properties #
    ######################################################

    @property
    def show_name(self):
        return self.session_context.show_name

    @show_name.setter
    def show_name(self, value):
        self.session_context.show_name = value
        self.reset_to_project()
        self._update_project_connections()

    @property
    def project_publishes(self):
        return self.session_context.project_publishes

    @project_publishes.setter
    def project_publishes(self, value):
        self.session_context.project_publishes = value

    @property
    def project_work(self):
        return self.session_context.project_work

    @project_work.setter
    def project_work(self, value):
        self.session_context.project_work = value

    @property
    def project_control(self):
        return self.session_context.project_control

    @project_control.setter
    def project_control(self, value):
        self.session_context.project_control = value

    @property
    def origin_path_hierarchy(self):
        return self.session_context.origin_path_hierarchy

    @origin_path_hierarchy.setter
    def origin_path_hierarchy(self, value):
        self.session_context.origin_path_hierarchy = value

        self.session_context.entity_name = None
        self.session_context.task_name = None
        self.session_context.task_type = None

        self.session_context.db_asset_stream_id = None

        self.session_context.db_asset_id = None
        self.session_context.db_asset_type = None
        self.session_context.db_asset_version_id = None

        self.session_context.asset_breakdown_id = None
        self.session_context.asset_breakdown_version_id = None

        self.session_context.stack_id = None
        self.session_context.stack_version_id = None

    @property
    def entity_name(self):
        return self.session_context.entity_name

    @entity_name.setter
    def entity_name(self, value):
        self.session_context.entity_name = value

    @property
    def entity_type(self):
        return self.session_context.entity_type

    @entity_type.setter
    def entity_type(self, value):
        self.session_context.entity_type = value

    @property
    def entity_id(self):
        return self.session_context.entity_id

    @entity_id.setter
    def entity_id(self, value):
        self.session_context.entity_id = value
        self.resolve_entity_breakdown()

    @property
    def asset_breakdown_id(self):
        return self.session_context.asset_breakdown_id

    @asset_breakdown_id.setter
    def asset_breakdown_id(self, value):
        self.session_context.asset_breakdown_id = value

    @property
    def asset_breakdown_version_id(self):
        return self.session_context.asset_breakdown_version_id

    @asset_breakdown_version_id.setter
    def asset_breakdown_version_id(self, value):
        self.session_context.asset_breakdown_version_id = value

    @property
    def task_name(self):
        return self.session_context.task_name

    @task_name.setter
    def task_name(self, value):
        self.session_context.task_name = value

    @property
    def task_type(self):
        return self.session_context.task_type

    @task_type.setter
    def task_type(self, value):
        self.session_context.task_type = value

    @property
    def task_id(self):
        return self.session_context.task_id

    @task_id.setter
    def task_id(self, value):
        self.session_context.task_id = value

    @property
    def db_asset_stream_id(self):
        return self.session_context.db_asset_stream_id

    @db_asset_stream_id.setter
    def db_asset_stream_id(self, value):
        self.session_context.db_asset_stream_id = value
        # asset_id = self.compile_db_asset_id()
        # self.db_asset_id = asset_id

    @property
    def db_asset_id(self):
        return self.session_context.db_asset_id

    @db_asset_id.setter
    def db_asset_id(self, value):
        self.session_context.db_asset_id = value

    @property
    def db_asset_type(self):
        return self.session_context.db_asset_type

    @db_asset_type.setter
    def db_asset_type(self, value):
        self.session_context.db_asset_type = value

    @property
    def db_asset_version_id(self):
        return self.session_context.db_asset_version_id

    @db_asset_version_id.setter
    def db_asset_version_id(self, value):
        self.session_context.db_asset_version_id = value

    @property
    def stack_id(self):
        return self.session_context.stack_id

    @stack_id.setter
    def stack_id(self, value):
        self.session_context.stack_id = value

    @property
    def stack_version_id(self):
        return self.session_context.stack_version_id

    @stack_version_id.setter
    def stack_version_id(self, value):
        self.session_context.stack_version_id = value

    def get_entity_category(self):
        origin_path_hierarchy_elements = self.resolve_origin_path_hierarchy()[-1]
        return origin_path_hierarchy_elements


    ######################################################
    # Resolvers                                          #
    ######################################################

    def _update_project_connections(self):
        self.project_publishes = "__".join([self.show_name, "PUBLISHES"])
        self.project_work = "__".join([self.show_name, "WORK"])
        self.project_control = "__".join([self.show_name, "CONTROL"])

    def resolve_origin_path_hierarchy(self):
        """
        Returns: self.origin_path_hierarchy content split by delimiter
        """
        delimiter = "."
        if delimiter in self.origin_path_hierarchy:
            return self.origin_path_hierarchy.split(delimiter)
        else:
            return [self.origin_path_hierarchy]

    def resolve_entity_breakdown(self):
        self.session_context.asset_breakdown_id = ".".join([self.entity_id, "breakdown"])

    def resolve_to_full_context(self):
        if self.entity_type == "group":
            origin_context = ".".join(filter(None, [self.show_name,
                                                    self.origin_path_hierarchy,
                                                    ]))
        else:
            origin_context = ".".join(filter(None, [self.show_name,
                                                    self.origin_path_hierarchy,
                                                    self.entity_name,
                                                    self.task_name
                                                    ]))

        return origin_context

    def resolve_to_task_type_context(self):
        """
            Returns FULL path, until current task
        """
        if self.entity_type == "group":
            origin_context = ".".join(filter(None, [self.show_name,
                                                    self.origin_path_hierarchy,
                                                    self.task_type]))
        else:
            origin_context = ".".join(filter(None, [self.show_name,
                                                    self.origin_path_hierarchy,
                                                    self.entity_name,
                                                    self.task_type]))
        return origin_context

    def resolve_to_base_context(self):
        """
               Returns FULL path, until current entity
        """
        if self.entity_type == "group":
            origin_context = ".".join(filter(None, [self.show_name,
                                                    self.origin_path_hierarchy,
                                                    ]))
        else:
            origin_context = ".".join(filter(None, [self.show_name,
                                                    self.origin_path_hierarchy,
                                                    self.entity_name,
                                                    ]))

        return origin_context

    def resolve_to_master(self):
        """
        Returns he path to the asset, does not include the task
        """
        origin_context = ".".join(filter(None, [self.show_name, self.origin_path_hierarchy, self.entity_name]))
        return origin_context

    def resolve_entity_id(self):
        """
        Returns the composed ID for the entry: to be deprecated and replaced
        and replaced with ObjectId()
        """
        resolve_id = self.resolve_to_master()
        return resolve_id


    ######################################################
    # Resetters                                          #
    ######################################################

    def reset_to_project(self):
        self.session_context.origin_path_hierarchy = None
        self.session_context.entity_name = None
        self.session_context.entity_type = None
        self.session_context.task_name = None
        self.session_context.task_type = None
        self.session_context.task_id = None

        self.session_context.db_asset_stream_id = None

        self.session_context.db_asset_id = None
        self.session_context.db_asset_type = None
        self.session_context.db_asset_version_id = None

        self.session_context.asset_breakdown_id = None
        self.session_context.asset_breakdown_version_id = None

        self.session_context.stack_id = None
        self.session_context.stack_version_id = None

    def reset_to_entity(self):
        self.session_context.task_name = None
        self.session_context.task_type = None
        self.session_context.task_id = None

        self.session_context.db_asset_stream_id = None

        self.session_context.db_asset_id = None
        self.session_context.db_asset_type = None
        self.session_context.db_asset_version_id = None

        # self.session_context.asset_breakdown_id = None
        # self.session_context.asset_breakdown_version_id = None

        self.session_context.stack_id = None
        self.session_context.stack_version_id = None

    @staticmethod
    def convert_to_uppercases(input_data: dict) -> dict:
        return {k.upper(): v for k, v in input_data.items()}

    ######################################################
    # Database Handlers                                  #
    ######################################################

    def database_handler(self):
        return OriginDatabaseHandler(context=self)

    def version_control(self):
        return OriginVersionHandler(context=self)

    # def os_paths_handler(self):
    #     return OriginOSPathHandler(context=self, file_format=None)

class DatabaseConnections:
    def __init__(self, context: ContextHandler):
        self.__context = context

        self.__db = MongoConnection().origin_production_database()
        self.project_structure_collection = self.__db[self.__context.show_name]
        self.project_publishes_collection = self.__db[self.__context.project_publishes]
        self.project_control_collection = self.__db[self.__context.project_control]
        self.project_work_collection = self.__db[self.__context.project_work]


class OriginDatabaseHandler:
    def __init__(self, context: ContextHandler):
        self.__context = context

        self.__db = MongoConnection().origin_production_database()
        self.__project_structure_collection = self.__db[self.__context.show_name]
        self.__project_publishes_collection = self.__db[self.__context.project_publishes]
        self.__project_control_collection = self.__db[self.__context.project_control]
        self.__project_work_collection = self.__db[self.__context.project_work]

    def get_db_document_by_id(self, db_collection, doc_id):
        db_ops = CollectionOperators(db_collection=db_collection)
        document = db_ops.entity_document(doc_id=doc_id)
        return document

    # def get_document_by_id(self, doc_id, db_collection: DatabaseConnections):
    #     db_ops = None
    #     if db_collection == DatabaseConnections.project_structure_collection:
    #         db_ops = CollectionOperators(db_collection=self.__context.show_name)
    #     elif db_collection == DatabaseConnections.project_publishes_collection:
    #         db_ops = CollectionOperators(db_collection=self.__context.project_publishes)
    #     elif db_collection == DatabaseConnections.project_control_collection:
    #         db_ops = CollectionOperators(db_collection=self.__context.project_control)
    #     elif db_collection == DatabaseConnections.project_work_collection:
    #         db_ops = CollectionOperators(db_collection=self.__context.project_work)
    #
    #     document = db_ops.entity_document(doc_id=doc_id)
    #     return document

    def get_project_document(self) -> Project:
        project_doc = self.get_db_document_by_id(db_collection=self.__context.show_name,
                                                 doc_id=self.__context.show_name)
        return Project(**project_doc)

    def get_asset_document(self) -> Asset:
        entity_doc = self.get_db_document_by_id(db_collection=self.__context.show_name,
                                                doc_id=self.__context.entity_id)

        if self.__context.entity_type == "group":
            return Group(**entity_doc)
        else:
            return Asset(**entity_doc)

    def get_task_document(self) -> Task:
        task_doc = self.get_db_document_by_id(db_collection=self.__context.show_name,
                                              doc_id=self.__context.task_id)
        return Task(**task_doc)

    def get_db_asset_stream_document(self):
        if self.__context.db_asset_stream_id:
            db_asset_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                                      doc_id=self.__context.db_asset_stream_id)

            return DBAsset(**db_asset_doc)
        else:
            return None

    def get_db_asset_document(self):
        if self.__context.db_asset_id is not None:
            db_asset_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                                      doc_id=self.__context.db_asset_id)

            if db_asset_doc is not None:
                return DBAsset(**db_asset_doc)
            else:
                return None

    def get_stream_breakdown(self):
        if self.__context.asset_breakdown_id:
            breakdown_doc_data = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                                            doc_id=self.__context.asset_breakdown_id)
            return AssetBreakdown(**breakdown_doc_data)
        else:
            return None

    def get_db_asset_version_document(self):
        if self.__context.db_asset_version_id is not None:
            db_asset_version_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                                              doc_id=self.__context.db_asset_version_id)

            if db_asset_version_doc is not None:
                return DBAssetVersion(**db_asset_version_doc)
            else:
                return None

    def get_asset_streams(self):
        db_ops = CollectionOperators(db_collection=self.__context.show_name)
        entity_doc = db_ops.entity_document(doc_id=self.__context.entity_id)
        if entity_doc is not None:
            asset_doc = Asset(**entity_doc)

            curr_asset_type = self.__context.entity_type
            stack_steams = asset_doc.stack_streams

            if curr_asset_type != "group":
                if stack_steams is None:
                    return {}
                if len(stack_steams) == 0:
                    return {}
                else:
                    return stack_steams

    def get_asset_breakdown_latest_version(self):
        breakdown_doc = self.get_stream_breakdown()
        if breakdown_doc is not None:
            latest_version_doc_data = breakdown_doc.operations().get_latest_version()
            if latest_version_doc_data is not None:
                return AssetBreakdownVersion(**latest_version_doc_data)
            else:
                return None
        else:
            return None

    def get_asset_breakdown_context_slots(self):
        breakdown_latest_version = self.get_asset_breakdown_latest_version()
        if breakdown_latest_version is not None:
            breakdown_data = breakdown_latest_version.data
            asset_stream_id = self.__context.db_asset_stream_id
            clean_asset_stream_id = asset_stream_id.replace(".", "__")
            context_slots = breakdown_data["db_assets"]
            return context_slots
        else:
            return None

    def get_stack_document(self):
        stack_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                               doc_id=self.__context.stack_id)
        if stack_doc is not None:
            return AssetStack(**stack_doc)
        else:
            return None

    def get_stack_latest_version(self, with_status=None):
        stack_doc = self.get_stack_document()
        if stack_doc is not None:
            latest_version_doc_data = stack_doc.operations().get_latest_version(db_asset_type="db_asset__stack_version",
                                                                                with_status=with_status)
            if latest_version_doc_data is not None:
                return AssetStackVersion(**latest_version_doc_data)
            else:
                return None
        else:
            return None

    def collection(self):
        pass  # use of Create Module

    def get_stream_stack(self):
        db_ops = CollectionOperators(db_collection=self.__context.project_publishes)

        if self.__context.db_asset_stream_id is not None:
            stream_stack_db_asset_id = self.__context.db_asset_stream_id + "." + "asset_stack"
            stack_doc = db_ops.entity_document(doc_id=stream_stack_db_asset_id)
            return stack_doc

        else:
            return None

    def get_current_stack_version(self):
        db_ops = CollectionOperators(db_collection=self.__context.project_publishes)
        stack_doc = self.get_stream_stack()

        if stack_doc is not None:
            current_doc = db_ops.get_current_version(_id={"$regex": f"^{stack_doc['_id']}"})
            if len(current_doc) != 0:
                return current_doc[0]
            else:
                return None
        else:
            return None

    def get_current_stack_slots(self):
        extract_version = self.get_current_stack_version()
        if extract_version is not None:
            return extract_version["data"]
        else:
            return None

    def get_current_db_asset_version(self,  db_doc_obj=None):
        """

        Returns: database document of the current asset version that has one of the approved class statuses
        It will return None if there is no current version
        Uses the db_asset_id parent to get all children db_asset_versions and resolves to the current version

        """
        db_ops = CollectionOperators(db_collection=self.__context.project_publishes)

        doc_id = None

        if db_doc_obj is not None:
            if isinstance(db_doc_obj, DBAssetVersion) or isinstance(db_doc_obj, DBAsset) or isinstance(db_doc_obj, Asset):
                doc_id = db_doc_obj.id
            if isinstance(db_doc_obj, str):
                doc_id = db_doc_obj
            if isinstance(db_doc_obj, dict):
                doc_id = db_doc_obj["_id"]


            if doc_id is not None:
                version_parent = doc_id.rsplit(".", 1)[0]
                current_doc = db_ops.get_current_version(_id={"$regex": f"^{version_parent}"} )
                if len(current_doc) != 0:
                    return current_doc[0]
                else:
                    return None
            else:
                return None

        current_doc = db_ops.get_current_version(_id={"$regex": f"^{self.__context.db_asset_id}"})
        print(current_doc)
        if len(current_doc) != 0:
            return current_doc[0]
        else:
            return None


class OriginVersionHandler:
    def __init__(self, context: ContextHandler):
        self.__context = context


if __name__ == "__main__":
    context_sample = {'show_name': 'New_State',
                      'project_publishes': 'New_State__PUBLISHES',
                      'project_work': 'New_State__WORK',
                      'project_control': 'New_State__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'yellow_hulk',
                      'entity_type': 'asset',
                      'entity_id': 'New_State.assets.chr.yellow_hulk',
                      'task_name': "modeling",
                      'task_type': "modeling"}

    con_han = ContextHandler()
    con_han.load_session(context_sample)
    xx = con_han.snapshot_session()
    print(xx)
