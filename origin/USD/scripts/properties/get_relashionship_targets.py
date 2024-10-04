"""
If you need to get the targets of a Relationship, you can use Usd.Relationship.GetForwardedTargets(). This method will give you the final composed targets for the Relationship and also take into account the relationship forwarding.
That is, if the Relationship itself targets another Relationship, we want to get the final targets in a potential chain of Relationships.
Learn more about relationship forwarding.
"""

from pxr import Usd, UsdGeom

# For example, getting the proxy prim on an Imageable
proxy_prim_rel: Usd.Relationship = UsdGeom.Imageable(myprim).GetProxyPrimRel()
proxyPrimTargets = proxy_prim_rel.GetForwardedTargets()