import sys
import os
import maya.standalone
import maya.cmds as cmds


def load_additional_plugins():
    import maya.cmds as cmds

    plugins = ["AbcImport", "AbcExport", "objExport"]
    for plugin in plugins:
        if not cmds.pluginInfo(plugin, query=True, loaded=True):
            print(f"Loading plugin: {plugin}")
            cmds.loadPlugin(plugin)
        else:
            print(f"'{plugin}' is already loaded.")


def publish_geometry(scene_path, output_dir):

    maya.standalone.initialize(name="python")

    load_additional_plugins()

    cmds.file(scene_path, open=True, force=True)

    geo_grp = "main|geo"
    if not cmds.objExists(geo_grp):
        raise RuntimeError("GEO group not found")

    cmds.select(geo_grp, hierarchy=True)

    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "geometry_publish.abc")

    cmds.AbcExport(
        j=f"-root {geo_grp} -file {out_file}"
    )

    print(f"[MAYA] Geometry published to {out_file}")

if __name__ == "__main__":
    scene = sys.argv[1]
    output = sys.argv[2]
    publish_geometry(scene, output)