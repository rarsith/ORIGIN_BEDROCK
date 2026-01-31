# doci/state.py
import json
import threading

class PublishState:
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self.tasks = {}

    def update(self, task):
        with self.lock:
            self.tasks[task.name] = {
                "status": task.status,
                "progress": task.progress
            }
            with open(self.path, "w") as f:
                json.dump(self.tasks, f, indent=2)
