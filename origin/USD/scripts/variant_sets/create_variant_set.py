"""
Create a Variant Set
Note

If this is your first time authoring a variant set, we recommend that you follow Authoring Variants USD tutorial first.

A Variant Set is a composition arc that serves as a sort of “switchable Reference” allowing you to provide alternate property opinions or entire prim hierarchies.
In this snippet, you’ll find how to create a Variant Set, add variants to the new Variant Set and author opinions for each variant.
"""

from pxr import Usd

def create_variant_set(prim: Usd.Prim, variant_set_name: str, variants: list) -> Usd.VariantSet:
    variant_set = prim.GetVariantSets().AddVariantSet(variant_set_name)
    for variant in variants:
        variant_set.AddVariant(variant)
    return variant_set

#############
# Full Usage
#############
from pxr import Sdf, UsdGeom

# Create an in-memory Stage with /World Xform prim as the default prim
stage: Usd.Stage = Usd.Stage.CreateInMemory()
default_prim: Usd.Prim = UsdGeom.Xform.Define(stage, Sdf.Path("/World")).GetPrim()
stage.SetDefaultPrim(default_prim)

# Create the variant set and add your variants to it.
variants = ["red", "blue", "green"]
shading_varset: Usd.VariantSet = create_variant_set(default_prim, "shading", variants)

usda = stage.GetRootLayer().ExportToString()
print(usda)

assert default_prim.GetVariantSets().HasVariantSet("shading")