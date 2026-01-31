import os

from origin.dcc.common.abc.camera_exporter import CameraExporter
from origin.dcc.extensions.blender.exporters.camera import BlenderCameraExporter
from origin.dcc.extensions.maya.publish.exporters.camera import MayaCameraExporter
from origin.envars.origin_envars import ContextHandler
from origin.dcc.publishers.handler.publisher_repository import get_dcc_exporter, PublisherType


class CameraPublish:
    def __init__(self, options):
        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}}
        self.options = options
        self.context_handler: ContextHandler = self.options["context_object"]
        self.dcc = os.getenv("DCC")

        self.camera_publisher: CameraExporter = self.get_publisher_class(dcc=self.dcc)

    def entity_properties(self):
        entity_doc = self.context_handler.database_handler().get_asset_document()
        entity_properties = entity_doc.definition
        return entity_properties

    def get_publisher_class(self, dcc):
        entity_properties = self.entity_properties()
        camera_classes = {
            "maya": MayaCameraExporter(camera_name="shot_cam",
                                       start_frame=entity_properties["full_range_in"],
                                       end_frame=entity_properties["full_range_out"],
                                       context=self.context_handler),
            "blender": BlenderCameraExporter(camera_name="turntable_camera:cam1"),

        }
        if dcc in list(camera_classes.keys()):
            return camera_classes[dcc]

    def export_file_types(self):
        exported_data = {}

        master_scene_data = self.camera_publisher.run_export(file_format="master")
        exported_data.update(master_scene_data)

        alembic_scene_data = self.camera_publisher.run_export(file_format="abc")
        exported_data.update(alembic_scene_data)

        usd_scene_data = self.camera_publisher.run_export(file_format="usd")
        exported_data.update(usd_scene_data)

        return exported_data

    def process_review_media(self):
        processed_reviews = {}
        return processed_reviews

    def publish(self):
        data_components = self.export_file_types()
        self.exported_results["data"] = data_components

        reviewable_components = self.process_review_media()

        return self.exported_results
