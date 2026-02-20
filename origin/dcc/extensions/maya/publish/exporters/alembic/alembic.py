from pathlib import Path

from origin.database.publisher.db_publisher import DBPublisher
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler

import maya.cmds as cmds

import logging

logger = logging.getLogger(__name__)
logger.info(f"running {__name__}")


class MayaAlembicExporter:
    alembic_file = "abc"

    def __init__(self,
                 options,
                 object_transform: str,
                 context: ContextHandler,
                 frame_range: tuple = (1001, 1001),
                 uv_write: bool = True,
                 world_space: bool = True,
                 write_uv_sets: bool = True,
                 write_visibility: bool = False,
                 data_format: str = "ogawa"):

        self.options = options

        self.object_transform = object_transform
        self.frame_range = frame_range
        self.uv_write = uv_write
        self.world_space = world_space
        self.write_uv_sets = write_uv_sets
        self.write_visibility = write_visibility
        self.data_format = data_format

        self.object_shape = None
        self.context_handler = context
        self.path_handler = None
        self.db_publisher = DBPublisher(options=self.options)

    def set_output_path(self, file_format):
        self.path_handler = OriginOSPathHandler(context=self.context_handler, file_format=file_format)
        full_path = Path(self.path_handler.publish_path(branch_dir_name=self.path_handler.branch_pub_data,
                                                        create_dir=True)) / self.path_handler.output_file_name
        return full_path

    def run_export(self):
        full_path = self.set_output_path(file_format=self.alembic_file)
        alembic_file_path = f"{full_path}.abc"

        export_command = f"-frameRange {self.frame_range[0]} {self.frame_range[1]} -stripNamespaces"
        if self.uv_write:
            export_command += "-uvWrite "
        if self.world_space:
            export_command += "-worldSpace "
        if self.write_uv_sets:
            export_command += "-writeUVSets "
        if self.write_visibility:
            export_command += "-writeVisibility "

        export_command += f" -dataFormat {self.data_format}"

        if "|" in self.object_transform:
            get_root = self.object_transform.rsplit("|", 1)[1]
        else:
            get_root = self.object_transform

        export_command += f" -root {get_root}"
        export_command += f" -file {alembic_file_path}"

        cmds.AbcExport(j=export_command)

        return {self.alembic_file: self.path_handler.convert_path_to_unix(alembic_file_path)}

    def execute(self):
        captured_data = self.run_export()

        print("ABC EXPORTER CONTEXT DB ASSET VERSION ID:  ", self.context_handler.db_asset_version_id)
        self.db_publisher.create_db_file_components(
            db_asset_version_id=self.context_handler.db_asset_version_id,
            published_data=captured_data,
            component_parent_id=self.context_handler.db_asset_version_id)

        return captured_data
