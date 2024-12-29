from pathlib import Path
from typing import Literal

import maya.cmds as cmds
from origin.dcc.abc.camera_exporter import CameraExporter
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler


class MayaCameraExporter(CameraExporter):
    alembic_file = "abc"
    usd_file = "usd"
    origin_scene_file = "master"
    version_string = "version_string"

    def __init__(self, camera_name, context: ContextHandler, start_frame=None, end_frame=None):
        self.context_handler = context
        self.camera_name = camera_name
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.camera_transform = None
        self.camera_shape = None
        self.path_handler = None
        self.get_camera_nodes()

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

    def get_camera_nodes(self):
        # Get the transform and shape node of the camera
        if cmds.objExists(self.camera_name):
            self.camera_transform = self.camera_name
            self.camera_shape = cmds.listRelatives(self.camera_transform, shapes=True)[0]
        else:
            raise ValueError("Invalid camera name")

    def set_camera_specs(self, focal_length=None, filmback=None, resolution_gate=None, cam_motion_blur=False):
        print("Setting Camera Specs")
        # Set camera focal length
        if focal_length:
            cmds.setAttr(f"{self.camera_shape}.focalLength", focal_length)

        # Set filmback attributes if provided
        if filmback:
            cmds.setAttr(f"{self.camera_shape}.horizontalFilmAperture", filmback['horizontal'])
            cmds.setAttr(f"{self.camera_shape}.verticalFilmAperture", filmback['vertical'])

        # Set resolution gate (if needed in VFX context)
        if resolution_gate:
            cmds.setAttr(f"{self.camera_shape}.horizontalResolution", resolution_gate[0])
            cmds.setAttr(f"{self.camera_shape}.verticalResolution", resolution_gate[1])

        if cam_motion_blur:
            cmds.setAttr(f"{self.camera_shape}.motionBlurOverride", 1)
        else:
            cmds.setAttr(f"{self.camera_shape}.motionBlurOverride", 2)

    def bake_animation(self):
        # Bake animation if camera is animated and frame range is provided
        if self.start_frame and self.end_frame:
            cmds.bakeResults(self.camera_transform, t=(self.start_frame, self.end_frame),
                             sampleBy=1, simulation=True,
                             disableImplicitControl=True, preserveOutsideKeys=False)

    def export_alembic(self):
        # Export the camera to Alembic
        start_frame = self.start_frame if self.start_frame else cmds.playbackOptions(query=True, minTime=True)
        end_frame = self.end_frame if self.end_frame else cmds.playbackOptions(query=True, maxTime=True)

        full_path = self.set_output_path(file_format=self.alembic_file)
        alembic_file_path = f"{full_path}.abc"

        abc_cmd = (f"-frameRange {start_frame} {end_frame} "
                   f"-root {self.camera_transform} "
                   "-stripNamespaces -worldSpace -writeVisibility "
                   f"-file {alembic_file_path}")
        cmds.AbcExport(j=abc_cmd)
        return {self.alembic_file: self.path_handler.convert_path_to_unix(alembic_file_path)}

    def export_usd(self):
        # Export the camera to USD
        cmds.select(self.camera_transform)
        usd_options = ["",
                       "exportUVs=0",
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
                       "stripNamespaces=0",
                       "worldspace=1"]

        if self.start_frame and self.end_frame:
            additional_options = [f"startTime={self.start_frame}", f"endTime={self.end_frame}"]
            for usd_option in additional_options:
                usd_options.append(usd_option)

        usd_combined_options = ";".join(usd_options)

        full_path = self.set_output_path(file_format=self.usd_file)
        usd_file_path = f"{full_path}.usd"

        cmds.file(usd_file_path, force=True, options=usd_combined_options, type="USD Export", exportSelected=True)
        return {self.usd_file: self.path_handler.convert_path_to_unix(usd_file_path)}

    def export_camera(self, file_format: Literal["abc", "master", "usd"]):
        print("Selecting Exporter")
        """
        file_type should be one of the predefined class variables:
            - MayaCameraExporter.alembic_file
            - MayaCameraExporter.usd_file
            - MayaCameraExporter.origin_scene_file
            """
        if file_format == self.origin_scene_file:
            return self.save_master_file()

        if file_format == self.alembic_file:
            return self.export_alembic()

        if file_format == self.usd_file:
            return self.export_usd()

    def run_export(self, file_format, focal_length=None, filmback=None, resolution_gate=None, cam_motion_blur=False):
        print("Running Camera EXPORT")
        # Set the camera specifications
        self.set_camera_specs(focal_length=focal_length, filmback=filmback, resolution_gate=resolution_gate)

        # Bake animation if it's an animated camera
        self.bake_animation()
        return self.export_camera(file_format)
