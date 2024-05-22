import os
import json
import uuid
from pydantic import BaseModel

from typing import Optional

import o_database.mongo_connection


class OriginEnvironmentManager:

    def ensure_env_var(self, var_name, default_value):
        # Check if the environment variable exists
        if os.getenv(var_name) is None:
            # If not, set it to the default value
            os.environ[var_name] = default_value
            print(f"Environment variable '{var_name}' set to '{default_value}'")
        else:
            print(f"Environment variable '{var_name}' already exists with value '{os.getenv(var_name)}'")


origin_root = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK"  # path to be read from a config file
OriginEnvironmentManager().ensure_env_var("ORIGIN_ROOT", origin_root)


class SessionContext(BaseModel):
    session_filename: Optional[str] = None
    session_id: Optional[str] = None
    show_name: Optional[str] = None

    project_publishes: Optional[str] = None
    project_work: Optional[str] = None
    project_control: Optional[str] = None

    origin_path_hierarchy: Optional[str] = None
    entry_name: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    task_name: Optional[str] = None
    task_type: Optional[str] = None


class ContextHandler:

    def __init__(self):

        self.session_context = SessionContext()
        self.set_session()

    def resolve_path_to_file(self):
        origin_dev_root = os.getenv("ORIGIN_ROOT")
        save_path = os.path.join(origin_dev_root, "context_manager", "sessions")
        return save_path

    def set_session(self):
        self._session_id = str(uuid.uuid1())
        self.session_context.session_filename = ".".join([self._session_id, "env"])
        os.environ["BASE_APP_CURRENT_SESSION"] = self.session_context.session_filename
        self.session_context.session_id = self._session_id
        self.save_session()

    def end_session(self):
        session_filename = self.session_context.session_filename
        if session_filename and os.path.exists(session_filename):
            os.remove(session_filename)
            os.environ.pop("BASE_APP_CURRENT_SESSION", None)
            print(f"Session file {session_filename} deleted and environment variable cleared.")

    def load_session(self):
        session_filename = os.getenv("BASE_APP_CURRENT_SESSION")
        if session_filename and os.path.exists(session_filename):
            with open(session_filename, "r") as f:
                session_data = json.load(f)
                self.session_context = SessionContext(**session_data)

    def save_session(self):
        root_path = r"C:\Users\arsithra\PycharmProjects\ORIGIN_BEDROCK\context_manager"
        save_path = os.path.join(root_path, "sessions", self.session_context.session_filename)

        with open(save_path, "w") as f:
            json.dump(self.session_context.dict(), f)

    def update_context(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.session_context, key, value)
        self.save_session()

    # Getters and setters for session context properties
    @property
    def show_name(self):
        return self.session_context.show_name

    @show_name.setter
    def show_name(self, value):
        self.session_context.show_name = value

        self.session_context.origin_path_hierarchy = None
        self.session_context.entry_name = None
        self.session_context.entity_type = None
        self.session_context.task_name = None
        self.session_context.task_type = None

        self._update_project_connections()

        self.save_session()

    @property
    def project_publishes(self):
        return self.session_context.project_publishes

    @project_publishes.setter
    def project_publishes(self, value):
        self.session_context.project_publishes = value
        self.save_session()

    @property
    def project_work(self):
        return self.session_context.project_work

    @project_work.setter
    def project_work(self, value):
        self.session_context.project_work = value
        self.save_session()

    @property
    def project_control(self):
        return self.session_context.project_control

    @project_control.setter
    def project_control(self, value):
        self.session_context.project_control = value
        self.save_session()

    @property
    def origin_path_hierarchy(self):
        return self.session_context.origin_path_hierarchy

    @origin_path_hierarchy.setter
    def origin_path_hierarchy(self, value):
        resolve_path = self._update_hierarchy_path(value)
        self.session_context.origin_path_hierarchy = resolve_path

        self.session_context.entry_name = None
        self.session_context.entity_type = None
        self.session_context.task_name = None
        self.session_context.task_type = None

        self.save_session()

    @property
    def entry_name(self):
        return self.session_context.entry_name

    @entry_name.setter
    def entry_name(self, value):
        self.session_context.entry_name = value

        self.session_context.task_name = None
        self.session_context.task_type = None

        self.save_session()

    @property
    def entity_type(self):
        return self.session_context.entity_type

    @entity_type.setter
    def entity_type(self, value):
        self.session_context.entity_type = value
        self.save_session()

    @property
    def entity_id(self):
        return self.session_context.entity_id

    @entity_id.setter
    def entity_id(self, value):
        self.session_context.entity_id = value
        self.save_session()

    @property
    def task_name(self):
        return self.session_context.task_name

    @task_name.setter
    def task_name(self, value):
        self.session_context.task_name = value
        self.save_session()

    @property
    def task_type(self):
        return self.session_context.task_type

    @task_type.setter
    def task_type(self, value):
        self.session_context.task_name = value
        self.save_session()

    def _update_hierarchy_path(self, sel_items: list, delimiter=".", use_root=False):
        hierarchy = delimiter.join(sel_items)
        return hierarchy

    def _update_project_connections(self):
        self.project_publishes = "__".join([self.show_name, "PUBLISHES"])
        self.project_work = "__".join([self.show_name, "WORK"])
        self.project_control = "__".join([self.show_name, "CONTROL"])

    def resolve_to_full_context(self):
        """
        Returns FULL path, including current task
        """
        origin_context = ".".join(
            filter(None, [self.show_name, self.origin_path_hierarchy, self.entry_name, self.task_name]))
        return origin_context

    def resolve_to_base_context(self):
        """
        Returns FULL path, including current task
        """
        origin_context = ".".join(filter(None, [self.show_name, self.origin_path_hierarchy, self.entry_name]))
        return origin_context

    def resolve_to_master(self):
        """
        Returns he path to the asset, does not include the task
        """
        origin_context = ".".join(filter(None, [self.show_name, self.origin_path_hierarchy, self.entry_name]))
        return origin_context

    def resolve_entity_id(self):
        """
        Returns the composed ID for the entry: to be depricated and replaced
        and replaced with ObjectId()
        """
        resolve_id = self.resolve_to_master()
        return resolve_id


OriginEnvar = ContextHandler()


if __name__ == "__main__":

    # context_session.set_session()

    db_path = ["assets", "characters"]

    OriginEnvar.show_name = "New_Era"
    OriginEnvar.origin_path_hierarchy = db_path
    OriginEnvar.entry_name = "hulk"
    OriginEnvar.task_name = "modeling"

    # print(OriginEnvar.show_name)
    # print(OriginEnvar.origin_path_hierarchy)
    # print(OriginEnvar.entry_name)
    # print(OriginEnvar.task_name)
    #
    # print(OriginEnvar.session_context.__dict__)
    # print(os.getenv("BASE_APP_CURRENT_SESSION"))

    OriginEnvar.end_session()
