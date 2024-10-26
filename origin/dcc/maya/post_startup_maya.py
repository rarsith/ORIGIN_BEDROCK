import os
from origin.dcc.env_setup import env_setup
import maya.cmds as cmds

env_setup()

from origin.o_database.entities.Xoperators import CollectionOperators, Asset

        
def get_entity_definition():
    entity_type = os.getenv('ENTITY_TYPE')
    show_name = os.getenv('SHOW_NAME')
    entity_id = os.getenv('ENTITY_ID')

    if entity_type != "group":
        db_ops = CollectionOperators(show_name)
        entity_doc = db_ops.entity_document(entity_id)
        if entity_doc:
            entity_received = Asset(**entity_doc)
            return entity_received.definition
        else:
            return None
    else:
        return None


def set_timeline_range(start_frame, end_frame):
    cmds.playbackOptions(min=start_frame, max=end_frame)
    cmds.playbackOptions(animationStartTime=start_frame, animationEndTime=end_frame)


def set_render_resolution(width, height):
    cmds.setAttr('defaultResolution.width', width)
    cmds.setAttr('defaultResolution.height', height)


def load_renderer():
    cmds.loadPlugin("mtoa", quiet=True)
    cmds.setAttr('defaultRenderGlobals.currentRenderer', 'arnold', type='string')

    if not cmds.objExists('defaultArnoldRenderOptions'):
        cmds.createNode('aiOptions', name='defaultArnoldRenderOptions')

    cmds.select(cl=True)


def set_motion_blur_settings(enable_motion_blur=1, motion_blur_by_frame=0.5, shutter_open=-0.25, shutter_close=0.25):
    load_renderer()
    cmds.setAttr('defaultArnoldRenderOptions.motion_blur_enable', enable_motion_blur)
    cmds.setAttr('defaultArnoldRenderOptions.motion_frames', motion_blur_by_frame)
    cmds.setAttr('defaultArnoldRenderOptions.range_type', 3)
    cmds.setAttr('defaultArnoldRenderOptions.motion_start', shutter_open)
    cmds.setAttr('defaultArnoldRenderOptions.motion_end', shutter_close)
    cmds.setAttr("defaultArnoldRenderOptions.AASamples", 3)


def set_origin_maya():
    entity_definition = get_entity_definition()

    set_timeline_range(start_frame=int(entity_definition["full_range_in"]),
                       end_frame=int(entity_definition["full_range_out"]))

    set_render_resolution(width=int(entity_definition["res_x"]),
                          height=int(entity_definition["res_y"]))

    set_motion_blur_settings(shutter_open=float(entity_definition["motion_blur_low"]),
                             shutter_close=float(entity_definition["motion_blur_high"]))
