import os
import json
import uuid
from pydantic import BaseModel

from typing import Optional

import o_database.mongo_connection
from o_database.entities.Xoperators import Group, Asset, Project, Task


class OriginEnvironmentManager:

    def ensure_env_var(self, var_name, default_value):
        # Check if the environment variable exists
        if os.getenv(var_name) is None:
            # If not, set it to the default value
            os.environ[var_name] = default_value
            print(f"Environment variable '{var_name}' set to '{default_value}'")
        else:
            print(f"Environment variable '{var_name}' already exists with value '{os.getenv(var_name)}'")


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


class ContextHandler:


    def __init__(self):

        self.session_context = SessionContext()
        # self.set_session()

    def get_entity_class(self):
        if self.entity_type == "group":
            return Group()
        if self.entity_type == "asset":
            return Asset()
        if self.entity_type == "project":
            return Project()
        if self.entity_type == "task":
            return Task()

    def resolve_server_path(self):
        origin_dev_root = os.getenv("ORIGIN_ROOT")
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

        self.session_context.origin_path_hierarchy = None
        self.session_context.entity_name = None
        self.session_context.entity_type = None
        self.session_context.task_name = None
        self.session_context.task_type = None

        self._update_project_connections()

        # self.save_session()

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
        # resolve_path = self._update_hierarchy_path(value)
        self.session_context.origin_path_hierarchy = value

        self.session_context.entity_name = None
        self.session_context.task_name = None
        self.session_context.task_type = None

        # self.save_session()

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

    def _update_project_connections(self):
        self.project_publishes = "__".join([self.show_name, "PUBLISHES"])
        self.project_work = "__".join([self.show_name, "WORK"])
        self.project_control = "__".join([self.show_name, "CONTROL"])

    def resolve_to_full_context(self):
        """
        Returns FULL path, including current task
        """
        origin_context = ".".join(
            filter(None, [self.show_name, self.origin_path_hierarchy, self.entity_name, self.task_type]))
        return origin_context

    def resolve_to_base_context(self):
        """
        Returns FULL path, including current task
        """
        origin_context = ".".join(filter(None, [self.show_name, self.origin_path_hierarchy, self.entity_name]))
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

    def convert_to_uppercases(self, input_data: dict) -> dict:
        return {k.upper(): v for k, v in input_data.items()}


OriginEnvar = ContextHandler()


if __name__ == "__main__":

    # context_session.set_session()

    db_path = ["assets", "characters"]

    OriginEnvar.show_name = "New_Era"
    OriginEnvar.origin_path_hierarchy = db_path
    OriginEnvar.entity_name = "hulk"
    OriginEnvar.task_name = "modeling"

    # print(OriginEnvar.show_name)
    # print(OriginEnvar.origin_path_hierarchy)
    # print(OriginEnvar.entity_name)
    # print(OriginEnvar.task_name)
    #
    context_data_details = OriginEnvar.snapshot_session()
    print(context_data_details)
    # print(context_data_details)
    # print(os.getenv("BASE_APP_CURRENT_SESSION"))

    # OriginEnvar.end_session()

    context = ContextHandler()
    context.load_session(context_data_details)
    print(context.resolve_to_full_context())
    print(context.resolve_to_base_context())
