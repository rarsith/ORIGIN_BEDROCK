import maya.cmds as cmds
from pxr import Sdf, Usd, UsdGeom, UsdUtils


def get_maya_sets_members(set_prefix="MAT"):
    full_prefix = set_prefix + "_"

    sets_with_members = {}

    all_sets = cmds.ls(type='objectSet') or []

    exclude = {'defaultLightSet', 'defaultObjectSet', 'initialShadingGroup'}

    custom_sets = [s for s in all_sets if s not in exclude and s.startswith(full_prefix)]

    for s in custom_sets:
        members = cmds.sets(s, query=True) or []
        full_path = cmds.ls(members, long=True) or []
        if not len(full_path) == 0:
            sets_with_members[s] = full_path
            
    return sets_with_members

    

def maya_sets_to_collections(usd_scene_target, root_prim, maya_sets: dict):

    stage = Usd.Stage.Open(usd_scene_path)

    geo_xform = UsdGeom.Scope.Define(stage, root_prim)

    geo_xform_prim = geo_xform.GetPrim()

    for m_set, m_set_members in maya_sets.items():
        if not m_set_members:
            continue
        
        included_targets = []
        for member in m_set_members:
            if not len(member) == 0:
                to_usd_path = member.replace("|", "/")
                included_targets.append(to_usd_path)
                
        Usd.CollectionAPI.Apply(geo_xform_prim, m_set)
        usd_colection = Usd.CollectionAPI(geo_xform_prim, m_set)
        usd_colection.CreateIncludesRel().SetTargets(included_targets)

    stage.GetRootLayer().Save()
    
if __name__ == "__main__":
    usd_scene_path = "D:/__SANDBOX/__test_scenes/AlienHead/DATA_PACKAGE/geo/alien_head_usdSets_test_006.usda"
    root_prim="/main/geo"
    material_sets = get_maya_sets_members("MAT")
    render_sets = get_maya_sets_members("RDR")
        
    maya_sets_to_collections(usd_scene_target=usd_scene_path, root_prim="/main/geo", maya_sets=material_sets)
    maya_sets_to_collections(usd_scene_target=usd_scene_path, root_prim="/main/geo", maya_sets=render_sets)
