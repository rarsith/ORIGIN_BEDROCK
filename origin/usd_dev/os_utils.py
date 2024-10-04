import os

# SETTINGS VARIABLES


class OSPathResolvers():
    SINGLE_USER = True  # (False: the project will be condered MULTIUSER which will make it tasks Statuses Dependent)
    PROJECT_ROOT = r"D:\__SANDBOX\USD"
    ORIGIN_SCENE_ID = "ORIGIN"
    PUBLISHES_PATH = r"publishes\data"
    USD_VARIANT_SET_NAME = "var_set"
    USD_VARIANT_NAME_DELIMITER = "__"
    ENTITY_INTERFACE_SUFFIX = "interface"

    # PIPELINE VARIABLES
    PROJECT = "USD_asset_schemas"
    BRANCH = "templates"
    CATEGORY = "assetCategory"
    ASSET_NAME = "assetName"
    TASK_NAME = "taskName"
    STREAM_ID = "streamName"
    STREAM_FULL_NAME = "assetCategory_assetName_taskName__streamName"
    APPROVED_VERSION = "v001"

    def convert_path(self, path_to_convert) -> str:
        from pathlib import Path, PurePosixPath
        path_conv = Path(path_to_convert)
        unix_path = PurePosixPath(path_conv)

        return str(unix_path)

    def path_resolve_asset_root(self):
        return os.path.join(self.PROJECT_ROOT, self.PROJECT, self.BRANCH, self.CATEGORY, self.ASSET_NAME)

    def path_resolve_task(self):
        task_root = self.path_resolve_asset_root()

        return os.path.join(task_root, self.TASK_NAME)

    def path_resolve_publishes(self):
        task_root = self.path_resolve_task()

        return os.path.join(task_root, self.PUBLISHES_PATH)

    def file_resolve_full_stream_name(self):
        stream_base_name = "_".join([self.CATEGORY, self.ASSET_NAME, self.TASK_NAME])

        return "__".join([stream_base_name, self.STREAM_ID])

    def path_resolve_active_stream(self):
        publishes_root = self.path_resolve_publishes()
        stream_full_name = self.file_resolve_full_stream_name()

        return os.path.join(publishes_root, stream_full_name)

    def name_resolve_version(self):
        stream_full_name = self.file_resolve_full_stream_name()
        in_stream_version = "_".join([stream_full_name, self.APPROVED_VERSION])

        return in_stream_version

    def path_resolve_allowed_publish(self):
        active_stream = self.path_resolve_active_stream()
        published_version = self.name_resolve_version()

        return os.path.join(active_stream, published_version)

    def file_name_resolve_origin(self, file_format="txt"):
        origin_file_name = "_".join([self.CATEGORY, self.ASSET_NAME, self.ORIGIN_SCENE_ID])

        return f"{origin_file_name}.{file_format}"

    def file_name_resolve_interface(self, file_format="usda"):
        interface_file_name = "_".join([self.ASSET_NAME, self.STREAM_ID, self.ENTITY_INTERFACE_SUFFIX])

        return f"{interface_file_name}.{file_format}"

    def get_file_origin(self):
        pub_path = self.path_resolve_allowed_publish()
        origin_file_name = self.file_name_resolve_origin()

        return os.path.join(pub_path, origin_file_name)

    def path_resolve_var_sets(self):
        publish_path = self.path_resolve_allowed_publish()
        var_sets = os.path.join(publish_path, self.USD_VARIANT_SET_NAME)

        return var_sets

    def path_get_published_variant_sets(self):
        from pathlib import Path

        to_var_sets = self.path_resolve_var_sets()
        p = Path(to_var_sets).glob('**/*')
        var_paths = [str(x) for x in p if x.is_dir()]

        return var_paths

    def files_get_published_variant_set(self, file_path: str) -> list:
        from pathlib import Path

        p = Path(file_path).glob('**/*')
        var_files = [str(x) for x in p if x.is_file()]

        return var_files

    def get_variant_name_from_file(self, full_file_path: str) -> str:
        file_from_path = os.path.split(full_file_path)[-1]
        file_name = os.path.splitext(file_from_path)[0]
        var_name = file_name.split("_")[-1]

        return var_name

    def dict_compute_from_var_sets(self, var_sets_root_paths: list) -> dict:
        var_sets_dict = {}
        for each_path in var_sets_root_paths:
            get_var_files = self.files_get_published_variant_set(each_path)
            get_parent_dir = os.path.split(each_path)[1]
            var_set_name = get_parent_dir.split(self.USD_VARIANT_NAME_DELIMITER)[-1]
            var_sets_dict[var_set_name] = get_var_files

        return var_sets_dict

    def add_payload_to_prim(self, prim, payload_usd_path) -> None:
        target_file_dir = self.path_resolve_allowed_publish()
        relative_path = os.path.relpath(payload_usd_path, target_file_dir)
        unix_path = self.convert_path(relative_path)

        prim.GetPayloads().AddPayload(unix_path)

    def create_variant_set(self, usd_file_target: str, variant_set_data: dict) -> None:
        from pxr import Usd
        base_stage = Usd.Stage.Open(usd_file_target)
        default_prim = base_stage.GetDefaultPrim()

        for variant_set, variants_paths in variant_set_data.items():
            variant_set = default_prim.GetVariantSets().AddVariantSet(variant_set)
            for variant in variants_paths:
                var_name = self.get_variant_name_from_file(variant)
                variant_set.AddVariant(var_name)
                variant_set.SetVariantSelection(var_name)
                with variant_set.GetVariantEditContext():
                    self.add_payload_to_prim(default_prim, variant)

        base_stage.GetRootLayer().Save()
