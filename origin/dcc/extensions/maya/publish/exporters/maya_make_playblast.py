import subprocess
from pathlib import Path

import ffmpeg
import maya.cmds as cmds

from origin.database.entities.actions import Create
from origin.database.publisher.db_publisher import DBPublisher
from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler


class MayaMakePlayblast:
    jpg_seq = "jpg_seq"
    mov = "mov"

    def __init__(self,
                 frame_range=None,
                 resolution=None,
                 resolution_percentage=None,
                 geo_scene_path=None,
                 camera_scene_path=None,
                 template_scene_path=None,
                 output_path=None,
                 options=None
                 ):

        self.options = options

        self.path_handler = None
        self.context_handler = self.options["context_object"]

        self.db_publisher = None

        if isinstance(self.context_handler, dict):
            self.context_handler = ContextHandler()
            self.context_handler.load_session(self.options["context_object"])

        self.geo_scene_path = geo_scene_path
        self.frame_range = frame_range
        self.resolution = resolution
        self.resolution_percentage = resolution_percentage
        self.camera_scene_path = camera_scene_path
        self.template_scene_path = template_scene_path
        self.output_path = output_path

        if self.options is not None:
            self.frame_range = self.options["review_options"]["frame_range"]
            self.resolution = self.options["review_options"]["resolution"]
            self.resolution_percentage = self.options["review_options"]["resolution_percentage"]
            self.camera_scene_path = self.options["review_options"]["camera_asset_ver_id"]
            self.template_scene_path = self.options["review_options"]["template_asset_ver_id"]
            self.geo_scene_path = self.options["review_options"]["geo_scene_path"]
            self.output_path = self.set_output_path(file_format=self.jpg_seq)
            self.quicktime_path = self.set_mov_path(file_format=self.mov)

    def set_output_path(self, file_format):
        self.path_handler = OriginOSPathHandler(context=self.context_handler, file_format=file_format)
        full_path = Path(self.path_handler.publish_path(branch_dir_name=self.path_handler.branch_pub_images,
                                                        create_dir=True)) / self.path_handler.output_file_name
        return full_path

    def set_mov_path(self, file_format):
        self.path_handler = OriginOSPathHandler(context=self.context_handler, file_format=file_format)
        full_path = Path(self.path_handler.publish_path(branch_dir_name=self.path_handler.branch_pub_quicktime,
                                                        create_dir=True)) / self.path_handler.output_file_name
        return full_path

    def fresh_scene(self):
        cmds.file(new=True, force=True)

    def setup_playblast_options(self):
        panel = "modelPanel4"

        if not cmds.modelPanel(panel, exists=True):
            cmds.modelPanel("modelPanel4")

        cmds.modelEditor(panel, e=True, rendererName='vp2Renderer')

        cmds.modelEditor(panel, e=True, lights=False)  # No lights
        cmds.modelEditor(panel, e=True, nurbsCurves=False)  # No NURBS curves
        cmds.modelEditor(panel, e=True, grid=False)  # No grid
        cmds.modelEditor(panel, e=True, cameras=False)  # No cameras
        cmds.modelEditor(panel, e=True, joints=False)  # No joints
        cmds.modelEditor(panel, e=True, locators=False)  # No locators
        cmds.modelEditor(panel, e=True, hud=False)  # No HUD
        cmds.modelEditor(panel, e=True, polymeshes=True)

        cmds.setAttr("hardwareRenderingGlobals.renderMode", 4)
        cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
        cmds.setAttr("hardwareRenderingGlobals.ssaoAmount", 1.0)  # Adjust strength
        cmds.setAttr("hardwareRenderingGlobals.ssaoRadius", 32.0)  # Adjust radius
        cmds.setAttr("hardwareRenderingGlobals.ssaoSamples", 32.0)  # Adjust radius
        cmds.setAttr("hardwareRenderingGlobals.ssaoFilterRadius", 32.0)  # Adjust radius

        # cmds.modelEditor('modelPanel4',
        #                  e=True,
        #                  displayLights="all")

        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)
        cmds.setAttr("hardwareRenderingGlobals.multiSampleCount", 8)  # 8x AA

    def setup_camera(self):
        camera_node = "camera_sc:camera"
        camera_node_shape = cmds.listRelatives(camera_node, shapes=True)[0]

        cams = cmds.ls(type='camera')
        states = {}
        for cam in cams:
            states[cam] = cmds.getAttr(cam + '.renderable')
            cmds.setAttr(cam + '.renderable', 0)

        cmds.setAttr(camera_node_shape + '.renderable', 1)

    def open_camera_scene(self):
        if self.camera_scene_path is not None:
            cmds.file(self.camera_scene_path,
                      i=True,
                      typ="Alembic",
                      ignoreVersion=True,
                      ra=True,
                      mergeNamespacesOnClash=False,
                      namespace="camera_sc",
                      pr=True,
                      importTimeRange="combine",
                      )
            self.setup_camera()

    def open_template(self):
        cmds.file(self.template_scene_path, open=True, force=True)

    def open_geometry_scene(self):
        if self.geo_scene_path is not None:
            cmds.file(self.geo_scene_path,
                      i=True,
                      typ="Alembic",
                      ignoreVersion=True,
                      ra=True,
                      mergeNamespacesOnClash=False,
                      namespace="geometry_sc",
                      pr=True,
                      importTimeRange="combine",
                      )
        else:
            print("Scene Setup Failed! Check Template", f"{self.geo_scene_path} NOT FOUND!")

    def setup_scene(self):
        if cmds.objExists("main|template|turntable_setup"):
            cmds.parentConstraint("main|template|turntable_setup", "geometry_sc:geo", maintainOffset=1)
        else:
            print("Scene Setup Failed! Check Template")
            return

    def run_playblast(self):
        self.fresh_scene()
        self.setup_playblast_options()
        self.open_template()
        self.open_geometry_scene()
        self.open_camera_scene()
        self.setup_scene()

        frames = cmds.playblast(
            startTime=int(self.frame_range[0]),
            endTime=int(self.frame_range[1]),
            format="image",
            filename=self.output_path,
            width=int(self.resolution[0]),
            height=int(self.resolution[1]),
            percent=self.resolution_percentage * 100,
            offScreen=True,
            viewer=False,
            compression="jpg",
            sequenceTime=0,
            clearCache=1,
            fp=4,
            quality=100,
            forceOverwrite=True
        )

        return {self.jpg_seq: frames}

    def images_to_mov(self,
            input_path,
            output_path,
            fps=24,
            file_format = "mov",
            codec="prores_ks",
            pix_fmt="yuv422p10le"):

        conform_input_path = None

        if not isinstance(input_path, Path):
            conform_input_path = Path(input_path).as_posix()

        ffmpeg_conform_path = self.hash_to_ffmpeg_patern(str(conform_input_path))

        if not isinstance(output_path, Path):
            conform_output_path = Path(output_path).as_posix()

        output_file_path = conform_output_path + "." + file_format

        (
            ffmpeg.input(ffmpeg_conform_path,
                         framerate=fps,
                         start_number='1001').output(
                                                    output_file_path,
                                                    vcodec=codec,
                                                    pix_fmt=pix_fmt,
                                                    r=fps,
                                                    movflags="faststart"
                                                    )
            .overwrite_output().run()
        )
        return output_file_path


    def hash_to_ffmpeg_patern(self, path):
        if "####" in path:
            count = path.count("#")
            return path.replace('#' * count, f'%0{count}d')
        return path


    def execute(self):
        captured_frames = self.run_playblast()
        encoded_video_path = self.images_to_mov(input_path=captured_frames['jpg_seq'], output_path=self.quicktime_path.as_posix())

        used_template_version = {"playblast_template": self.options["review_options"]["template_asset_ver_id"]}
        mov_version = {"review_mov": encoded_video_path}

        self.db_publisher = DBPublisher(options=self.options)
        self.db_publisher.create_db_file_components(
            db_asset_version_id=self.context_handler.db_asset_version_id,
            published_data=captured_frames,
            component_parent_id=self.context_handler.db_asset_version_id)

        self.db_publisher.create_db_custom_file_components(
            db_asset_version_id=self.context_handler.db_asset_version_id,
            published_data=used_template_version,
            component_parent_id=self.context_handler.db_asset_version_id)

        self.db_publisher.create_db_custom_file_components(
            db_asset_version_id=self.context_handler.db_asset_version_id,
            published_data=mov_version,
            component_parent_id=self.context_handler.db_asset_version_id)

        return captured_frames

