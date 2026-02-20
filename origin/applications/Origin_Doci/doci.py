import os
import json
import shutil
import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from origin.dcc.common.batch_processing.batch_processing import BatchProcessing


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


def run_pipeline(options):
    print("INITIATING BATCH PUBLISH")
    publisher_type = BatchProcessing(options=options, task="publish")
    publisher_type.run()

    print("[DOCI] Pipeline complete")


class JsonHandler(FileSystemEventHandler):
    def __init__(self, root_folder):
        self.root_folder = Path(root_folder)
        self.incoming = self.root_folder / '_incoming'
        self.processing = self.root_folder / '_processing'
        self.failed = self.root_folder / '_failed'
        self.done = self.root_folder / '_done'
        self.tmp = self.root_folder / '__tmp__'

    def on_moved(self, event):
        if event.is_directory:
            return

        src = Path(event.dest_path)

        if not src.suffix == ".json":
            return

        self._claim_and_run(src)

        # self._handle(event)

    def on_created(self, event):
        if event.is_directory:
            return

        src = Path(event.src_path)

        if not src.suffix == ".json":
            return

        self._claim_and_run(src)

    def _claim_and_run(self, src_path):
        try:
            # 🔒 CLAIM JOB (atomic lock)
            processing_path = self.processing / src_path.name
            shutil.move(str(src_path), str(processing_path))

            print("[DOCI] Claimed job:", processing_path)

        except Exception:
            # another worker probably grabbed it first
            return

        try:
            with open(processing_path) as f:
                data = json.load(f)

            run_pipeline(data)

            # ✅ success
            shutil.move(str(processing_path), str(self.done / processing_path.name))
            print("[DOCI] Done")

        except Exception as e:
            print("[DOCI] Failed:", e)

            # ❌ failure
            shutil.move(str(processing_path), str(self.failed / processing_path.name))


class DociObserver:
    INCOMING = '_incoming'
    PROCESSING = '_processing'
    FAILED = '_failed'
    DONE = '_done'
    TMP = '__tmp__'

    def __init__(self, root_folder):

        self.root_folder = root_folder
        self.observer = None

    def create_watch_folders(self):
        inc = Path(self.root_folder) / self.INCOMING
        inc.mkdir(exist_ok=True)

        proc = Path(self.root_folder) / self.PROCESSING
        proc.mkdir(exist_ok=True)

        failed = Path(self.root_folder) / self.FAILED
        failed.mkdir(exist_ok=True)

        done = Path(self.root_folder) / self.DONE
        done.mkdir(exist_ok=True)

        tmp = Path(self.root_folder) / self.TMP
        tmp.mkdir(exist_ok=True)

        return inc, proc, failed, done

    def incoming_folder(self):
        inc, proc, failed, done = self.create_watch_folders()

        return inc

    def watch_publish(self):
        if self.observer and self.observer.is_alive():
            print ('[DOCI] Already Running!')
            return

        watch_folder = self.incoming_folder()

        self.observer = Observer()
        self.observer.schedule(JsonHandler(root_folder=self.root_folder), watch_folder, recursive=False)
        self.observer.start()

        print("[ORIGIN DOCI] Watching:", watch_folder)

        return self.observer.is_alive()


    def stop_watch_publish(self):
        if not self.observer:
            return

        print('[DOCI] Stopping watcher...')
        self.observer.stop()
        # self.observer.join()

        self.observer = None

    def check_observer_state(self):
        if not  self.observer:
            return 'no OBSERVER'
        if self.observer.is_alive():
            return "running"

        return 'stopped'


# if __name__ == "__main__":
#     root_path = r'X:\_doci'
#     tt = DociObserver(root_folder=root_path)
#     tt.watch_publish()

