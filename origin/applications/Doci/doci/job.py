import uuid
import time

class Job:
    def __init__(self, event):
        self.id = str(uuid.uuid4())
        self.event = event
        self.status = "pending"
        self.created = time.time()

    def __repr__(self):
        return f"<Job {self.id} {self.status}>"