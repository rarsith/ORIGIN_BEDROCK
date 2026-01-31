import os
import re

from origin.dcc.publishers.handler.publisher_repository import get_dcc_exporter, PublisherType
from origin.envars.origin_envars import ContextHandler


class GeometryPublish:
    def __init__(self, options=None):
        self.exported_results = {"data": {}, "img_seq": {}, "quicktime": {}, "thumbnail": {}}

        self.geometry_exporter = None
        self.master_scene_exporter = None
        self.options = options

        self.context_handler: ContextHandler = self.options["context_object"]
        self.dcc = os.getenv("DCC")

        self.image_sequence_exporter = None
        self.quicktime_exporter = None

    def get_publisher_class(self, dcc):
        dcc_exporter = get_dcc_exporter(module_name=PublisherType.geometry, dcc=dcc)
        return dcc_exporter(options=self.options)

    def get_media_creator_publisher_class(self, review_medium):
        dcc_exporter = get_dcc_exporter(module_name=PublisherType.playblast, dcc=self.dcc)
        return dcc_exporter(options=self.options)

    def export_file_types(self):
        exported_data = {}
        self.geometry_exporter = self.get_publisher_class(dcc=self.dcc)
        collected_data = self.geometry_exporter.export()
        exported_data.update(collected_data)

        return exported_data

    def check_image_sequence(self):
        if "img_seq" in list(self.exported_results.keys()):
            self.quicktime_exporter = MakeMedia(img_seq_path=self.exported_results["img_seq"])

    def export_review_images(self):
        self.image_sequence_exporter = self.get_media_creator_publisher_class(review_medium=self.options["review_medium"])
        captured_frames = self.image_sequence_exporter.execute()
        return captured_frames

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

        if self.options["review_medium"] != "no preview":
            print(f"REVIEW OPTION FOUND: {self.options['review_medium']}")
            self.options["review_options"]['geo_scene_path'] = exported_geo_formats["abc"]
            img_seq = self.export_review_images()
            return [exported_geo_formats, img_seq]


        else:
            print(f"NO REVIEW OPTION FOUND: {self.options['review_medium']}")

        # return self.exported_results

