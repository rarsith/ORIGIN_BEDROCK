import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
# from pydantic import BaseModel

from origin.common_utils.json_utils import save_json
from origin.database.mongo_connection import MongoConnection

@dataclass
class SessionContext:
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

    def as_dict(self):
        """Converts the dataclass to a dict specifically for MongoDB."""
        data = asdict(self)

        # Swap 'id' for '_id'
        if "id" in data:
            data["_id"] = data.pop("id")

        return data


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
        context_data = self.session_context.as_dict()
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

    # def database_handler(self):
    #     return OriginDatabaseHandler(context=self)


class DatabaseConnections:
    def __init__(self, context: ContextHandler):
        self.__context = context

        self.__db = MongoConnection().origin_production_database()
        self.project_structure_collection = self.__db[self.__context.show_name]
        self.project_publishes_collection = self.__db[self.__context.project_publishes]
        self.project_control_collection = self.__db[self.__context.project_control]
        self.project_work_collection = self.__db[self.__context.project_work]


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
