from origin.envars.origin_envars import ContextHandler
from origin.ui.publish.publisher.publisher import Publish
from origin.ui.publish.quality_checks.quality_checks import QcGhost
from origin.ui.publish.set_file_types.file_types import FileTypes
from origin.ui.publish.output_reviewable_options.preview_render_options import PreviewOptions
from origin.ui.publish.material_assignment.material_assignment import MaterialSetsAssignments
from origin.ui.publish.inject_displacement.inject_displacement import InjectDisplacement
from origin.ui.publish.asset_stream_manager.asset_stream_manager_ui import EntryStackStream
from origin.ui.stack_management.asset_stack_manager_ui import AssetStackManager


def get_publish_type(context: ContextHandler, pub_type):
    context_handler = context

    pub_types = {
        "geometry": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            MaterialSetsAssignments(),
            InjectDisplacement(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "camera": [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "turntable_camera": [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            Publish(context=context)
        ],

        "texture_set": [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "texture": [
            QcGhost(),
            Publish(context=context)
        ],

        "rig_module": [
            QcGhost(),
            Publish(context=context)
        ],

        "animation_rig": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "groom": [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "look": [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "fx_cache": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "scene": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "hda": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "editorial": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            Publish(context=context)
        ],

        "render": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "comp": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "template": [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "usd_assembly": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "img_seq": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "animation": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "image": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        "reference": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],
    }

    if pub_type in list(pub_types.keys()):
        return pub_types[pub_type]
    else:
        return []
    #
    # initialized = []
    # if pub_type in list(pub_types.keys()):
    #     for p_type in pub_types[pub_type]:
    #         print(p_type)
    #         if hasattr(p_type, "context"):
    #             if context_handler:
    #                 cls = p_type(context=context_handler)
    #                 initialized.append(cls)
    #         else:
    #             cls = p_type()
    #             initialized.append(cls)
    #     return initialized
    # else:
    #     return []

if __name__ == "__main__":
    context_sample = {'show_name': 'The_Rock',
                                        'project_publishes': 'The_Rock__PUBLISHES',
                                        'project_work': 'The_Rock__WORK',
                                        'project_control': 'The_Rock__CONTROL',
                                        'origin_path_hierarchy': 'assets.chr',
                                        'entity_name': 'tafer',
                                        'entity_id': 'The_Rock.assets.chr.tafer',
                                        'entity_type': 'asset',
                                        'task_name': "modeling",
                                        'task_type': "modeling",
                                        'task_id': "The_Rock.assets.chr.tafer.modeling",
                                        'db_asset_id': 'The_Rock.assets.chr.tafer.geometry.tafer_main',
                                        'db_asset_stream_id': 'The_Rock.assets.chr.tafer.tafer_main',
                                        }

    con = ContextHandler()
    con.load_session(context_sample)

    typeso = get_publish_type(context=con, pub_type="geometry")
    print(typeso)
