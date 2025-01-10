from pathlib import Path
from typing import Literal

from origin.database.publisher.db_publisher import DBPublisher
from origin.dcc.abc.geometry_exporter import GeometryExporter
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler

import maya.cmds as cmds


class MayaUSDExporter:
    usd_file = "usd"

    def __init__(self,
                 object_transform: list,
                 context: ContextHandler,
                 frame_range: tuple = None):

        self.object_transform = object_transform
        self.frame_range = frame_range
        self.context_handler = context
        self.path_handler = None
        self.db_publisher = DBPublisher(context=self.context_handler)

    def set_output_path(self, file_format):
        self.path_handler = OriginOSPathHandler(context=self.context_handler, file_format=file_format)
        full_path = Path(self.path_handler.publish_path(branch_dir_name=self.path_handler.branch_pub_data,
                                                        create_dir=True)) / self.path_handler.output_file_name
        return full_path

    def run_export(self):
        cmds.select(self.object_transform)
        usd_options = ["",
                       "exportUVs=1",
                       "exportSkin=none",
                       "exportBlendShapes=0",
                       "exportDisplayColor=0",
                       "filterTypes=nurbsCurve",
                       "exportColorSets=0",
                       "exportComponentTags=0",
                       "defaultMeshScheme=none",
                       "animation=1",
                       "eulerFilter=1",
                       "staticSingleSample=0",
                       "frameStride=1",
                       "frameSample=0.0",
                       "defaultUSDFormat=usdc",
                       "parentScope=camera",
                       "exportDisplayColor=0"
                       "convertMaterialsTo=[]",
                       "exportInstances=1",
                       "exportVisibility=1",
                       "exportSkels=none",
                       "mergeTransformAndShape=1",
                       "stripNamespaces=1",
                       "worldspace=1"]

        if self.frame_range:
            additional_options = [f"startTime={self.frame_range[0]}", f"endTime={self.frame_range[1]}"]
            for usd_option in additional_options:
                usd_options.append(usd_option)

        usd_combined_options = ";".join(usd_options)

        full_path = self.set_output_path(file_format=self.usd_file)
        usd_file_path = f"{full_path}.usd"

        cmds.file(usd_file_path, force=True, options=usd_combined_options, type="USD Export", exportSelected=True)

        return {self.usd_file: self.path_handler.convert_path_to_unix(usd_file_path)}

    def execute(self):
        captured_data = self.run_export()

        self.db_publisher.create_db_file_components(
            db_asset_version_id=self.context_handler.db_asset_version_id,
            published_data=captured_data,
            component_parent_id=self.context_handler.db_asset_version_id)

        return captured_data


