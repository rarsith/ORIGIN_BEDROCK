import maya.cmds as cmds
from maya.OpenMaya import MGlobal as om
from origin.dcc.abc.camera_exporter import CameraExporter


class MayaCameraExporter(CameraExporter):
    def __init__(self, camera_name, start_frame=None, end_frame=None):
        self.camera_name = camera_name
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.camera_transform = None
        self.camera_shape = None
        self.get_camera_nodes()

    def save_master_file(self):
        pass

    def get_camera_nodes(self):
        # Get the transform and shape node of the camera
        if cmds.objExists(self.camera_name):
            self.camera_transform = self.camera_name
            self.camera_shape = cmds.listRelatives(self.camera_transform, shapes=True)[0]
        else:
            om.MGlobal.displayError(f"Camera '{self.camera_name}' does not exist.")
            raise ValueError("Invalid camera name")

    def set_camera_specs(self, focal_length=None, filmback=None, resolution_gate=None):
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

    def bake_animation(self):
        # Bake animation if camera is animated and frame range is provided
        if self.start_frame and self.end_frame:
            cmds.bakeResults(self.camera_transform, t=(self.start_frame, self.end_frame),
                             sampleBy=1, simulation=True,
                             disableImplicitControl=True, preserveOutsideKeys=False)
            om.MGlobal.displayInfo("Animation baked successfully.")

    def export_camera(self, export_path, file_format="ma"):
        # Export the camera based on the specified format
        if file_format == "ma":
            cmds.select(self.camera_transform)
            cmds.file(export_path, force=True, options="v=0;", type="mayaAscii", exportSelected=True)
            om.MGlobal.displayInfo(f"Camera exported as .ma to {export_path}.")
        elif file_format == "abc":
            self.export_alembic(export_path)
        elif file_format == "usd":
            self.export_usd(export_path)
        else:
            om.MGlobal.displayError(f"Unsupported format: {file_format}")

    def export_alembic(self, export_path):
        # Export the camera to Alembic
        start_frame = self.start_frame if self.start_frame else cmds.playbackOptions(query=True, minTime=True)
        end_frame = self.end_frame if self.end_frame else cmds.playbackOptions(query=True, maxTime=True)

        abc_cmd = (f"-frameRange {start_frame} {end_frame} "
                   f"-root {self.camera_transform} "
                   "-stripNamespaces -worldSpace -writeVisibility "
                   f"-file {export_path}")
        cmds.AbcExport(j=abc_cmd)
        om.MGlobal.displayInfo(f"Camera exported as .abc to {export_path}.")

    def export_usd(self, export_path):
        # Export the camera to USD
        cmds.select(self.camera_transform)
        usd_options = {"shadingMode": "none", "exportDisplayColor": False}
        if self.start_frame and self.end_frame:
            usd_options.update({"startTime": self.start_frame, "endTime": self.end_frame})

        cmds.file(export_path, force=True, options=usd_options, type="USD Export", exportSelected=True)
        om.MGlobal.displayInfo(f"Camera exported as .usd to {export_path}.")

    def run_export(self, focal_length=None, filmback=None, resolution_gate=None, export_path=None, file_format="ma"):
        # Set the camera specifications
        self.set_camera_specs(focal_length=focal_length, filmback=filmback, resolution_gate=resolution_gate)

        # Bake animation if it's an animated camera
        self.bake_animation()

        # Export the camera
        if export_path:
            self.export_camera(export_path, file_format=file_format)
        else:
            om.MGlobal.displayError("No export path specified.")
