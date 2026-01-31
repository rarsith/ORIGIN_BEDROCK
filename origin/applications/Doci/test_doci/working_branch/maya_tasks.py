import sys
import os
import maya.standalone
import maya.cmds as cmds


def load_additional_plugins():
    plugins = ["AbcImport", "AbcExport", "objExport"]
    for plugin in plugins:
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            print(f"Loading plugin: {plugin}")
            cmds.loadPlugin(plugin)
        else:
            print(f"'{plugin}' is already loaded.")


def start_maya_standalone():
    maya.standalone.initialize(name="python")

    # cmds.setAttr("hardwareRenderingGlobals.renderingAPI", 4)  # OpenGL Core
    # cmds.setAttr("hardwareRenderingGlobals.rendererName", "vp2Renderer", type="string")

    load_additional_plugins()


def save_debug_scene(path):
    path = os.path.abspath(path)

    cmds.file(rename=path)
    cmds.file(save=True, type="mayaAscii")

    print(f"DOCI_RESULT::{path}")


def ensure_maya_light():
    # if not cmds.ls(type=['directionalLight', 'pointLight', 'spotLight', 'areaLight']):
    extra_light = cmds.directionalLight()
    cmds.setAttr(extra_light + ".intensity", 7)


def export_geo(scene, out_dir):
    cmds.file(scene, open=True, force=True)

    root_group = "main|geo"

    if not cmds.objExists(root_group):
        raise RuntimeError("f{root_group} group not found")

    os.makedirs(out_dir, exist_ok=True)
    abc_path = os.path.join(out_dir, "geometry.abc")


    cmds.select(root_group, hierarchy=True)
    cmds.AbcExport(j=f"-root {root_group} -file {abc_path}")

    print(f"DOCI_RESULT::{abc_path}")


def setup_playblast_options(camera_name):
    # window = cmds.window(visible=False)
    # cmds.paneLayout()
    panel = cmds.modelPanel(barLayout=True)
    #
    # cmds.lookThru(panel, camera_name)

    cmds.modelPanel(panel, e=True, camera=camera_name)

    cmds.modelEditor(panel, e=True,
                     rendererName='vp2Renderer',
                     polymeshes=True,
                     lights=True,
                     displayLights="all",
                     useDefaultLighting=False,
                     nurbsCurves=False,
                     grid=False,
                     cameras=False,
                     joints=False,
                     locators=False,
                     hud=False,
                     displayAppearance="smoothShaded",
                     displayTextures=True
                     )

    # SSAO is optional — keep if you want
    cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)

    cmds.setFocus(panel)
    return panel


def setup_camera():
    camera_node = "camera_sc:camera"
    camera_node_shape = cmds.listRelatives(camera_node, shapes=True)[0]

    cams = cmds.ls(type='camera')
    states = {}
    for cam in cams:
        states[cam] = cmds.getAttr(cam + '.renderable')
        cmds.setAttr(cam + '.renderable', 0)

    cmds.setAttr(camera_node_shape + '.renderable', 1)
    cmds.viewFit(camera_node_shape, all=True)


def open_camera_scene(cam_path):
    if cam_path is not None:
        cmds.file(cam_path,
                  i=True,
                  typ="Alembic",
                  ignoreVersion=True,
                  ra=True,
                  mergeNamespacesOnClash=False,
                  namespace="camera_sc",
                  pr=True,
                  importTimeRange="combine",
                  )
        setup_camera()
        print("camera opened and ready to use")


def playblast_from_cache(turntable_scene, abc_path, camera_path, out_dir):
    cmds.file(turntable_scene, open=True, force=True)

    if not os.path.exists(abc_path):
        raise RuntimeError("Alembic not found")

    # Import Alembic
    cmds.AbcImport(abc_path, mode="import")

    open_camera_scene(cam_path=camera_path)

    os.makedirs(out_dir, exist_ok=True)

    ensure_maya_light()
    setup_playblast_options(camera_name="camera_sc:camera")

    cmds.playblast(
        format="image",
        filename=os.path.join(out_dir, "playblast"),
        sequenceTime=False,
        clearCache=True,
        viewer=0,
        showOrnaments=False,
        offScreen=True,
        percent=100,
        compression="png",
        framePadding=4
    )
    save_debug_scene(os.path.join(out_dir, "playblast.ma"))

if __name__ == "__main__":
    start_maya_standalone()

    task = sys.argv[1]
    args = sys.argv[2:]

    if task == "export_geo":
        export_geo(*args)
    elif task == "playblast_from_cache":
        playblast_from_cache(*args)
    else:
        raise RuntimeError(f"Unknown task: {task}")
