"""
Find All the Prims of a Given Type
If you want to find all of the prims of a certain type, you can Traverse the stage and use Usd.Prim.IsA() to compare the type of every prim on the stage with the type you are looking for.
"""

from typing import List, Type
from pxr import Usd, UsdGeom


def find_prims_by_type(stage: Usd.Stage, prim_type: Type[Usd.Typed]) -> List[Usd.Prim]:
    found_prims = [x for x in stage.Traverse() if x.IsA(prim_type)]
    return found_prims


##############
# Full Usage
##############

from pxr import UsdGeom, Sdf

# Create an in-memory Stage with /World Xform prim as the default prim
stage: Usd.Stage = Usd.Stage.CreateInMemory()
default_prim = UsdGeom.Xform.Define(stage, Sdf.Path("/World"))
stage.SetDefaultPrim(default_prim.GetPrim())

# Create some shape prims
UsdGeom.Xform.Define(stage, "/World/Group")
UsdGeom.Mesh.Define(stage, "/World/Foo")
UsdGeom.Mesh.Define(stage, "/World/Group/Bar")
UsdGeom.Sphere.Define(stage, "/World/Group/Baz")

# find the prims with of type UsdGeom.Mesh
prims: List[Usd.Prim] = find_prims_by_type(stage, UsdGeom.Mesh)

# Print the mesh prims you found
print(prims)

# Check the number of prims found and whether the found data is correct.
assert len(prims) == 2
prim: Usd.Prim
for prim in prims:
    assert isinstance(prim, Usd.Prim)
    assert prim.GetTypeName() == "Mesh"