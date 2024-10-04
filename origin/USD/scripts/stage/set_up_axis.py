"""
Set the Stage Up Axis
You can set the upAxis metadata on the stage using UsdGeom.SetStageUpAxis to define which world axis points up. The tokens for the different axes are scoped in UsdGeom.Tokens.

Note

Fallback stage upAxis is Y.

Warning

Existing objects will not be automatically rotated to adapt to the stage upAxis. Learn more about stage up axis.
"""

from pxr import Usd, UsdGeom

def set_up_axis(stage: Usd.Stage, axis: UsdGeom.Tokens):
    UsdGeom.SetStageUpAxis(stage, axis)


#############
# Full Usage
#############
axis: UsdGeom.Tokens = UsdGeom.Tokens.z
stage: Usd.Stage = Usd.Stage.CreateInMemory()
set_up_axis(stage, axis)

usda = stage.GetRootLayer().ExportToString()
print(usda)

# Check that the expected upAxis was set
assert UsdGeom.GetStageUpAxis(stage) == axis