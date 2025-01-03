import maya.standalone
import maya.cmds as cmds

# Initialize Maya in standalone mode
maya.standalone.initialize(name='python')


def ensure_alembic_plugin():
    plugin_name = "AbcImport"
    if not cmds.pluginInfo(plugin_name, query=True, loaded=True):
        print(f"Loading Alembic plugin: {plugin_name}")
        cmds.loadPlugin(plugin_name)
    else:
        print(f"Alembic plugin '{plugin_name}' is already loaded.")


ensure_alembic_plugin()


def import_scenes_and_playblast(geometry_scene, camera_scene, template_scene, playblast_output_path):
    panel = "modelPanel4"

    if not cmds.modelPanel(panel, exists=True):
        cmds.modelPanel("modelPanel4")

    cmds.modelEditor(panel, e=True, rendererName='vp2Renderer')

    cmds.modelEditor(panel, e=True, lights=False)  # No lights
    cmds.modelEditor(panel, e=True, nurbsCurves=False)  # No NURBS curves
    cmds.modelEditor(panel, e=True, grid=False)  # No grid
    cmds.modelEditor(panel, e=True, cameras=False)  # No cameras
    cmds.modelEditor(panel, e=True, joints=False)  # No joints
    cmds.modelEditor(panel, e=True, locators=False)  # No locators
    cmds.modelEditor(panel, e=True, hud=False)  # No HUD
    cmds.modelEditor(panel, e=True, polymeshes=True)

    cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
    cmds.setAttr("hardwareRenderingGlobals.ssaoAmount", 1.0)  # Adjust strength
    cmds.setAttr("hardwareRenderingGlobals.ssaoRadius", 16.0)  # Adjust radius

    cmds.modelEditor('modelPanel4', e=True, displayLights="all")

    cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)
    cmds.setAttr("hardwareRenderingGlobals.multiSampleCount", 8)  # 8x AA

    cmds.file(template_scene, open=True, force=True)

    cmds.file(geometry_scene,
              i=True,
              typ="Alembic",
              ignoreVersion=True,
              ra=True,
              mergeNamespacesOnClash=False,
              namespace="geometry_sc",
              pr=True,
              importTimeRange="combine",
              )

    cmds.file(camera_scene,
              i=True,
              typ="Alembic",
              ignoreVersion=True,
              ra=True,
              mergeNamespacesOnClash=False,
              namespace="camera_sc",
              pr=True,
              importTimeRange="combine",
              )

    camera_node = "camera_sc:cam1"  # Adjust based on the imported camera's name
    camera_node_shape = cmds.listRelatives(camera_node, shapes=True)[0]

    cams = cmds.ls(type='camera')
    states = {}
    for cam in cams:
        states[cam] = cmds.getAttr(cam + '.renderable')
        cmds.setAttr(cam + '.rnd', 0)

    # Change the solo cam to renderable
    cmds.setAttr(camera_node_shape + '.renderable', 1)

    parent_cam_to_locator = cmds.parentConstraint("tt_grp", "geometry_sc:geo", maintainOffset=1)

    cmds.playblast(
        startTime=1001,
        endTime=1100,  # Adjust based on your scene's frame range
        format="image",  # Or "qt" or "image"
        filename=playblast_output_path,
        width=1920,  # Adjust resolution as needed
        height=1080,
        percent=100,
        offScreen=True,  # To run without a GUI
        viewer=False,  # Don't display the playblast window
        compression="jpg",
        sequenceTime=0,
        clearCache=1,
        fp=4,
        quality=100,
        forceOverwrite=True
    )
    print(f"Playblast saved to {playblast_output_path}")


# Example usage
import_scenes_and_playblast(
    geometry_scene="E:/__ORIGIN_PROJECTS__/projects/The_Rock/assets/chr/tafer/modeling/publishes/data/geometry__tafer__tafer_dragonBody/chr__tafer__tafer_dragonBody__v0001/alembic/chr__tafer__tafer_dragonBody__v0001.abc",
    camera_scene="E:/__ORIGIN_PROJECTS__/projects/The_Rock/assets\chr/tafer/modeling/publishes/data/turntable_camera__tafer__tafer_dragonBody/chr__tafer__tafer_dragonBody__v0001/alembic/chr__tafer__tafer_dragonBody__v0001.abc",
    template_scene="E:/__ORIGIN_PROJECTS__/projects/The_Rock/assets/chr/tafer/modeling/work_rarsith/scene_files/temaplte_scene.mb",
    playblast_output_path="E:/__ORIGIN_PROJECTS__/projects/The_Rock/assets/chr/tafer/modeling/work_rarsith/tafer_DragonBody.jpg"
)
