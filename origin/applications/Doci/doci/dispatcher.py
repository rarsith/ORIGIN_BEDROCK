from job import Job

class Dispatcher:
    def __init__(self, executor):
        self.executor = executor

    def submit(self, event):
        job = Job(event)
        print("Dispatching", job)
        self.executor.execute(job)