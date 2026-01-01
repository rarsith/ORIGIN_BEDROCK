from concurrent.futures import ProcessPoolExecutor
from origin.applications.Doci.handlers import publish

class LocalExecutor:
    def __init__(self, max_workers=4):
        self.pool = ProcessPoolExecutor(max_workers=max_workers)

    def execute(self, job):
        for task in job.event.get("tasks", []):
            self.pool.submit(self.run_task, task, job.event)

    @staticmethod
    def run_task(task, event):
        handler = publish.get_handler(task["type"])
        handler.run(task, event)