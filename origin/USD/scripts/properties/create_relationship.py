# A Relationship is a type of Usd.Property that points to other Prims, Attributes or Relationships. The Relationship targets are represented by a list of Paths. This code sample shows how to create a Relationship and set some initial targets.

from pxr import Usd

prim: Usd.Prim = stage.GetPrimAtPath("/World/MyPrim")
custom_relationship: Usd.Relationship = prim.CreateRelationship("myCustomRelationship")
# You can also use Usd.Relationship.AddTarget() to add targets to an existing Relationship.
custom_relationship.SetTargets(["/World/TargetA", "/World/TargetB"])