import os

from origin.dcc.maya.exporters.template import MayaPlayblastTemplateExporter
from origin.dcc.abc.template_exporter import TemplateExporter
from origin.envars.origin_envars import ContextHandler


class TemplatePublish:
    def __init__(self, publish_options):

        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}}
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.dcc = os.getenv("DCC")

        self.publisher: TemplateExporter = self.get_publisher_class(dcc=self.dcc)

    def get_publisher_class(self, dcc):
        exporter_classes = {
            "maya": MayaPlayblastTemplateExporter(objects_names=["main|template"], context=self.context_handler),

        }
        if dcc in list(exporter_classes.keys()):
            return exporter_classes[dcc]

    def export_file_types(self):
        exported_data = {}

        collected_data = self.publisher.export("master")
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
