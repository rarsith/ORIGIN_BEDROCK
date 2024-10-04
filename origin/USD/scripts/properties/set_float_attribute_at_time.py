from pxr import Usd, Sdf, Gf

def set_float_attribute_at_time(attr: Usd.Attribute, value: float, time_value: float) -> None:
    """
    See: https://openusd.org/release/api/class_usd_attribute.html
    Args:
        attr: The attribute to set.
        value: A floating point value, i.e. `3.141516`.
        time_value: Set a timesample at a particular time.
    """
    attr.Set(value, time_value)