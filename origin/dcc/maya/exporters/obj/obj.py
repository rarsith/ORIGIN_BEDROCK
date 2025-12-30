from pathlib import Path

from origin.database.publisher.db_publisher import DBPublisher
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler

import maya.cmds as cmds


class MayaOBJExporter:
    obj_file = "obj"

    def __init__(self,
                 options,
                 object_transform: str,
                 context: ContextHandler):

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
        full_path = self.set_output_path(file_format=self.obj_file)
        obj_file_path = f"{full_path}.obj"

        cmds.select(self.object_transform, r=True)

        obj_export_options = ["groups=0", "ptgroups=0", "materials=0", "smoothing=0", "normals=0"]
        export_options_str = ";".join(obj_export_options)

        cmds.file(obj_file_path,
                  force=True,
                  options=export_options_str,
                  typ="OBJExport",
                  pr=True,
                  es=True)

        return {self.obj_file: self.path_handler.convert_path_to_unix(obj_file_path)}

    def execute(self):
        captured_data = self.run_export()

        self.db_publisher.create_db_file_components(
            db_asset_version_id=self.context_handler.db_asset_version_id,
            published_data=captured_data,
            component_parent_id=self.context_handler.db_asset_version_id)

        return captured_data
