import os
import re
from origin.dcc.publishers.make_playblast import MakePlayblast
from origin.envars.origin_envars import ContextHandler
from origin.dcc.maya.publish.exporters.OLD_geometry import MayaGeometryExporter
from origin.dcc.blender.exporters.geometry import BlenderGeometryExporter
from origin.dcc.abc.geometry_exporter import GeometryExporter


class GeometryPublish:
    def __init__(self, publish_options=None):
        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}, "thumbnail": {}}

        self.publishing_options = publish_options

        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.dcc = os.getenv("DCC")

        self.geometry_exporter: GeometryExporter = self.get_geometry_exporter_class(dcc=self.dcc)
        self.image_sequence_exporter = None
        self.quicktime_exporter = None

    def get_geometry_exporter_class(self, dcc):
        geometry_classes = {
            "maya": MayaGeometryExporter(objects_names=["main|geo"], context=self.context_handler),
            "blender": BlenderGeometryExporter(objects_names=["main|geo"], context=self.context_handler),

        }
        if dcc in list(geometry_classes.keys()):
            return geometry_classes[dcc]

    def get_media_creator_publisher_class(self, review_medium):
        if review_medium is not None:
            get_media_creator_publisher = {
                "playblast": MakePlayblast(options=self.publishing_options)
                # "render": MakeRender(context=self.context_handler, options=review_options)
            }
            return get_media_creator_publisher[self.publishing_options["review_medium"]]
        return None

    def export_file_types(self):
        exported_data = {}

        if self.publishing_options["persistent_file_formats"]:
            for persistent_file_format in self.publishing_options["persistent_file_formats"]:
                collected_data = self.geometry_exporter.export_geometry(persistent_file_format)

                exported_data.update(collected_data)

        if self.publishing_options["user_file_formats"]:
            for file_format in self.publishing_options["user_file_formats"]:
                collected_data = self.geometry_exporter.export_geometry(file_format)

                exported_data.update(collected_data)

        return exported_data

    def check_review_options(self):
        if "review_medium" in list(self.publishing_options.keys()):
            return self.publishing_options["review_medium"]
        return None

    def check_image_sequence(self):
        if "img_seq" in list(self.exported_results.keys()):
            self.quicktime_exporter = MakeMedia(img_seq_path=self.exported_results["img_seq"])

    def export_review_images(self):
        self.image_sequence_exporter = self.get_media_creator_publisher_class(review_medium=self.check_review_options())

        exported_images_seq = {}

        if self.image_sequence_exporter is not None:
            collected_data = self.image_sequence_exporter.execute()
            exported_images_seq.update(collected_data)
        return exported_images_seq

    def create_review_quicktime(self):
        exported_quicktimes = {}
        self.check_image_sequence()

        if self.quicktime_exporter is not None:
            collected_data = self.quicktime_exporter.export()
            exported_quicktimes.update(collected_data)

        return exported_quicktimes

    def extract_captured_frames(self, log_text):
        for line in log_text.splitlines():  # Split the text into lines
            if "captured_frames:" in line:
                match = re.search(r"captured_frames:\s*(.+)", line)
                if match:
                    return match.group(1).strip()  # Extract the path after 'captured_frames:'
        return None

    def publish(self):
        data_components = self.export_file_types()
        self.exported_results["data"] = data_components
        self.publishing_options["review_options"]['geo_scene_path'] = self.exported_results["data"]["abc"]

        self.export_review_images()

        return self.exported_results

