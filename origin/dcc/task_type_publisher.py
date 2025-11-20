from origin.dcc.publishers.geometry_publish import GeometryPublish
from origin.dcc.publishers.animation_publish import AnimationPublish
from origin.dcc.publishers.camera_publish import CameraPublish
from origin.dcc.publishers.animationrig_publish import AnimationRigPublish
from origin.dcc.publishers.shot_sculpt_publish import ShotSculptPublish
from origin.dcc.publishers.template_publish import TemplatePublish
from origin.dcc.publishers.turntable_camera_publisher import TurntableCameraPublish


def get_publish_type_class(publish_type):
    publish_types = {
        # "fx_cache": FxCachePublish,
        # "scene": SceneFilePublish,
        # "hda": HoudiniDigitalAssetPublish,
        # "editorial": EditorialMediaPublish,
        # "render": RenderPublish,
        # "groom": GroomPublish,
        # "comp": CompPublish,
        # "look": LookPublish,
        "template": TemplatePublish,
        "geometry": GeometryPublish,
        # "usd_assembly": USDAssemblyPublish,
        # "img_seq": ImageSequencePublish,
        "camera": CameraPublish,
        "turntable_camera": TurntableCameraPublish,
        # "rig_module": RigModulePublish,
        "animation_rig": AnimationRigPublish,
        # "texture_set": TextureSetPublish,
        # "texture": TexturePublish,
        "animation": AnimationPublish,
        "shot_sculpt": ShotSculptPublish,
        # "image": ImagePublish,
        # "reference": ReferencePublish,
    }
    if publish_type in list(publish_types.keys()):
        return publish_types[publish_type]


class PublisherType:
    def __init__(self, publish_options):
        self.publishing_options = publish_options

        self.publisher_type = get_publish_type_class(publish_options["publish_type"])

    def execute_publish(self):
        publish_results = self.publisher_type(publish_options=self.publishing_options).publish()
        return publish_results
