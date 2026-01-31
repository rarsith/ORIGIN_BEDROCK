# doci/tasks/base.py
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class Task(ABC):
    def __init__(self, name, dependent=None):
        self.name = name
        self.dependent = dependent
        self.status = TaskStatus.PENDING
        self.started_at = None
        self.finished_at = None
        self.progress = 0
        self.outputs = {}

    def can_run(self):
        return self.dependent is None or self.dependent.status == TaskStatus.DONE

    def run(self, context):
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.utcnow()

        try:
            self.outputs = self._run(context)
            self.status = TaskStatus.DONE
        except Exception:
            self.status = TaskStatus.FAILED
            raise
        finally:
            self.finished_at = datetime.utcnow()

    def update_progress(self, value):
        self.progress = value

    @abstractmethod
    def _run(self, context):
        """Return dict of outputs"""
        pass
