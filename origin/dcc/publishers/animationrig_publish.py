import os

from origin.dcc.publishers.handler.publisher_repository import get_dcc_exporter, PublisherType
from origin.envars.origin_envars import ContextHandler


class AnimationRigPublish:
    def __init__(self, options):

        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}}
        self.options = options
        self.context_handler: ContextHandler = self.options["context_object"]
        self.dcc = os.getenv("DCC")

        self.rigging_publisher = None

    def get_publisher_class(self, dcc):
        dcc_exporter = get_dcc_exporter(module_name=PublisherType.anim_rig, dcc=dcc)
        return dcc_exporter(options=self.options)

    def export_file_types(self):
        exported_data = {}

        self.rigging_publisher = self.get_publisher_class(dcc=self.dcc)

        collected_data = self.rigging_publisher.export("master")
        exported_data.update(collected_data)

        return exported_data

    def process_review_media(self):
        processed_reviews = {}
        return processed_reviews

    def publish(self):
        self.export_file_types()
        self.process_review_media()

        return self.exported_results
