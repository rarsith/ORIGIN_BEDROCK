import json
from watchdog.events import FileSystemEventHandler

class OriginWatcher(FileSystemEventHandler):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def on_created(self, event):
        if not event.src_path.endswith(".json"):
            return

        with open(event.src_path) as f:
            data = json.load(f)

        self.dispatcher.submit(data)