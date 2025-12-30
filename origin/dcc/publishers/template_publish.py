import os

from origin.dcc.maya.exporters.template import MayaPlayblastTemplateExporter
from origin.envars.origin_envars import ContextHandler


class TemplatePublish:
    def __init__(self, publish_options):

        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}}
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.dcc = os.getenv("DCC")

        self.publisher = None

    def get_publisher_class(self, dcc):
        exporter_classes = {
            "maya": MayaPlayblastTemplateExporter(options=self.publishing_options)
        }
        if dcc in list(exporter_classes.keys()):
            return exporter_classes[dcc]

    def export_file_types(self):
        exported_data = {}
        self.publisher = self.get_publisher_class(dcc=self.dcc)
        collected_data = self.publisher.export("master")
        exported_data.update(collected_data)

        return exported_data

    def publish(self):
        self.export_file_types()
        return self.exported_results
