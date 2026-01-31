# doci/tasks/playblast_export.py
class PlayblastExport(Task):
    def __init__(self, playblast_scene, dependent):
        super().__init__("playblast_export", dependent)
        self.scene = playblast_scene

    def _run(self, context):
        abc_dir = self.dependent.outputs["abc_dir"]

        cmd = [
            context["mayapy"],
            context["playblast_script"],
            self.scene,
            abc_dir
        ]
        subprocess.run(cmd, check=True)

        return {
            "frames_dir": f"{abc_dir}/playblast"
        }
