from origin.database.publisher.db_publisher import DBPublisher
from origin.dcc.maya.batch.tasks.abc.batch_task import BatchTask
from origin.dcc.save_session import scene_session_operations_class
from origin.dcc.task_type_publisher import PublisherType
from origin.envars.origin_envars import ContextHandler


class MayaPublishTask(BatchTask):
    def execute(self):
        if isinstance(self.options["context_object"], dict):
            context_handler = ContextHandler()
            context_handler.load_session(self.options["context_object"])
        else:
            context_handler = self.options["context_object"]

        db_publisher = DBPublisher(options=self.options)

        db_asset_id = db_publisher.create_db_asset(context=context_handler,
                                                   parent=context_handler.db_asset_stream_id,
                                                   publish_type=self.options["publish_type"])

        context_handler.db_asset_id = db_asset_id

        db_asset_version_id = db_publisher.create_db_asset_version(context=context_handler,
                                                                   parent_id=context_handler.db_asset_id)
        context_handler.db_asset_version_id = db_asset_version_id

        self.options["context_object"] = context_handler

        obj = PublisherType(publish_options=self.options)
        publish_results = obj.execute_publish()

        db_publisher.create_asset_breakdown_version(context=context_handler)

        db_publisher.create_stack_version(context=context_handler)



