"""
It’s best practice to set the defaultPrim metadata on a Stage if the Stage’s root layer may be used as a Reference or Payload.
Otherwise, consumers of your Stage are forced to provide a target prim when they create a Reference or Payload arc.
Even though the Usd.Stage.SetDefaultPrim() accepts any Usd.Prim, the default prim must be a top-level prim on the Stage.
"""

from pxr import Usd

def set_default_prim(stage: Usd.Stage, prim: Usd.Prim):
    stage.SetDefaultPrim(prim)


#############
# Full Usage
#############

from pxr import UsdGeom, Sdf

# Create new USD stage for this sample
stage: Usd.Stage = Usd.Stage.CreateInMemory()

# Create an xform which should be set as the default prim
default_prim: Usd.Prim = UsdGeom.Xform.Define(stage, Sdf.Path("/World")).GetPrim()

# Make the xform the default prim
set_default_prim(stage, default_prim)

usda = stage.GetRootLayer().ExportToString()
print(usda)

# Check that the expected default prim was set
assert stage.GetDefaultPrim() == default_prim