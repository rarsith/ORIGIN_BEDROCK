import os
from pathlib import Path

from origin.common_utils.users import Users
from origin.envars.origin_envars import ContextHandler
from origin.database.entities.operators import get_file_component_class


class OriginOSPathHandler:
    publishes_root = "publishes"
    user_work_root = "work"

    branch_pub_data = "data"
    branch_pub_images = "images"
    branch_pub_quicktime = "quicktime"

    branch_user_exchange = "exchange"
    branch_user_scene_files = "scene_files"
    branch_user_workspace = "workspace"
    branch_user_caches = "caches"

    def __init__(self, context, file_format=None):
        self.__context_handler = context
        self.origin_projects_root = os.getenv("ORIGIN_PROJECTS_ROOT")

        self.__origin_path_elements = self.__context_handler.resolve_origin_path_hierarchy()
        self.__category_name = self.__context_handler.get_entity_category()
        self.__db_asset_doc = self.__context_handler.database_handler().get_db_asset_document()
        self.__version_string = None
        self.output_file_name = None
        self.file_format = file_format

        self.__compile_next_version()
        self.__compile_file_name()

    def __compile_next_version(self):
        if self.__db_asset_doc:
            self.__version_string, version = self.__db_asset_doc.get_next_version()
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

    def __publish_base_path(self):
        publish_base_path = self.__base_path()
        publish_base_path.append(self.publishes_root)

        return publish_base_path

    def __work_base_path(self):
        base_path = self.__base_path()
        base_path.append(self.__compile_user_work_dir())

        return base_path

    def __publish_db_asset_version_branch(self, branch_dir_name):
        pub_path = self.__publish_base_path()
        pub_path.append(branch_dir_name)
        pub_path.append(self.__compile_server_db_asset_dir_name())
        pub_path.append(self.__compile_server_db_asset_version_dir_name())
        pub_path.append(self.__compile_file_parent_dir_name())

        return pub_path

    def __work_db_asset_version_branch(self, branch_dir_name):
        work_path = self.__work_base_path()
        work_path.append(branch_dir_name)

        return work_path

    def publish_path(self, branch_dir_name, create_dir=False, relative=False):
        publish_path_elements = self.__publish_db_asset_version_branch(branch_dir_name=branch_dir_name)
        return self.compose_path(path_elements=publish_path_elements, create_dirs=create_dir, relative=relative)

    def work_path(self, branch_dir_name, create_dir=False, relative=False):
        work_path_elements = self.__work_db_asset_version_branch(branch_dir_name=branch_dir_name)
        return self.compose_path(path_elements=work_path_elements, create_dirs=create_dir, relative=relative)

    def create_work_folders(self):
        self.work_path(self.branch_user_caches, create_dir=True)
        self.work_path(self.branch_user_exchange, create_dir=True)
        self.work_path(self.branch_user_scene_files, create_dir=True)
        self.work_path(self.branch_user_workspace, create_dir=True)

    def get_next_version_string(self):
        return self.__compile_next_version()

    def convert_path_to_unix(self, path):
        to_path = Path(path)
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
    context_sample = {'show_name': 'New_State',
                      'project_publishes': 'New_State__PUBLISHES',
                      'project_work': 'New_State__WORK',
                      'project_control': 'New_State__CONTROL',
                      'origin_path_hierarchy': 'assets.chr',
                      'entity_name': 'yellow_hulk',
                      'db_asset_id': 'New_State.assets.chr.yellow_hulk.modeling.collar',
                      'entity_type': 'asset',
                      'entity_id': 'New_State.assets.chr.yellow_hulk',
                      'task_name': "modeling",
                      'task_type': "modeling"}

    context_obj = ContextHandler()
    context_obj.load_session(session_data=context_sample)

    app = OriginOSPathHandler(context=context_obj, file_format="obj")
    x_path_items = app.publish_path(branch_dir_name=app.branch_pub_images)
    # compile_path = app.compose_path(x_path_items)
    print(x_path_items)
