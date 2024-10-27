import os
from typing import Optional
from pydantic import BaseModel

# from origin.database.entities.actions import Create
from origin.database.entities.operators import Project, Asset, Task, DBAsset
from origin.database.mongo import CollectionOperators


# from origin.paths.output_paths import OriginOSPathHandler


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
    db_asset_version_id: Optional[str] = None
    stack_id: Optional[str] = None


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

    def snapshot_session(self) -> dict:
        context_data = self.session_context.dict(by_alias=True)
        return context_data

    # Getters and setters for session context properties
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
        self.session_context.db_asset_version_id = None

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

    @property
    def db_asset_id(self):
        return self.session_context.db_asset_id

    @db_asset_id.setter
    def db_asset_id(self, value):
        self.session_context.db_asset_id = value

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

    def get_entity_category(self):
        origin_path_hierarchy_elements = self.resolve_origin_path_hierarchy()[-1]
        return origin_path_hierarchy_elements

    def _update_project_connections(self):
        self.project_publishes = "__".join([self.show_name, "PUBLISHES"])
        self.project_work = "__".join([self.show_name, "WORK"])
        self.project_control = "__".join([self.show_name, "CONTROL"])

    def compile_db_asset_id(self):
        stream_name = self.db_asset_stream_id.rsplit(".", 1)[1]
        db_asset_id = ".".join([self.entity_id, self.task_type, stream_name])
        return db_asset_id

    def resolve_origin_path_hierarchy(self):
        """
        Returns: self.origin_path_hierarchy content split by delimiter
        """
        delimiter = "."
        if delimiter in self.origin_path_hierarchy:
            return self.origin_path_hierarchy.split(delimiter)
        else:
            return [self.origin_path_hierarchy]

    def resolve_to_full_context(self):
        origin_context = ".".join(
            filter(None, [self.show_name, self.origin_path_hierarchy, self.entity_name, self.task_name, self.db_asset_id]))
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

    def reset_to_project(self):
        self.session_context.origin_path_hierarchy = None
        self.session_context.entity_name = None
        self.session_context.entity_type = None
        self.session_context.task_name = None
        self.session_context.task_type = None
        self.session_context.task_id = None
        self.session_context.db_asset_stream_id = None
        self.session_context.db_asset_id = None
        self.session_context.db_asset_version_id = None

    def reset_to_entity(self):
        self.session_context.task_name = None
        self.session_context.task_type = None
        self.session_context.task_id = None
        self.session_context.db_asset_stream_id = None
        self.session_context.db_asset_id = None
        self.session_context.db_asset_version_id = None

    @staticmethod
    def convert_to_uppercases(input_data: dict) -> dict:
        return {k.upper(): v for k, v in input_data.items()}

    def database_handler(self):
        return OriginDatabaseHandler(context=self)

    def version_control(self):
        return OriginVersionHandler(context=self)

    # def os_paths_handler(self):
    #     return OriginOSPathHandler(context=self, file_format=None)


class OriginDatabaseHandler:
    def __init__(self, context: ContextHandler):
        self.__context = context

    def get_db_document_by_id(self, db_collection, doc_id):
        db_ops = CollectionOperators(db_collection=db_collection)
        document = db_ops.entity_document(doc_id=doc_id)
        return document

    def get_project_document(self) -> Project:
        project_doc = self.get_db_document_by_id(db_collection=self.__context.show_name,
                                                 doc_id=self.__context.show_name)
        return Project(**project_doc)

    def get_asset_document(self) -> Asset:
        entity_doc = self.get_db_document_by_id(db_collection=self.__context.show_name,
                                                doc_id=self.__context.entity_id)
        return Asset(**entity_doc)

    def get_task_document(self) -> Task:
        task_doc = self.get_db_document_by_id(db_collection=self.__context.show_name,
                                              doc_id=self.__context.task_id)
        return Task(**task_doc)



    def get_db_asset_document(self):
        if self.__context.db_asset_id:
            db_asset_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                                      doc_id=self.__context.db_asset_id)

            return DBAsset(**db_asset_doc)
        else:
            return None

    def get_stack_document(self):
        stack_doc = self.get_db_document_by_id(db_collection=self.__context.project_publishes,
                                               doc_id=self.__context.stack_id)
        return stack_doc

    # def create(self):
    #     return Create(context=self.context)

    def collection(self):
        pass  # use of Create Module


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
    xx = con_han.resolve_origin_path_hierarchy()
    print(xx[-1])
