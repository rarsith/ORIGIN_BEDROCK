import maya.cmds as cmds

def create_material_sets():
    # Step 1: Get material-to-mesh mapping
    material_map = get_material_assignments()

    # Step 2: Create the master set if it doesn't exist
    master_set = "MAT_sets"
    if not cmds.objExists(master_set):
        master_set = cmds.sets(name=master_set, empty=True)

    for material, meshes in material_map.items():
        # Sanitize material name for use in set name
        set_name = f"MAT_{material}"

        # Create or clear the set
        if cmds.objExists(set_name):
            cmds.sets(clear=set_name)
        else:
            set_name = cmds.sets(name=set_name, empty=True)

        # Add meshes to the material set
        if meshes:
            cmds.sets(meshes, add=set_name)

        # Add the material set to the master set
        cmds.sets(set_name, add=master_set)

def get_material_assignments():
    """Returns a dictionary with materials as keys and lists of assigned meshes as values."""
    material_to_meshes = {}

    # Get all shading engines
    shading_engines = cmds.ls(type='shadingEngine')

    for se in shading_engines:
        # Get the surface shader connected to the shading engine
        materials = cmds.ls(cmds.listConnections(se + ".surfaceShader"), materials=True)
        if not materials:
            continue

        material = materials[0]

        # Get all meshes assigned to this shading engine
        members = cmds.sets(se, query=True) or []
        meshes = set()

        for member in members:
            shapes = []
            if cmds.objectType(member) == "transform":
                shapes = cmds.listRelatives(member, shapes=True, fullPath=True) or []
            elif cmds.objectType(member) in ["mesh", "nurbsSurface"]:
                shapes = [member]
            else:
                continue

            for shape in shapes:
                transform = cmds.listRelatives(shape, parent=True, fullPath=True)
                if transform:
                    meshes.add(transform[0])

        material_to_meshes[material] = list(meshes)

    return material_to_meshes

# Run it
create_material_sets()
