from origin.envars.origin_envars import ContextHandler
from origin.ui.publish.publisher.publisher import Publish
from origin.ui.publish.quality_checks.quality_checks import QcGhost
from origin.ui.publish.set_file_types.file_types import FileTypes
from origin.ui.publish.bundle_selector.assign_to_bundle import BundleSelector
from origin.ui.publish.output_reviewable_options.preview_render_options import PreviewOptions
from origin.ui.publish.material_assignment.material_assignment import MaterialSetsAssignments
from origin.ui.publish.inject_displacement.inject_displacement import InjectDisplacement
from origin.ui.publish.asset_stream_manager.asset_stream_manager_ui import EntryStackStream
from origin.ui.stack_management.asset_stack_manager_ui import LoaderMainUI
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
            FileTypes(),
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
