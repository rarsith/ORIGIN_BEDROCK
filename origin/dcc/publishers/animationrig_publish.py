import os

from origin.dcc.maya.exporters.anim_rig import MayaAnimationRigExporter
from origin.dcc.abc.animation_rig_exporter import AnimationRigExporter
from origin.envars.origin_envars import ContextHandler


class AnimationRigPublish:
    def __init__(self, publish_options):

        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}}
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.dcc = os.getenv("DCC")

        self.rigging_publisher = None

    def get_publisher_class(self, dcc):
        classes = {
            "maya": MayaAnimationRigExporter(options=self.publishing_options),
        }
        if dcc in list(classes.keys()):
            return classes[dcc]

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
