"""
A Specialize is a composition arc that enables a prim to contain all of the scene description contained in the base prim it specializes.
The difference between Specialize and Inherit is that opinions authored on the prim with the specialize arc will always be stronger than the base prim.
This snippet shows how to add a Specialize arc to a prim.
A single prim can have multiple Specializes.
"""

from pxr import Usd

def add_specialize_to(base_prim: Usd.Prim, specializes: Usd.Specializes) -> bool:
    return specializes.AddSpecialize(base_prim.GetPath())

#############
# Full Usage
#############
from pxr import Sdf, UsdGeom

# Create an in-memory Stage with /World Xform prim as the default prim
stage: Usd.Stage = Usd.Stage.CreateInMemory()
default_prim: Usd.Prim = UsdGeom.Xform.Define(stage, Sdf.Path("/World")).GetPrim()
stage.SetDefaultPrim(default_prim)

prim: Usd.Prim = UsdGeom.Xform.Define(stage, default_prim.GetPath().AppendPath("prim")).GetPrim()
base: Usd.Prim = UsdGeom.Xform.Define(stage, default_prim.GetPath().AppendPath("base")).GetPrim()
specializes: Usd.Specializes = prim.GetSpecializes()

added_successfully = add_specialize_to(base, specializes)

usda = stage.GetRootLayer().ExportToString()
print(usda)

assert added_successfully