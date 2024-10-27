from origin.envars.origin_envars import ContextHandler
from origin.ui.publish.publisher.publisher import Publish
from origin.ui.publish.quality_checks.quality_checks import QcGhost
from origin.ui.publish.set_file_types.file_types import FileTypes
from origin.ui.publish.bundle_selector.assign_to_bundle import BundleSelector
from origin.ui.publish.output_reviewable_options.preview_render_options import PreviewOptions
from origin.ui.publish.material_assignment.material_assignment import MaterialSetsAssignments
from origin.ui.publish.inject_displacement.inject_displacement import InjectDisplacement
from origin.ui.publish.asset_stream_manager.asset_stream_manager_ui import EntryStackStream


def get_publish_type(context: ContextHandler):
    context_handler = context

    task_types = {
        "modeling": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            MaterialSetsAssignments(),
            InjectDisplacement(),
            BundleSelector(),
            PreviewOptions(),
            Publish(context=context)
        ],
        "texturing": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            Publish(context=context)
        ],

        "rigging": [
            EntryStackStream(context=context),
            QcGhost(),
            FileTypes(),
            BundleSelector(),
            PreviewOptions(),
            Publish(context=context)
        ],
    }

    if context_handler.task_type in list(task_types.keys()):
        return task_types[context_handler.task_type]
    else:
        return []
