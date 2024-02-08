# Usd.Prim.GetAttribute() returns a Usd.Attribute, but this is not the value for the Attribute. You must call Usd.Attribute.Get() to perform the attribute value resolution resulting in a default value, timesample value or interpolated value for the Attribute.

def get_attribute_value(prim: Usd.Prim, attribute_name: str):
    """
    See: https://openusd.org/release/api/class_usd_attribute.html
    Args:
        prim: The prim owner of the attribute.
        attribute_name: The name of the attribute to retrieve.
    Return:
        The value of the attribute, see https://openusd.org/release/api/_usd__page__datatypes.html
        for the return types.
        For example, for `float3`, the return type will be `Gf.Vec3f`.
    """
    attr = prim.GetAttribute(attribute_name)
    return attr.Get()