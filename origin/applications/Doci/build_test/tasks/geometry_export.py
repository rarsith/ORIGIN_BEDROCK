# doci/tasks/geometry_export.py
from doci.tasks.base import Task
import subprocess


class GeometryExport(Task):
    def __init__(self, scene, out_dir, dependent=None):
        super().__init__("geometry_export", dependent)
        self.scene = scene
        self.out_dir = out_dir

    def _run(self, context):
        cmd = [
            context["mayapy"],
            context["geo_script"],
            self.scene,
            self.out_dir
        ]
        subprocess.run(cmd, check=True)

        return {
            "abc_dir": self.out_dir
        }
