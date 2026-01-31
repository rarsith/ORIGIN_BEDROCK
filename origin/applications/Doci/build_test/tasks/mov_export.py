# doci/tasks/mov_export.py
class MovExport(Task):
    def __init__(self, dependent):
        super().__init__("mov_export", dependent)

    def _run(self, context):
        frames = self.dependent.outputs["frames_dir"]
        movie = frames.replace("playblast", "preview.mov")

        cmd = [
            "ffmpeg",
            "-y",
            "-framerate", "24",
            "-i", f"{frames}/playblast.%04d.png",
            "-c:v", "libx264",
            movie
        ]
        subprocess.run(cmd, check=True)

        return {"movie": movie}
