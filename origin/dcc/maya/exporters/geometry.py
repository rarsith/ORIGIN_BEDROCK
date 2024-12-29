from pathlib import Path
from typing import Literal

from origin.dcc.abc.geometry_exporter import GeometryExporter
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler

import maya.cmds as cmds


class MayaGeometryExporter(GeometryExporter):
    obj_file = "obj"
    alembic_file = "abc"
    usd_file = "usd"
    origin_scene_file = "master"
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

    def export_alembic(self,
                       frame_range=(1, 1),
                       uv_write=True,
                       world_space=True,
                       write_uv_sets=True,
                       data_format="ogawa"):

        full_path = self.set_output_path(file_format=self.alembic_file)

        alembic_file_path = f"{full_path}.abc"

        export_command = f"-frameRange {frame_range[0]} {frame_range[1]} "
        if uv_write:
            export_command += "-uvWrite "
        if world_space:
            export_command += "-worldSpace "
        if write_uv_sets:
            export_command += "-writeUVSets "

        export_command += f" -dataFormat {data_format}"
        for obj in self.objects_names:
            if "|" in obj:
                get_root = obj.split("|", 1)[-1]
            else:
                get_root = obj
            export_command += f" -root {get_root}"

        export_command += f" -file {alembic_file_path}"
        cmds.AbcExport(j=export_command)

        return {self.alembic_file: self.path_handler.convert_path_to_unix(alembic_file_path)}

    def export_obj(self):
        full_path = self.set_output_path(file_format=self.obj_file)
        obj_file_path = f"{full_path}.obj"
        cmds.select(self.objects_names, r=True)
        obj_export_options = ["groups=0", "ptgroups=0", "materials=0", "smoothing=0", "normals=0"]
        export_options_str = ";".join(obj_export_options)

        cmds.file(obj_file_path,
                  force=True,
                  options=export_options_str,
                  typ="OBJexport",
                  pr=True,
                  es=True)

        return {self.obj_file: self.path_handler.convert_path_to_unix(obj_file_path)}

    def export_usd(self):
        full_path = self.set_output_path(file_format=self.usd_file)
        usd_file_path = f"{full_path}.usd"

        return {self.usd_file: self.path_handler.convert_path_to_unix(usd_file_path)}

    def export_geometry(self, file_format: Literal["abc", "obj", "master", "usd"]):
        """
        file_type should be one of the predefined class variables:
            - MayaGeometryExporter.obj_file
            - MayaGeometryExporter.alembic_file
            - MayaGeometryExporter.usd_file
            - MayaGeometryExporter.origin_scene_file
            """
        if file_format == self.origin_scene_file:
            return self.save_master_file()

        if file_format == self.alembic_file:
            return self.export_alembic()

        if file_format == self.obj_file:
            return self.export_obj()

        if file_format == self.usd_file:
            return self.export_usd()
