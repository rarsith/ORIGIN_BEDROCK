import os
import time
from enum import Enum
from pathlib import Path

from origin.common_utils.users import Users
from origin.envars.origin_envars import ContextHandler
from origin.database.entities.operators import get_file_component_class
from origin.common_utils.users import Users
from origin.common_utils.generate_uuid import generate_uuid

import logging

logger = logging.getLogger(__name__)

def wait_for_file(path, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(path):
            try:
                with open(path, "r"):
                    return True
            except IOError:
                pass
        time.sleep(1.0)
    return False

class WorkBranches:
    ROOT = "work"
    EXCHANGE_BRANCH = "exchange"
    SCENE_FILES_BRANCH = "scene_files"
    WORKSPACE_BRANCH = "workspace"
    CACHES_BRANCH = "caches"


class PublishBranches:
    ROOT = "publishes"
    TEMP_PUBLISH_ROOT = "data"
    DATA_BRANCH = "data"
    IMAGES_BRANCH = "images"
    QUICKTIME_BRANCH = "quicktime"


class OriginOSPathHandler:
    temp_publish_data_root = "data"
    temp_publish_data = "tmp"
    publishes_root = "publishes"
    user_work_root = "work"

    branch_pub_data = "data"
    branch_pub_images = "images"
    branch_pub_quicktime = "quicktime"

    branch_user_exchange = "exchange"
    branch_user_scene_files = "scene_files"
    branch_user_workspace = "workspace"
    branch_user_caches = "caches"

    def __init__(self, context = None, file_format=None, compile_next_version=True, compile_filename=True):
        self.__context_handler = context
        self.origin_projects_root = Path(os.getenv("ORIGIN_PROJECTS_ROOT"))

        if isinstance(self.__context_handler, dict):
            self.__context_handler = ContextHandler()
            self.__context_handler.load_session(context)

        if self.__context_handler is not None:
            self.__origin_path_elements = self.__context_handler.resolve_origin_path_hierarchy()
            self.__category_name = self.__context_handler.get_entity_category()
            self.__db_asset_doc = self.__context_handler.database_handler().get_db_asset_document()

        self.__version_string = None
        self.output_file_name = None
        self.file_format = file_format

        if compile_next_version:
            self.__compile_next_version()
        if compile_filename:
            self.__compile_file_name()

    def __compile_next_version(self):
        if self.__db_asset_doc:
            self.__version_string, version = self.__db_asset_doc.operations().get_version_cnt()
            return self.__version_string

    def __compile_server_db_asset_version_dir_name(self):
        server_db_asset_version_name = "__".join([self.__category_name,
                                                  self.__context_handler.entity_name,
                                                  self.__db_asset_doc.name,
                                                  self.__version_string])
        return server_db_asset_version_name

    def __compile_server_db_asset_dir_name(self):
        server_db_asset_name = "__".join([self.__db_asset_doc.type,
                                          self.__context_handler.entity_name,
                                          self.__db_asset_doc.name])
        return server_db_asset_name

    def __compile_user_work_dir(self):
        get_user = Users().curr_user()
        work_dir = "_".join([self.user_work_root, get_user])

        return work_dir

    def __compile_file_name(self):
        if self.__db_asset_doc:
            self.output_file_name = "__".join([self.__category_name,
                                               self.__context_handler.entity_name,
                                               self.__db_asset_doc.name,
                                               self.__version_string])
            return self.output_file_name

    def __compile_file_parent_dir_name(self):
        if self.file_format:
            file_component_class = get_file_component_class(self.file_format)
            file_component = file_component_class()
            return file_component.label
        else:
            return None

    def __base_path(self):
        task_level = self.__context_handler.resolve_to_task_type_context()
        path_entities = task_level.split(".")

        return path_entities

    def __temp_publish_path(self):
        work_pub_tmp_path = self.work_base_path()
        work_pub_tmp_path.append(self.temp_publish_data_root)

        return work_pub_tmp_path

    def __publish_db_asset_version_branch(self, branch_dir_name):
        pub_path = self.__publish_base_path()
        pub_path.append(branch_dir_name)
        pub_path.append(self.__compile_server_db_asset_dir_name())
        pub_path.append(self.__compile_server_db_asset_version_dir_name())
        pub_path.append(self.__compile_file_parent_dir_name())

        return pub_path

    def __temp_publish_db_asset_version_branch(self):
        temp_pub_path = self.__temp_publish_path()
        temp_pub_path.append(self.__compile_server_db_asset_dir_name())
        temp_pub_path.append(self.__compile_server_db_asset_version_dir_name())
        temp_pub_path.append(self.__compile_file_parent_dir_name())

        return temp_pub_path

    def __work_db_asset_version_branch(self, branch_dir_name=None):
        if branch_dir_name is not None:
            work_path = self.work_base_path()
            work_path.append(branch_dir_name)
            return work_path
        else:
            return self.work_base_path()

    def __publish_base_path(self):
        publish_base_path = self.__base_path()
        publish_base_path.append(self.publishes_root)

        return publish_base_path

    def work_base_path(self, as_path=False, abs_path=False):
        base_path = self.__base_path()
        base_path.append(self.__compile_user_work_dir())

        if not as_path:
            return base_path
        elif as_path and abs_path:
            resolved_path = os.path.join(self.origin_projects_root, *base_path)
            return resolved_path

    def publish_path(self, branch_dir_name=None, create_dir=False, relative=False):
        publish_path_elements = self.__publish_db_asset_version_branch(branch_dir_name=branch_dir_name)
        return self.compose_path(path_elements=publish_path_elements, create_dirs=create_dir, relative=relative)

    def temp_publish_path(self, create_dir=False, relative=False):
        temp_publish_path_elements = self.__temp_publish_db_asset_version_branch()
        return self.compose_path(path_elements=temp_publish_path_elements, create_dirs=create_dir, relative=relative)

    def doci_incoming_path(self):
        doci_root = os.getenv('ORIGIN_DOCI_ROOT')
        incoming = Path(doci_root) / '_incoming'

        return incoming

    def doci_temp_path(self):
        doci_root = os.getenv('ORIGIN_DOCI_ROOT')
        temp = Path(doci_root) / '__tmp__'

        return temp

    def doci_file_name(self):
        uuid = generate_uuid()
        user = Users.curr_user()
        if self.__db_asset_doc:
            doci_file_name = "__".join(['doci_pub',
                                        self.__category_name,
                                        self.__context_handler.entity_name,
                                        self.__db_asset_doc.name,
                                        user,
                                        self.__version_string,
                                        uuid
                                        ]
                                       )


            return f"{doci_file_name}.json"

    def work_path(self, branch_dir_name=None, create_dir=False, relative=False):
        work_path_elements = self.__work_db_asset_version_branch(branch_dir_name=branch_dir_name)
        return self.compose_path(path_elements=work_path_elements, create_dirs=create_dir, relative=relative)

    def get_tmp_publish_folder(self):
        tmp_pub_elem = self.__temp_publish_path()
        return self.compose_path(path_elements=tmp_pub_elem, create_dirs=True, relative=False)

    def create_work_folders(self):
        self.work_path(self.branch_user_caches, create_dir=True)
        self.work_path(self.branch_user_exchange, create_dir=True)
        self.work_path(self.branch_user_scene_files, create_dir=True)
        self.work_path(self.branch_user_workspace, create_dir=True)

    def project_path(self):
        projects_root = os.getenv('ORIGIN_PROJECTS_ROOT')
        return Path(projects_root) / self.__context_handler.show_name

    def get_publish_data_path(self):
        return self.publish_path(self.branch_pub_data)

    def get_publish_quicktime_path(self):
        return self.publish_path(self.branch_pub_quicktime)

    def get_publish_images_path(self):
        return self.publish_path(self.branch_pub_images)

    def get_user_caches_path(self):
        return self.work_path(self.branch_user_caches)

    def get_user_exchange(self):
        return self.work_path(self.branch_user_exchange)

    def get_user_scene_files(self):
        return self.work_path(self.branch_user_scene_files)

    def get_next_version_string(self):
        return self.__compile_next_version()

    def resolve_to_absolute_path(self, rel_path, as_unix=False):
        to_path = Path(rel_path)

        if self.origin_projects_root in to_path.parents:
            resolved_path = to_path
        else:
            resolved_path = self.origin_projects_root / to_path

        if as_unix:
            return self.convert_path_to_unix(resolved_path)

        return resolved_path

    def resolve_to_relative(self, abs_path, as_unix=False):
        to_path = Path(abs_path)

        if self.origin_projects_root in to_path.parents:
            resolved_path = to_path.relative_to(self.origin_projects_root)
        else:
            resolved_path = to_path

        if as_unix:
            return self.convert_path_to_unix(resolved_path)

        return resolved_path

    def convert_path_to_unix(self, path):
        to_path = Path(path)
        to_path.resolve()
        return to_path.as_posix()

    @staticmethod
    def compose_db_path_dict(path_entities: list):
        main_path_all = dict(path_elements=path_entities)
        return main_path_all

    def compose_path(self, path_elements, create_dirs=False, relative=False):
        relative_path = Path(*path_elements)
        absolute_path = Path(self.origin_projects_root) / relative_path
        if relative:
            return relative_path
        if create_dirs:
            if not absolute_path.exists():
                absolute_path.mkdir(parents=True, exist_ok=True)

        return absolute_path


if __name__ == "__main__":
    context_object = {
    "asset_breakdown_id": None,
    "asset_breakdown_version_id": None,
    "db_asset_id": "Small_Rock.assets.characters.tafar.geometry.tafar_MAIN",
    "db_asset_stream_id": "Small_Rock.assets.characters.tafar.tafar_MAIN",
    "db_asset_type": None,
    "db_asset_version_id": None,
    "entity_id": "Small_Rock.assets.characters.tafar",
    "entity_name": "tafar",
    "entity_type": "asset",
    "origin_path_hierarchy": "assets.characters",
    "project_control": "Small_Rock__CONTROL",
    "project_publishes": "Small_Rock__PUBLISHES",
    "project_work": "Small_Rock__WORK",
    "publish_id": None,
    "show_name": "Small_Rock",
    "stack_id": "Small_Rock.assets.characters.tafar.tafar_MAIN.asset_stack",
    "stack_version_id": None,
    "task_id": "Small_Rock.assets.characters.tafar.modeling",
    "task_name": "modeling",
    "task_type": "modeling"}

    CONTEXT = { 'show_name': 'Small_Rock',
                'project_publishes': 'Small_Rock__PUBLISHES',
                'project_work': 'Small_Rock__WORK',
                'project_control': 'Small_Rock__CONTROL',
                'origin_path_hierarchy': 'assets.characters',
                'entity_name': 'red_hulk',
                'entity_type': 'asset',
                'entity_id': 'Small_Rock.assets.characters.red_hulk',
                'task_name': 'modeling',
                'task_type': 'modeling',
                'task_id': 'Small_Rock.assets.characters.red_hulk.modeling',
                'publish_id': None,
                'db_asset_stream_id': 'Small_Rock.assets.characters.red_hulk.red_hulk_MAIN',
                'db_asset_id': 'Small_Rock.assets.characters.red_hulk.geometry.red_hulk_MAIN',
                'db_asset_type': None,
                'db_asset_version_id': None,
                'asset_breakdown_id': None,
                'asset_breakdown_version_id': None,
                'stack_id': 'Small_Rock.assets.characters.red_hulk.red_hulk_MAIN.asset_stack',
                'stack_version_id': None}

    os.environ['ORIGIN_DOCI_ROOT'] = r'X:\_doci'

    app = OriginOSPathHandler(context=CONTEXT, file_format="json")
    ss = app.doci_file_name()
    print(ss)

