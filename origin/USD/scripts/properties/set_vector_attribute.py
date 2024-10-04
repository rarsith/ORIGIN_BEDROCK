# In Omniverse, you can use the ChangeProperty command to set the default value or timesample value of an Attribute. With the USD API, you can call Usd.Attribute.Set() to set a default value or timesample value.


from pxr import Usd, Sdf, Gf

def set_vector_attribute(attr: Usd.Attribute, value: Gf.Vec3f) -> None:
    """
    Args:
        attr: The attribute to set.
        value: A floating point vector, i.e. `(1., 2., 3.)`.
    """
    attr.Set(value)