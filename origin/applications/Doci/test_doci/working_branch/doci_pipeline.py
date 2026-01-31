import os
import json
import time
import subprocess
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent

MAYAPY = r"D:/Program Files/Autodesk/Maya2024/bin/mayapy.exe"
MAYA_SCRIPT = r"C:/Users/arsithra/PycharmProjects/ORIGIN_BEDROCK/origin/applications/Doci/test_doci/working_branch/maya_tasks.py"
WATCH_FOLDER = r"C:/Users/arsithra/PycharmProjects/ORIGIN_BEDROCK/origin/applications/Doci/test_doci/working_branch/dropbox"

# -----------------------------
# HELPERS
# -----------------------------
def wait_for_file(path, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(path):
            try:
                with open(path, "r"):
                    return True
            except IOError:
                pass
        time.sleep(1.0)
    return False


def run_maya(task, args):
    cmd = [MAYAPY, MAYA_SCRIPT, task, *args]
    result = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        print(line.strip())
        if line.startswith("DOCI_RESULT::"):
            return line.replace("DOCI_RESULT::", "").strip()

    return None

# -----------------------------
# PIPELINE
# -----------------------------
def run_pipeline(data):
    publish_scene = data["publish_scene"]
    turntable_scene = data["turntable_scene"]
    camera_file = data["camera_scene"]
    base_output = data["output_dir"]

    geo_dir = str(Path(base_output) /  "cache")
    pb_dir = str(Path(base_output) / "playblast")
    mov_path = str(Path(base_output) / "preview.mov")

    # 1️⃣ Export Alembic (producer)
    abc_path = run_maya(
        "export_geo",
        [publish_scene, geo_dir]
    )

    # 2️⃣ Playblast from cache (consumer)
    run_maya(
        "playblast_from_cache",
        [turntable_scene, abc_path, camera_file, pb_dir]
    )

    # 3️⃣ Encode movie
    encode_movie(pb_dir, mov_path)

    print("[DOCI] Pipeline complete")

# -----------------------------
# NON-MAYA TASK
# -----------------------------
def encode_movie(image_dir, mov_path):
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", "24",
        "-start_number", "970",
        "-i", str(Path(image_dir) / "playblast.%04d.png"),
        "-c:v", "libx264",
        mov_path
    ]
    subprocess.run(cmd, check=True)

    for line in subprocess.check_output(cmd):
        print(line)


# -----------------------------
# WATCHDOG
# -----------------------------
class JsonHandler(FileSystemEventHandler):

    def on_created(self, event):
        self._handle(event)

    # def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
    #     self._handle(event)

    def _handle(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".json"):
            return

        print("[DOCI] Detected job:", event.src_path)

        if not wait_for_file(event.src_path):
            return

        with open(event.src_path) as f:
            data = json.load(f)

        run_pipeline(data)

# -----------------------------
# MAIN
# -----------------------------
def main():
    observer = Observer()
    observer.schedule(JsonHandler(), WATCH_FOLDER, recursive=False)
    observer.start()

    print("[DOCI] Watching:", WATCH_FOLDER)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    print("[DOCI] Done")


if __name__ == "__main__":
    main()

