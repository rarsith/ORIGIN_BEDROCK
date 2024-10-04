# In Omniverse, you can use the ChangeProperty command to set the default value or timesample value of an Attribute. With the USD API, you can call Usd.Attribute.Set() to set a default value or timesample value.


from pxr import Usd, Sdf, Gf

def set_float_attribute(attr: Usd.Attribute, value: float) -> None:
    """
    See: https://openusd.org/release/api/class_usd_attribute.html
    Args:
        attr: The attribute to set.
        value: A floating point value, i.e. `3.141516`.
    """
    attr.Set(value)