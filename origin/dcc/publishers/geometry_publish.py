import os
import re

from origin.dcc.maya.exporters.geometry import MayaGeometryExporter
from origin.dcc.publishers.make_playblast import MakePlayblast
from origin.envars.origin_envars import ContextHandler


class GeometryPublish:
    def __init__(self, publish_options=None):
        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}, "thumbnail": {}}

        self.geometry_exporter = None
        self.master_scene_exporter = None
        self.publishing_options = publish_options

        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.dcc = os.getenv("DCC")

        self.image_sequence_exporter = None
        self.quicktime_exporter = None

    def get_geometry_exporter_class(self, dcc):
        geometry_classes = {
            "maya": MayaGeometryExporter(options=self.publishing_options),
            # "blender": BlenderGeometryExporter(objects_names=["main|geo"], context=self.context_handler),

        }
        if dcc in list(geometry_classes.keys()):
            return geometry_classes[dcc]

    def get_media_creator_publisher_class(self, review_medium):
        get_media_creator_publisher = {
            "playblast": MakePlayblast(options=self.publishing_options)
            # "render": MakeRender(context=self.context_handler, options=review_options)
        }
        if review_medium in list(get_media_creator_publisher.keys()):
            return get_media_creator_publisher[review_medium]

    def export_file_types(self):
        exported_data = {}
        self.geometry_exporter = self.get_geometry_exporter_class(dcc=self.dcc)
        collected_data = self.geometry_exporter.export()
        exported_data.update(collected_data)

        return exported_data

    def check_image_sequence(self):
        if "img_seq" in list(self.exported_results.keys()):
            self.quicktime_exporter = MakeMedia(img_seq_path=self.exported_results["img_seq"])

    def export_review_images(self):
        self.image_sequence_exporter = self.get_media_creator_publisher_class(review_medium=self.publishing_options["review_medium"])
        self.image_sequence_exporter.execute()

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
        exported_geo_formats = self.export_file_types()

        if self.publishing_options["review_medium"] != "no preview":
            print(f"REVIEW OPTION FOUND: {self.publishing_options['review_medium']}")
            self.publishing_options["review_options"]['geo_scene_path'] = exported_geo_formats["abc"]
            self.export_review_images()

        else:
            print(f"NO REVIEW OPTION FOUND: {self.publishing_options['review_medium']}")

        # return self.exported_results

