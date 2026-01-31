from origin.database.entities.operators import PublishTypes
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

    pub_types = {
        PublishTypes.GEOMETRY: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            MaterialSetsAssignments(),
            InjectDisplacement(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.CAMERA: [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.TURNTABLE_CAMERA: [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.TEXTURE_SET: [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.TEXTURE: [
            QcGhost(),
            Publish(context=context)
        ],

        PublishTypes.RIG_MODULE: [
            QcGhost(),
            Publish(context=context)
        ],

        PublishTypes.ANIMATION_RIG: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.GROOM: [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.LOOK: [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.FX_CACHE: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.SCENE: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.HDA: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.EDITORIAL: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            Publish(context=context)
        ],

        PublishTypes.RENDER: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.COMP: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.TEMPLATE: [
            EntryStackStream(context=context),
            QcGhost(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.USD_ASSEMBLY: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.IMG_SEQ: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.ANIMATION: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.IMAGE: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.REFERENCE: [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            AssetStackManager(),
            PreviewOptions(),
            Publish(context=context)
        ],

        PublishTypes.ASSET_STACK: [
            PreviewOptions(),
            Publish(context=context)
        ]
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

    typeso = get_publish_type(context=con, pub_type=PublishTypes.GEOMETRY)
    print(typeso)
