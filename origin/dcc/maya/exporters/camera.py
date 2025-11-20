import os
from pathlib import Path
from typing import Literal

import maya.cmds as cmds
from origin.dcc.abc.camera_exporter import CameraExporter
from origin.dcc.maya.exporters.alembic.alembic import MayaAlembicExporter
from origin.dcc.maya.exporters.scene.master_scene import MayaMasterSceneExporter
from origin.dcc.maya.exporters.usd.usd import MayaUSDExporter
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler


class MayaCameraExporter:
    alembic_file = "abc"
    usd_file = "usd"
    origin_scene_file = "master"
    version_string = "version_string"

    def __init__(self, options, camera_name, src_file_path=None, start_frame=None, end_frame=None):
        self.options = options

        self.context_handler = self.options["context_object"]

        if isinstance(self.context_handler, dict):
            self.context_handler = ContextHandler()
            self.context_handler.load_session(self.options["context_object"])

        self.camera_name = camera_name

        self.src_file_path = src_file_path

        if self.src_file_path is None:
            self.src_file_path = self.options["master_scene"]

        self.start_frame = start_frame
        self.end_frame = end_frame
        self.camera_transform = None
        self.camera_shape = None
        self.path_handler = None

        self.master_file_exporter = None
        self.alembic_file_exporter = None
        self.obj_file_exporter = None
        self.usd_file_exporter = None

        self.exported_results = {}
        os.environ["ANIM_BAKED"] = "0"

    def open_master_file(self):
        if self.src_file_path is not None:
            cmds.file(self.src_file_path, open=True, force=True)
            self.get_camera_nodes()
            # cmds.file(self.src_file_path,
            #           i=True,
            #           typ="mayaBinary",
            #           ignoreVersion=True,
            #           ra=True,
            #           mergeNamespacesOnClash=False,
            #           namespace="turntable_camera",
            #           pr=True,
            #           importTimeRange="combine",
            #           )

    def set_output_path(self, file_format):
        self.path_handler = OriginOSPathHandler(context=self.context_handler, file_format=file_format)
        full_path = Path(self.path_handler.publish_path(branch_dir_name=self.path_handler.branch_pub_data,
                                                        create_dir=True)) / self.path_handler.output_file_name
        return full_path

    def export_master_scene(self):
        self.master_file_exporter = MayaMasterSceneExporter(options=self.options,
                                                            context=self.context_handler,
                                                            object_transform=self.camera_name)

        exported_results = self.master_file_exporter.execute()
        self.exported_results.update(exported_results)

    def get_camera_nodes(self):
        # Get the transform and shape node of the camera
        if cmds.objExists(self.camera_name):
            print("CAMERA NAME: ", self.camera_name)
            self.camera_transform = self.camera_name
            self.camera_shape = cmds.listRelatives(self.camera_transform, shapes=True)[0]
        else:
            raise ValueError(f"Invalid camera name: {self.camera_name} from maya scene {self.src_file_path}")

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
            temp_locator = cmds.spaceLocator()

            parent_to_cam = cmds.parentConstraint(self.camera_transform, temp_locator, maintainOffset=0)

            cmds.bakeResults(
                temp_locator,
                simulation=True,
                preserveOutsideKeys=True,
                sparseAnimCurveBake=False,
                removeBakedAttributeFromLayer=False,
                bakeOnOverrideLayer=False,
                minimizeRotation=True,
                sampleBy=1,
                oversamplingRate=1,
                disableImplicitControl=True,
                controlPoints=False,
                shape=False,
                time=(self.start_frame, self.end_frame)
            )

            cmds.delete(parent_to_cam[0])

            parent = cmds.listRelatives(self.camera_transform, parent=True)
            if parent:
                cmds.parent(self.camera_transform, world=True)

            parent_cam_to_locator = cmds.parentConstraint(temp_locator, self.camera_transform, maintainOffset=1)

            cmds.bakeResults(
                self.camera_transform,
                simulation=True,
                preserveOutsideKeys=True,
                sparseAnimCurveBake=False,
                removeBakedAttributeFromLayer=False,
                bakeOnOverrideLayer=False,
                minimizeRotation=True,
                sampleBy=1,
                oversamplingRate=1,
                disableImplicitControl=True,
                controlPoints=False,
                shape=False,
                time=(self.start_frame, self.end_frame)
            )

            cmds.delete(parent_cam_to_locator[0])
            cmds.delete(temp_locator)
            cmds.select(cl=True)

            os.environ["ANIM_BAKED"] = "1"

    def export_alembic(self):
        self.alembic_file_exporter = MayaAlembicExporter(options=self.options,
                                                         context=self.context_handler,
                                                         object_transform=self.camera_name,
                                                         frame_range=(self.start_frame, self.end_frame))

        exported_results = self.alembic_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export_usd(self):
        self.usd_file_exporter = MayaUSDExporter(options=self.options,
                                                 context=self.context_handler,
                                                 object_transform=self.camera_name,
                                                 frame_range=(self.start_frame, self.end_frame))
        exported_results = self.usd_file_exporter.execute()
        self.exported_results.update(exported_results)

    def export_camera(self, files_formats: list = None):
        print("Selecting Exporter")
        files = {self.alembic_file: self.export_alembic,
                 self.usd_file: self.export_usd
                 }

        if files_formats is None:
            files_formats = [self.alembic_file, self.usd_file]

        if files_formats is not None:
            for file_type in files_formats:
                if file_type in files:
                    files[file_type]()
        return self.exported_results

    def run_export(self, focal_length=None, filmback=None, resolution_gate=None, cam_motion_blur=False):
        self.open_master_file()
        self.set_camera_specs(focal_length=focal_length, filmback=filmback, resolution_gate=resolution_gate)

        if os.getenv("ANIM_BAKED") == "0":
            self.bake_animation()

        self.export_master_scene()
        self.export_camera()

        return self.exported_results
