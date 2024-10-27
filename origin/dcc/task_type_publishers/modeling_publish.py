import os

from origin.envars.origin_envars import ContextHandler
from origin.dcc.maya.exporters.geometry import MayaGeometryExporter, GeometryExporter


class ModelingPublish:
    def __init__(self, publish_options):

        self.exported_results = {"data": {}, "images": {}, "quicktime": {}}
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.dcc = os.getenv("DCC")

        self.geometry_publisher: GeometryExporter = self.get_geometry_publisher_class(dcc=self.dcc)

    def get_geometry_publisher_class(self, dcc):
        geometry_classes = {
            "maya": MayaGeometryExporter(objects_names=["main"], context=self.context_handler),

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



if __name__ == "__main__":
    context_sample = {'show_name': 'New_State',
                      'project_publishes': 'New_State__PUBLISHES',
                      'project_work': 'New_State__WORK',
                      'project_control': 'New_State__CONTROL',
                      'origin_path_hierarchy': 'assets.chr.yellow_hulk',
                      'entity_name': 'yellow_hulk',
                      'db_asset_id': 'New_State.assets.chr.yellow_hulk.modeling.gloves',
                      'entity_type': 'asset',
                      'entity_id': 'New_State.assets.chr.yellow_hulk',
                      'task_name': "modeling",
                      'task_type': "modeling"}

    context_class = ContextHandler()
    context_class.load_session(session_data=context_sample)

    publishing_options = {'db_asset_id': 'New_State.assets.chr.yellow_hulk.modeling.gloves_metalic',
                          'db_asset_qc': 'OK',
                          'user_file_formats': ['ABC', 'USD', 'OBJ'],
                          'persistent_file_formats': ['master'],
                          'all_sets_assigned': [],
                          'inject_textures_path': None,
                          'bundle_stream_id': '',
                          'review_options': ['Playblast'],
                          'pub_comment': 'asdfasdfzdf',
                          'pub_status': 'IN PROGRESS',
                          'context_object': context_class}

    maya_deo_exp = ModelingPublish(publish_options=publishing_options)
    maya_deo_exp.publish()
