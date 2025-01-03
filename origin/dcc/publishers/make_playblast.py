import os
import pprint
import re

from origin.dcc.maya.batch.maya_batch import run_maya_batch_script
from origin.envars.origin_envars import ContextHandler


class MakePlayblast:
    jpg_seq = "jpg_seq"

    def __init__(self, options=None):
        self.exported_results = {"frames": []}
        self.publishing_options = options
        if self.publishing_options is not None:
            self.context_handler: ContextHandler = self.publishing_options["context_object"]

        self.dcc = os.getenv("DCC")

        # self.make_playblast_class = self.get_playblast_class(dcc=self.dcc)

    # def get_playblast_class(self, dcc):
    #     classes = {
    #         "maya": run_maya_batch_script(script_path="/origin/dcc/maya/batch/playblast/maya_make_playblast.py",
    #                                       options=self.publishing_options)
    #
    #         # "blender": BlenderMakePlayblast(context=self.context_handler),
    #
    #     }
    #     if dcc in list(classes.keys()):
    #         return classes[dcc]

    # def make_playblast(self):
    #     exported_data = []
    #
    #     collected_data = self.make_playblast_class.execute()
    #     exported_data.append(collected_data)
    #
    #     return exported_data



    def execute(self):
        frames = run_maya_batch_script(script_path="E:/Local_projects/PycharmProjects/ORIGIN_BEDROCK/origin/dcc/maya/batch/playblast/maya_make_playblast.py",
                                       options=self.publishing_options)

        self.exported_results["frames"].append(frames)

        # quicktime_component = self.create_review_quicktime()
        # self.exported_results["quicktime"] = quicktime_component

        return self.exported_results


if __name__ == "__main__":
    pass
    # context_sample = {'show_name': 'The_Rock',
    #                   'project_publishes': 'The_Rock__PUBLISHES',
    #                   'project_work': 'The_Rock__WORK',
    #                   'project_control': 'The_Rock__CONTROL',
    #                   'origin_path_hierarchy': 'assets.chr',
    #                   'entity_name': 'tafer',
    #                   'entity_id': 'The_Rock.assets.chr.tafer',
    #                   'entity_type': 'asset',
    #                   'task_name': "modeling",
    #                   'task_type': "modeling",
    #                   'task_id': "The_Rock.assets.chr.tafer.modeling",
    #                   'db_asset_id': 'The_Rock.assets.chr.tafer.geometry.tafer_main',
    #                   'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer_main',
    #                   }
    #
    # options = {'publish_type': 'image_seq', 'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer_main',
    #            'context_object': context_sample, 'db_asset_qc': 'OK', 'user_file_formats': ['abc', 'usd', 'obj'],
    #            'persistent_file_formats': ['master'], 'material_collections': {}, 'inject_textures_path': None,
    #            'stack_db_asset_id': 'The_Rock.assets.chr.tafer.tafer_main.asset_stack', 'review_medium': 'playblast',
    #            'review_options': {'frame_range': (1001, 1101),
    #                               'resolution': (1920, 1080),
    #                               'resolution_percentage': 0.5,
    #                               'template_asset_ver_id': 'E:/__ORIGIN_PROJECTS__/projects/The_Rock/templates/maya/playblast/template/publishes/data/template__playblast__playblast_main/maya__playblast__playblast_main__v0004/origin_scene/maya__playblast__playblast_main__v0004.mb',
    #                               'camera_asset_ver_id': 'E:/__ORIGIN_PROJECTS__/projects/The_Rock/assets/chr/tafer/modeling/publishes/data/turntable_camera__tafer__tafer_main/chr__tafer__tafer_main__v0004/alembic/chr__tafer__tafer_main__v0004.abc',
    #                               'geo_scene_path': 'E:/__ORIGIN_PROJECTS__/projects/The_Rock/assets/chr/tafer/modeling/publishes/data/geometry__tafer__tafer_main/chr__tafer__tafer_main__v0055/alembic/chr__tafer__tafer_main__v0055.abc'}}

    # context_handler = ContextHandler()
    # context_handler.load_session(context_sample)

    # pprint.pprint(options)

    # app = MakePlayblast(options=options)
    # app.execute()
