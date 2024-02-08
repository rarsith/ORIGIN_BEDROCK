"""
Show or Hide a Prim
See USD: Visibility. You can show or hide a prim by setting the visibility attribute to either inherited or invisible.

If the value is set to inherited, then prim will either be visible or invisible depending on the prim’s parent visibility value. If the value is set to invisible, then the prim and all children prims will be invisible.
"""

"""
You can use the USD API Usd.Prim.GetAttribute() to get an attribute of a prim and then use Usd.Attribute.Set() to change the value. The attribute name for visibility is visibility and you can set it to the value of inherited or invisible.
"""

from typing import Union
from pxr import Sdf, Usd, UsdGeom


def get_visibility_attribute(
    stage: Usd.Stage, prim_path: str
) -> Union[Usd.Attribute, None]:
    """Return the visibility attribute of a prim"""
    path = Sdf.Path(prim_path)
    prim = stage.GetPrimAtPath(path)
    if not prim.IsValid():
        return None
    visibility_attribute = prim.GetAttribute("visibility")
    return visibility_attribute


def hide_prim(stage: Usd.Stage, prim_path: str):
    """Hide a prim

    Args:
        stage (Usd.Stage, required): The USD Stage
        prim_path (str, required): The prim path of the prim to hide
    """
    visibility_attribute = get_visibility_attribute(stage, prim_path)
    if visibility_attribute is None:
        return
    visibility_attribute.Set("invisible")


def show_prim(stage: Usd.Stage, prim_path: str):
    """Show a prim

    Args:
        stage (Usd.Stage, required): The USD Stage
        prim_path (str, required): The prim path of the prim to show
    """
    visibility_attribute = get_visibility_attribute(stage, prim_path)
    if visibility_attribute is None:
        return
    visibility_attribute.Set("inherited")


#############
# Full Usage
#############
# Here you will show your code sample in context. Add any additional imports
# that you may need for your "Full Usage" code

# Create a simple in-memory stage with a Cube
stage: Usd.Stage = Usd.Stage.CreateInMemory()
default_prim_path = Sdf.Path("/World")
default_prim = UsdGeom.Xform.Define(stage, default_prim_path)
stage.SetDefaultPrim(default_prim.GetPrim())
cube_path = default_prim_path.AppendPath("Cube")
cube = UsdGeom.Cube.Define(stage, cube_path)

# The prim is initially visible. Assert so and then demonstrate how to toggle
# it off and on
assert get_visibility_attribute(stage, cube_path).Get() == "inherited"
hide_prim(stage, cube_path)
assert get_visibility_attribute(stage, cube_path).Get() == "invisible"
show_prim(stage, cube_path)
assert get_visibility_attribute(stage, cube_path).Get() == "inherited"

# Print the USDA out
usda = stage.GetRootLayer().ExportToString()
print(usda)