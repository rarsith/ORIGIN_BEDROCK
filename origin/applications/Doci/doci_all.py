import sys
import os
import maya.standalone
import maya.cmds as cmds

import subprocess
import os

from origin.dcc.common.utils.executables import set_executable
from origin.applications.Doci.handlers.maya_geometry import MayaGeometryPublish

HANDLERS = {
    MayaGeometryPublish.JOB_TYPE: MayaGeometryPublish()
}


def load_additional_plugins():
    import maya.cmds as cmds

    plugins = ["AbcImport", "AbcExport", "objExport"]
    for plugin in plugins:
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            print(f"Loading plugin: {plugin}")
            cmds.loadPlugin(plugin)
        else:
            print(f"'{plugin}' is already loaded.")


def publish_geometry(scene_path, output_dir):

    maya.standalone.initialize(name="python")

    load_additional_plugins()

    cmds.file(scene_path, open=True, force=True)

    geo_grp = "main|geo"
    if not cmds.objExists(geo_grp):
        raise RuntimeError("GEO group not found")

    cmds.select(geo_grp, hierarchy=True)

    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "geometry_publish.abc")

    cmds.AbcExport(
        j=f"-root {geo_grp} -file {out_file}"
    )

    print(f"[MAYA] Geometry published to {out_file}")





app_path = r"D:\Program Files\Autodesk\Maya2024"

os.environ["DCC"] = "maya"
os.environ["APP"] = app_path
os.environ["APP_BIN"] = os.path.join(app_path, "bin")

MAYAPY = set_executable()  # assume env is set correctly



SCRIPT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..", "Doci", "publish_geomery.py"
    )
)

class MayaGeometryPublish:
    JOB_TYPE = "maya_geometry_publish"

    def run(self, job):
        scene = job.payload["scene"]
        output = job.payload["output_dir"]

        cmd = [
            MAYAPY,
            SCRIPT,
            scene,
            output
        ]

        print("[DOCI] Running:", " ".join(cmd))
        subprocess.run(cmd, check=True)





class Executor:
    def execute(self, job):
        handler = HANDLERS.get(job.job_type)
        if not handler:
            raise RuntimeError(f"No handler for {job.job_type}")

        handler.run(job)

class Job:
    def __init__(self, job_type, payload):
        self.job_type = job_type
        self.payload = payload

from origin.applications.Doci.doci.job import Job
from origin.applications.Doci.doci.executor import Executor


def run_sample():
    job = Job(
        job_type="maya_geometry_publish",
        payload={
            "scene": "X:/projects/Small_Rock/assets/characters/hulk/modeling/publishes/data/geometry__hulk__hulk_MAIN/characters__hulk__hulk_MAIN__v0002/origin_scene/characters__hulk__hulk_MAIN__v0002.mb",
            "output_dir": "X:/projects/Small_Rock/assets/characters/hulk/modeling/publishes/data/geometry__hulk__hulk_MAIN/characters__hulk__hulk_MAIN__v0002"
        }
    )

    Executor().execute(job)

if __name__ == "__main__":
    run_sample()







if __name__ == "__main__":
    scene = sys.argv[1]
    output = sys.argv[2]
    publish_geometry(scene, output)