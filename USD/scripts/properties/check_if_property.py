"""
Certain functions may return a Usd.Property object, but the Property may not exist due to an incorrect path or because of changes on the Stage. You can use Usd.Object.IsValid() to check if the Property is valid or exists.

Note

Remember, that Properties consist of Usd.Attribute and Usd.Relationship. You can perform this check on both types of objects.

"""

from pxr import Usd

pts_attr: Usd.Attribute = mesh_prim.GetAttribute("points")
if pts_attr.IsValid():
    print("Attribute exists!")


# Alternatively, Usd.Object overrides the boolean operator so you can check with a simple boolean expression.

from pxr import Usd

pts_attr: Usd.Attribute = mesh_prim.GetAttribute("points")
if pts_attr:
    print("Attribute exists!")