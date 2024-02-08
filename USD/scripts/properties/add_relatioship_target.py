from pxr import Usd, UsdGeom

# If you just want to add a target to an existing Relationship, you can use Usd.Relationship.AddTarget() to add a Path to the Relationship’s targets list.

# For example, adding a proxy prim target on an Imageable
proxy_prim_rel: Usd.Relationship = UsdGeom.Imageable(myprim).GetProxyPrimRel()
proxy_prim_rel.AddTarget("/World/MyProxy")