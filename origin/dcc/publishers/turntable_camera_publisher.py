import os

from origin.dcc.blender.exporters.camera import BlenderCameraExporter
from origin.dcc.maya.publish.exporters.camera import MayaCameraExporter
from origin.envars.origin_envars import ContextHandler


class TurntableCameraPublish:
    def __init__(self, publish_options):
        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}}
        self.publishing_options = publish_options

        self.context_handler = self.publishing_options["context_object"]

        if isinstance(self.context_handler, dict):
            self.context_handler = ContextHandler()
            self.context_handler.load_session(self.publishing_options["context_object"])

        self.dcc = os.getenv("DCC")

        self.camera_publisher = self.get_camera_publisher_class(dcc=self.dcc)

    def entity_properties(self):
        entity_doc = self.context_handler.database_handler().get_asset_document()
        entity_properties = entity_doc.definition
        return entity_properties

    def get_camera_publisher_class(self, dcc):
        entity_properties = self.entity_properties()
        camera_classes = {
            "maya": MayaCameraExporter(options=self.publishing_options,
                                       camera_name="turntable_camera:cam1",
                                       start_frame=entity_properties["full_range_in"],
                                       end_frame=entity_properties["full_range_out"],
                                       ),
            "blender": BlenderCameraExporter(camera_name="turntable_camera:cam1"),

        }
        if dcc in list(camera_classes.keys()):
            return camera_classes[dcc]

    def export_file_types(self):
        exported_data = {}
        self.camera_publisher = self.get_camera_publisher_class(dcc=self.dcc)
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
