import os

from origin.dcc.maya.exporters.anim_rig import MayaAnimRiggingExporter, AnimRiggingExporter
from origin.envars.origin_envars import ContextHandler


class RiggingPublish:
    def __init__(self, publish_options):

        self.exported_results = {"data": {}, "images": {}, "quicktime": {}}
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.dcc = os.getenv("DCC")

        self.rigging_publisher: AnimRiggingExporter = self.get_publisher_class(dcc=self.dcc)

    def get_publisher_class(self, dcc):
        rigging_classes = {
            "maya": MayaAnimRiggingExporter(objects_names=["main|rig"], context=self.context_handler),

        }
        if dcc in list(rigging_classes.keys()):
            return rigging_classes[dcc]

    def export_file_types(self):
        exported_data = {}

        if self.publishing_options["persistent_file_formats"]:
            for persistent_file_format in self.publishing_options["persistent_file_formats"]:
                collected_data = self.rigging_publisher.export_rigging(persistent_file_format)

                exported_data.update(collected_data)

        # if self.publishing_options["user_file_formats"]:
        #     for file_format in self.publishing_options["user_file_formats"]:
        #         collected_data = self.rigging_publisher.export_rigging(file_format)
        #
        #         exported_data.update(collected_data)

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
                      'task_name': "rigging",
                      'task_type': "rigging"}

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
