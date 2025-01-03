from pathlib import Path
from typing import Literal

from origin.dcc.abc.template_exporter import TemplateExporter
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler

import maya.cmds as cmds


class MayaPlayblastTemplateExporter(TemplateExporter):
    origin_scene_file = "master"
    maya_scene = "maya_scene"
    version_string = "version_string"

    def __init__(self, objects_names: list, context: ContextHandler):
        self.objects_names = objects_names
        self.context_handler = context
        self.path_handler = None

    def set_output_path(self, file_format):
        self.path_handler = OriginOSPathHandler(context=self.context_handler, file_format=file_format)
        full_path = Path(self.path_handler.publish_path(branch_dir_name=self.path_handler.branch_pub_data,
                                                        create_dir=True)) / self.path_handler.output_file_name

        return full_path

    def save_master_file(self):
        file_path_path = self.set_output_path(file_format=self.origin_scene_file)
        full_path = f"{file_path_path}.mb"
        cmds.file(rename=full_path)
        cmds.file(save=True, type='mayaBinary')
        return {self.origin_scene_file: self.path_handler.convert_path_to_unix(full_path)}

    def save_maya_scene(self):
        file_path_path = self.set_output_path(file_format=self.origin_scene_file)
        full_path = f"{file_path_path}.mb"
        cmds.file(rename=full_path)
        cmds.file(save=True, type='mayaBinary')
        return {self.origin_scene_file: self.path_handler.convert_path_to_unix(full_path)}

    def export(self, file_format: Literal["maya_scene", "master"]):
        """
        file_type should be one of the predefined class variables:
            - MayaAnimRiggingExporter.usd_file
            - MayaAnimRiggingExporter.origin_scene_file
            - MayaAnimRiggingExporter.maya_scene
            """
        if file_format == self.origin_scene_file:
            return self.save_master_file()

        if file_format == self.save_maya_scene():
            return self.save_maya_scene()

