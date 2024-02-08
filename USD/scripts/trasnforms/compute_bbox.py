"""
Compute the Bounding Box for a Prim
USD includes functions for computing the bounding box for a prim and all of its descendants. Bounding boxes are represented by the minimum point and maximum point of the bounding box.
The two points form a diagonal across the interior of the box.
These code samples show how to compute and retrieve a prim’s bounding box in world space.
"""

from pxr import Usd, UsdGeom, Gf

def compute_bbox(prim: Usd.Prim) -> Gf.Range3d:
    """
    Compute Bounding Box using ComputeWorldBound at UsdGeom.Imageable
    See https://openusd.org/release/api/class_usd_geom_imageable.html

    Args:
        prim: A prim to compute the bounding box.
    Returns:
        A range (i.e. bounding box), see more at: https://openusd.org/release/api/class_gf_range3d.html
    """
    imageable = UsdGeom.Imageable(prim)
    time = Usd.TimeCode.Default() # The time at which we compute the bounding box
    bound = imageable.ComputeWorldBound(time, UsdGeom.Tokens.default_)
    bound_range = bound.ComputeAlignedBox()
    return bound_range


def compute_bbox_with_cache(cache: UsdGeom.BBoxCache, prim: Usd.Prim) -> Gf.Range3d:
    """
    Compute Bounding Box using ComputeWorldBound at UsdGeom.BBoxCache. More efficient if used multiple times.
    See https://openusd.org/release/api/class_usd_geom_b_box_cache.html

    Args:
        cache: A cached, i.e. `UsdGeom.BBoxCache(Usd.TimeCode.Default(), ['default', 'render'])`
        prim: A prim to compute the bounding box.
    Returns:
        A range (i.e. bounding box), see more at: https://openusd.org/release/api/class_gf_range3d.html

    """
    bound = cache.ComputeWorldBound(prim)
    bound_range = bound.ComputeAlignedBox()
    return bound_range