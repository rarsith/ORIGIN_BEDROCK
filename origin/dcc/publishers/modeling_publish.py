import os

from origin.envars.origin_envars import ContextHandler
from origin.dcc.maya.exporters.geometry import (MayaGeometryExporter)
from origin.dcc.blender.exporters.geometry import BlenderGeometryExporter
from origin.dcc.abc.geometry_exporter import GeometryExporter


class GeometryPublish:
    def __init__(self, publish_options):
        self.exported_results = {"data": {}, "images": {}, "quicktime": {}}
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.dcc = os.getenv("DCC")

        self.geometry_publisher: GeometryExporter = self.get_geometry_publisher_class(dcc=self.dcc)

    def get_geometry_publisher_class(self, dcc):
        geometry_classes = {
            "maya": MayaGeometryExporter(objects_names=["main|geo"], context=self.context_handler),
            "blender": BlenderGeometryExporter(objects_names=["main|geo"], context=self.context_handler),

        }
        if dcc in list(geometry_classes.keys()):
            return geometry_classes[dcc]

    def export_file_types(self):
        exported_data = {}

        if self.publishing_options["persistent_file_formats"]:
            for persistent_file_format in self.publishing_options["persistent_file_formats"]:
                collected_data = self.geometry_publisher.export_geometry(persistent_file_format)

                exported_data.update(collected_data)

        if self.publishing_options["user_file_formats"]:
            for file_format in self.publishing_options["user_file_formats"]:
                collected_data = self.geometry_publisher.export_geometry(file_format)

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
