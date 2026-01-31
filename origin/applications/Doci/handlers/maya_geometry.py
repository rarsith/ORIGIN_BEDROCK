import subprocess
import os

from origin.dcc.common.utils.executables import set_executable

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