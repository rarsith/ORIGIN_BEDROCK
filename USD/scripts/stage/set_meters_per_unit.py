"""
You can set the metersPerUnit metadata on the stage using UsdGeom.SetStageMetersPerUnit. Convenience shortcuts for units are scoped in UsdGeom.LinearUnits (e.g. UsdGeom.LinearUnits.meters is 1.0 metersPerUnit)

Note

Fallback stage linear units are centimeters (0.01).

Warning

Existing objects will not be automatically scaled to adapt to the stage linear units. Learn more about stage linear units.


You can set the metersPerUnit metadata on the stage using UsdGeom.SetStageMetersPerUnit to define the linear units of the stage. Convenience shortcuts for units are scoped in UsdGeom.LinearUnits (e.g. UsdGeom.LinearUnits.meters is 1.0 metersPerUnit)

"""

from pxr import Usd, UsdGeom


def set_meters_per_unit(stage: Usd.Stage, unit: UsdGeom.LinearUnits = UsdGeom.LinearUnits.centimeters):
    UsdGeom.SetStageMetersPerUnit(stage, unit) # Any double-precision float can be used for metersPerUnit.


#############
# Full Usage
#############
unit: UsdGeom.LinearUnits = UsdGeom.LinearUnits.centimeters
stage: Usd.Stage = Usd.Stage.CreateInMemory()
set_meters_per_unit(stage, unit)

usda = stage.GetRootLayer().ExportToString()
print(usda)

# Check that the expected meterPerUnit were set
assert UsdGeom.GetStageMetersPerUnit(stage) == unit
