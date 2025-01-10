from origin.dcc.maya.batch.tasks.abc.batch_task import BatchTask
from origin.dcc.task_type_publisher import PublisherType


class MayaPublishTask(BatchTask):
    def execute(self):
        obj = PublisherType(publish_options=self.options)
        obj.execute_publish()
