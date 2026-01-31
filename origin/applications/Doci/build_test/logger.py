# doci/logger.py
import json
from datetime import datetime


class PublishLogger:
    def __init__(self, log_path):
        self.log_path = log_path
        self.events = []

    def task_start(self, task):
        self._log(task, "start")

    def task_end(self, task):
        self._log(task, "end")

    def _log(self, task, event):
        self.events.append({
            "task": task.name,
            "event": event,
            "status": task.status.value,
            "time": datetime.utcnow().isoformat(),
            "outputs": task.outputs
        })
        self._flush()

    def _flush(self):
        with open(self.log_path, "w") as f:
            json.dump(self.events, f, indent=2)
