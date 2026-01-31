from origin.dcc.extensions.blender.exporters.camera import BlenderCameraExporter
from origin.dcc.extensions.maya.publish.exporters.anim_rig import MayaAnimationRigExporter
from origin.dcc.extensions.maya.publish.exporters.camera import MayaCameraExporter
from origin.dcc.extensions.maya.publish.exporters.geometry import MayaGeometryExporter
from origin.dcc.extensions.maya.publish.exporters.maya_make_playblast import MayaMakePlayblast
from origin.dcc.extensions.maya.publish.exporters.template import MayaPlayblastTemplateExporter


class PublisherType:
    anim_rig = "anim_rig"
    camera = "camera"
    geometry = "geometry"
    playblast = "playblast"
    template = "template"
    fx_cache = "fx_cache"
    scene = "scene"
    nds = "hda"
    editorial = "editorial"
    render = "render"
    groom = "groom"
    comp = "comp"
    look = "look"
    usd_assembly = "usd_assembly"
    img_seq = "img_seq"
    turntable_camera = "turntable_camera"
    rig_module = "rig_module"
    animation_rig = "animation_rig"
    texture_set = "texture_set"
    texture = "texture"
    animation = "animation"
    shot_sculpt = "shot_sculpt"
    image = "image"
    reference = "reference"

DCC_PUBLISHERS = {
    PublisherType.anim_rig : {
        "maya": MayaAnimationRigExporter,
        "blender": "",
        "houdini": "",
        "gaffer": "",
        "nuke": "",
        "mari": "",
    },

    PublisherType.camera : {
        "maya": MayaCameraExporter,
        "blender": BlenderCameraExporter,
        "houdini": "",
        "gaffer": "",
        "nuke": "",
        "mari": "",
    },

    PublisherType.geometry : {
        "maya": MayaGeometryExporter,
        "blender": "",
        "houdini": "",
        "gaffer": "",
        "nuke": "",
        "mari": "",
        # Add other exporter here
    },

    PublisherType.playblast : {
        "maya": MayaMakePlayblast,
        "blender": "",
        "houdini": "",
        "gaffer": "",
        "nuke": "",
        "mari": "",
        # Add other exporter here
    },

    PublisherType.template : {
        "maya": MayaPlayblastTemplateExporter,
        "blender": "",
        "houdini": "",
        "gaffer": "",
        "nuke": "",
        "mari": "",
        # Add other exporter here
    }
}


def get_dcc_exporter(module_name: str, dcc: str):
    """
    Returns the exporter class for a given module and DCC.

    Args:
        module_name (str): e.g., "camera", "anim_rig"
        dcc (str): e.g., "maya", "blender"

    Returns:
        class or None
    """
    module_exporters = DCC_PUBLISHERS.get(module_name, {})
    return module_exporters.get(dcc)

