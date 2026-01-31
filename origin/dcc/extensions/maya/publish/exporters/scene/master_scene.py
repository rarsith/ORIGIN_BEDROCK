from pathlib import Path

from origin.database.publisher.db_publisher import DBPublisher
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler

import maya.cmds as cmds


class MayaMasterSceneExporter:
    origin_scene_file = "master"
    version_string = "version_string"

    def __init__(self, options, context: ContextHandler, object_transform=None):
        self.options = options
        self.object_transform = object_transform
        self.context_handler = context
        self.path_handler = None
        self.db_publisher = DBPublisher(options=self.options)

    def set_output_path(self, file_format):
        self.path_handler = OriginOSPathHandler(context=self.context_handler, file_format=file_format)
        full_path = Path(self.path_handler.publish_path(branch_dir_name=self.path_handler.branch_pub_data,
                                                        create_dir=True)) / self.path_handler.output_file_name
        return full_path

    def run_export(self):
        file_path_path = self.set_output_path(file_format=self.origin_scene_file)
        full_path = f"{file_path_path}.mb"

        if self.object_transform is not None:
            if cmds.objExists(self.object_transform):
                cmds.select(self.object_transform, replace=True)

                cmds.file(
                    full_path,
                    force=True,
                    options="v=0;",
                    typ="mayaBinary",
                    pr=True,
                    es=True)

                cmds.select(cl=True)
            else:
                raise RuntimeError(f"Object {self.object_transform} does not exist")

        else:
            cmds.file(full_path, ea=True, force=True, type='mayaBinary')

        return {self.origin_scene_file: self.path_handler.convert_path_to_unix(full_path)}

    def execute(self):
        captured_data = self.run_export()
        self.db_publisher.create_db_file_components(
            db_asset_version_id=self.context_handler.db_asset_version_id,
            published_data=captured_data,
            component_parent_id=self.context_handler.db_asset_version_id)

        return captured_data
