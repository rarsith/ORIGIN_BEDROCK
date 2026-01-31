# doci/publish.py
class Publish:
    def __init__(self, context, logger, tasks, state):
        self.tasks = []
        self.context = context
        self.state = state
        self.logger = logger

    def addTask(self, task):
        self.tasks.append(task)
        return task

    def run(self):
        for task in self.tasks:
            task.status = 'running'
            if not task.can_run():
                raise RuntimeError(f"Dependency not met for {task.name}")

            self.state.update(task)
            self.logger.task_start(task)

            task.run(self.context)

            task.status = 'done'
            task.progress = 100

            self.state.update(task)
            self.logger.task_end(task)
