import maya.cmds as cmds

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
            
            
if __name__ == "__main__":
    material_sets = get_maya_sets_members("MAT")
    render_sets = get_maya_sets_members("RDR")
    