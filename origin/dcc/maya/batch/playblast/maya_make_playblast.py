import maya.standalone
import argparse
import re
import json
from pathlib import Path

import maya.cmds as cmds

from origin.dcc.env_setup import env_setup
env_setup()

from origin.envars.origin_envars import ContextHandler
from origin.paths.output_paths import OriginOSPathHandler

def ensure_alembic_plugin():
    plugin_name = "AbcImport"
    if not cmds.pluginInfo(plugin_name, query=True, loaded=True):
        print(f"Loading Alembic plugin: {plugin_name}")
        cmds.loadPlugin(plugin_name)
    else:
        print(f"Alembic plugin '{plugin_name}' is already loaded.")


class MayaMakePlayblast:
    jpg_seq = "jpg_seq"

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

    def set_output_path(self, file_format):
        self.path_handler = OriginOSPathHandler(context=self.context_handler, file_format=file_format)
        full_path = Path(self.path_handler.publish_path(branch_dir_name=self.path_handler.branch_pub_images,
                                                        create_dir=True)) / self.path_handler.output_file_name
        return full_path

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

        cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
        cmds.setAttr("hardwareRenderingGlobals.ssaoAmount", 1.0)  # Adjust strength
        cmds.setAttr("hardwareRenderingGlobals.ssaoRadius", 16.0)  # Adjust radius

        cmds.modelEditor('modelPanel4', e=True, displayLights="all")

        cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)
        cmds.setAttr("hardwareRenderingGlobals.multiSampleCount", 8)  # 8x AA

    def setup_camera(self):
        camera_node = "camera_sc:cam1"
        camera_node_shape = cmds.listRelatives(camera_node, shapes=True)[0]

        cams = cmds.ls(type='camera')
        states = {}
        for cam in cams:
            states[cam] = cmds.getAttr(cam + '.renderable')
            cmds.setAttr(cam + '.renderable', 0)

        cmds.setAttr(camera_node_shape + '.renderable', 1)

    def open_camera_scene(self):
        excluded_default_cameras = ["persp", "side", "front", "top"]
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

    def setup_scene(self):
        if cmds.objExists("main|template|turntable_setup"):
            cmds.parentConstraint("main|template|turntable_setup", "geometry_sc:geo", maintainOffset=1)
        else:
            print("Scene Setup Failed! Check Template")
            return

    def run_playblast(self):
        self.setup_playblast_options()
        self.open_template()
        self.open_geometry_scene()
        self.open_camera_scene()
        self.setup_scene()

        frames = cmds.playblast(
            startTime=self.frame_range[0],
            endTime=self.frame_range[1],
            format="image",
            filename=self.output_path,
            width=self.resolution[0],
            height=self.resolution[1],
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



    def execute(self):
        captured_frames = self.run_playblast()
        return captured_frames


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a Maya playblast in batch mode.")
    parser.add_argument("--options", type=str, required=True, help="Serialized JSON string of options.")
    return parser.parse_args()


def main():
    maya.standalone.initialize(name='python')

    try:

        ensure_alembic_plugin()

        args = parse_arguments()

        # Parse the options JSON string into a dictionary
        options = json.loads(args.options)

        # Extract review options from the provided options dictionary
        review_options = options.get("review_options", {})

        # Initialize the playblast object
        playblast_obj = MayaMakePlayblast(
            options=options,  # Pass the entire options dictionary
            frame_range=review_options.get("frame_range"),
            resolution=review_options.get("resolution"),
            resolution_percentage=review_options.get("resolution_percentage"),
            geo_scene_path=review_options.get("geo_scene_path"),
            camera_scene_path=review_options.get("camera_asset_ver_id"),
            template_scene_path=review_options.get("template_asset_ver_id"),
            output_path=review_options.get("output_path")
        )

        # Execute the playblast
        captured_frames = playblast_obj.execute()
        print("captured_frames:", captured_frames)
        return captured_frames

    finally:
        maya.standalone.uninitialize()


if __name__ == "__main__":
    main()
