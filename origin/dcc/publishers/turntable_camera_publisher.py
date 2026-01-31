import os

# from origin.dcc.blender.exporters.camera import BlenderCameraExporter
# from origin.dcc.maya.publish.exporters.camera import MayaCameraExporter
from origin.dcc.publishers.handler.publisher_repository import get_dcc_exporter, PublisherType
from origin.envars.origin_envars import ContextHandler


class TurntableCameraPublish:
    def __init__(self, options=None):
        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}}
        self.options = options

        if self.options is not None:
            self.context_handler = self.options["context_object"]
            if isinstance(self.context_handler, dict):
                self.context_handler = ContextHandler()
                self.context_handler.load_session(self.options["context_object"])

        self.dcc = os.getenv("DCC")

        self.camera_publisher = self.get_publisher_class(dcc=self.dcc)

    def entity_properties(self):
        entity_doc = self.context_handler.database_handler().get_asset_document()
        entity_properties = entity_doc.definition
        return entity_properties

    def get_publisher_class(self, dcc):
        dcc_exporter = get_dcc_exporter(module_name=PublisherType.camera, dcc=dcc)
        return dcc_exporter(options=self.options)

    def export_file_types(self):
        exported_data = {}
        self.camera_publisher = self.get_publisher_class(dcc=self.dcc)
        collected_data = self.camera_publisher.run_export()
        exported_data.update(collected_data)

        return exported_data

    def process_review_media(self):
        processed_reviews = {}
        return processed_reviews

    def publish(self):
        self.export_file_types()
        self.process_review_media()

        return self.exported_results
