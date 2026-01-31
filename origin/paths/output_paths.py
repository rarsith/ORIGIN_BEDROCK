import os
from pathlib import Path

from origin.common_utils.users import Users
from origin.envars.origin_envars import ContextHandler
from origin.database.entities.operators import get_file_component_class


class SavingRootBranch:
    publishes_root = "publishes"
    user_work_root = "work"

    branch_pub_data = "data"
    branch_pub_images = "images"
    branch_pub_quicktime = "quicktime"

    branch_user_exchange = "exchange"
    branch_user_scene_files = "scene_files"
    branch_user_workspace = "workspace"
    branch_user_caches = "caches"


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

    def __init__(self, context: ContextHandler = None, file_format=None):
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

        self.__compile_next_version()
        self.__compile_file_name()

    def __compile_next_version(self):
        if self.__db_asset_doc:
            self.__version_string, version = self.__db_asset_doc.operations().get_next_version()
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

    def publish_base_path(self):
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

    def __publish_db_asset_version_branch(self, branch_dir_name):
        pub_path = self.publish_base_path()
        pub_path.append(branch_dir_name)
        pub_path.append(self.__compile_server_db_asset_dir_name())
        pub_path.append(self.__compile_server_db_asset_version_dir_name())
        pub_path.append(self.__compile_file_parent_dir_name())

        return pub_path

    def __work_db_asset_version_branch(self, branch_dir_name=None):
        if branch_dir_name is not None:
            work_path = self.work_base_path()
            work_path.append(branch_dir_name)
            return work_path
        else:
            return self.work_base_path()

    def publish_path(self, branch_dir_name=None, create_dir=False, relative=False):
        publish_path_elements = self.__publish_db_asset_version_branch(branch_dir_name=branch_dir_name)
        return self.compose_path(path_elements=publish_path_elements, create_dirs=create_dir, relative=relative)

    def work_path(self, branch_dir_name=None, create_dir=False, relative=False):
        work_path_elements = self.__work_db_asset_version_branch(branch_dir_name=branch_dir_name)
        return self.compose_path(path_elements=work_path_elements, create_dirs=create_dir, relative=relative)

    def create_work_folders(self):
        self.work_path(self.branch_user_caches, create_dir=True)
        self.work_path(self.branch_user_exchange, create_dir=True)
        self.work_path(self.branch_user_scene_files, create_dir=True)
        self.work_path(self.branch_user_workspace, create_dir=True)

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
    # context_sample = {'show_name': 'The_Rock',
    #                   'project_publishes': 'The_Rock__PUBLISHES',
    #                   'project_work': 'The_Rock__WORK',
    #                   'project_control': 'The_Rock__CONTROL',
    #                   'origin_path_hierarchy': 'assets.props',
    #                   'entity_name': 'tafer',
    #                   'entity_id': 'The_Rock.assets.chr.tafer',
    #                   'asset_breakdown_id': 'The_Rock.assets.chr.tafer.breakdown',
    #                   'entity_type': 'asset',
    #                   'task_name': "modeling",
    #                   'task_type': "modeling",
    #                   'task_id': "The_Rock.assets.chr.tafer.modeling",
    #                   'db_asset_id': 'The_Rock.assets.chr.tafer.geometry.tafer_main',
    #                   'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer_main',
    #                   'stack_id': 'The_Rock.assets.chr.tafer.tafer_main.asset_stack',
    #                   }

    context_object = {
    "asset_breakdown_id": None,
    "asset_breakdown_version_id": None,
    "db_asset_id": None,
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
    "task_type": "modeling"
}

    # context_obj = ContextHandler()
    # context_obj.load_session(session_data=context_sample)

    app = OriginOSPathHandler(context=context_object, file_format="master")
    # app = OriginOSPathHandler(context=context_object, file_format="master")
    ss = app.__compile_server_db_asset_version_dir_name()
    print(ss)


    # x_path_items = app.get_publish_quicktime_path()
    # x_to_unix = app.convert_path_to_unix(x_path_items)
    # print("UNIX:  ", x_to_unix)
    #
    # y_path_items = app.get_publish_images_path()
    # z_path_items = app.get_publish_data_path()
    # a_path_items = app.get_user_caches_path()
    # b_path_items = app.get_user_scene_files()
    # c_path_items = app.get_user_exchange()
    # rel_unix = app.resolve_to_relative(c_path_items, as_unix=True)
    # print("RELATIVE: ", rel_unix)
    # # compile_path = app.compose_path(x_path_items)
    # print(x_path_items)
    # print(y_path_items)
    # print(z_path_items)
    #
    # print(a_path_items)
    # print(b_path_items)
    # print(c_path_items)
