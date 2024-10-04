from pxr import Usd

def get_child_prim(parent_prim, child_name) -> Usd.Prim:
    child_prim: Usd.Prim = parent_prim.GetChild(child_name)
    return child_prim

#############
# Full Usage
#############

from pxr import Sdf, UsdGeom

# Create an in-memory Stage with /World Xform prim as the default prim
stage: Usd.Stage = Usd.Stage.CreateInMemory()
default_prim: Usd.Prim = UsdGeom.Xform.Define(stage, Sdf.Path("/World")).GetPrim()
stage.SetDefaultPrim(default_prim)

# Create a Cube prim
cube: Usd.Prim = UsdGeom.Cube.Define(stage, default_prim.GetPath().AppendPath("Box"))

# Get the child prim of the default prim with the name "Box"
child_prim = get_child_prim(default_prim, "Box")

# Print the full Stage
usda = stage.GetRootLayer().ExportToString()
print(usda)
# Print the path of the child prim you were looking for.
print(child_prim.GetPath())

# Verify the child and parent relationship
assert child_prim.GetParent() == default_prim
assert child_prim.GetPath() == cube.GetPath()


##################################################

from pxr import Usd, UsdGeom

def get_first_child_mesh(parent_prim: Usd.Prim) -> Usd.Prim:
    # Iterates only active, loaded, defined, non-abstract children
    for child_prim in parent_prim.GetChildren():
        if child_prim.IsA(UsdGeom.Mesh):
            return child_prim

def print_all_children_names(parent_prim: Usd.Prim):
    # Iterates over all children
    for child_prim in parent_prim.GetAllChildren():
        print(child_prim.GetName())