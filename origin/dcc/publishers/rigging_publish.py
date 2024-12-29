import os

from origin.dcc.maya.exporters.anim_rig import MayaAnimationRigExporter
from origin.dcc.abc.animation_rig_exporter import AnimationRigExporter
from origin.envars.origin_envars import ContextHandler


class AnimationRigPublish:
    def __init__(self, publish_options):

        self.exported_results = {"data": {}, "images": {}, "quicktime": {}}
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.dcc = os.getenv("DCC")

        self.rigging_publisher: AnimationRigExporter = self.get_publisher_class(dcc=self.dcc)

    def get_publisher_class(self, dcc):
        rigging_classes = {
            "maya": MayaAnimationRigExporter(objects_names=["main|rig"], context=self.context_handler),

        }
        if dcc in list(rigging_classes.keys()):
            return rigging_classes[dcc]

    def export_file_types(self):
        exported_data = {}

        collected_data = self.rigging_publisher.export_rigging("master")
        exported_data.update(collected_data)

        return exported_data

    def process_review_media(self):
        processed_reviews = {}
        return processed_reviews

    def publish(self):
        data_components = self.export_file_types()
        self.exported_results["data"] = data_components

        reviewable_components = self.process_review_media()

        return self.exported_results
