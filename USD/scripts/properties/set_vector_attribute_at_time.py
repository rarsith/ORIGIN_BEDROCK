from pxr import Usd, Sdf, Gf

def set_vector_attribute_at_time(attr: Usd.Attribute, value: Gf.Vec3f, time_value: float) -> None:
    """
    Args:
        attr: The attribute to set.
        value: A floating point vector, i.e. `(1., 2., 3.)`.
        time_value: Set a timesample at a particular time.
    """
    attr.Set(value, time_value)