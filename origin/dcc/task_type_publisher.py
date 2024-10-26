import os
from origin.envars.Xorigin_envars import ContextHandler

from origin.dcc.task_type_publishers.rotomation_publish import RotomationPublish
from origin.dcc.task_type_publishers.animation_publish import AnimationPublish
from origin.dcc.task_type_publishers.camera_publish import CameraPublish
from origin.dcc.task_type_publishers.layout_publish import LayoutPublish
from origin.dcc.task_type_publishers.modeling_publish import ModelingPublish
from origin.dcc.task_type_publishers.rigging_publish import RiggingPublish
from origin.dcc.task_type_publishers.shot_sculpt_publish import ShotSculptPublish


def get_task_type_publish_class(task_type):
    publish_types = {
        "modeling": ModelingPublish,
        "rigging": RiggingPublish,
        "matchmove": CameraPublish,
        "layout": LayoutPublish,
        "rotomation": RotomationPublish,
        "animation": AnimationPublish,
        "shot_sculpt": ShotSculptPublish,
    }
    if task_type in list(publish_types.keys()):
        return publish_types[task_type]


class TaskTypePublisher:
    def __init__(self, publish_options):
        self.publishing_options = publish_options
        self.context_handler: ContextHandler = self.publishing_options["context_object"]
        self.task_type_publisher = get_task_type_publish_class(task_type=self.context_handler.task_type)

    def execute_publish(self):
        publish_results = self.task_type_publisher(publish_options=self.publishing_options).publish()
        return publish_results

