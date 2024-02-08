"""
USD itself does not currently have a notion of a user session associated with a current stage. This is handled by higher-level facilities in USD applications such as usdviewApi in USDView and omni.usd in Omniverse Kit.

"""

from pxr import Usd
import omni.usd

def get_current_stage() -> Usd.Stage:
    return omni.usd.get_context().get_stage()


#############
# Full Usage
#############
# Create a new USD stage through the UsdContext
success: bool = omni.usd.get_context().new_stage()

# Get the the current stage from the UsdContext
current_stage: Usd.Stage = get_current_stage()

# Check if the a new stage was created and a valid stage was returned
assert success
assert current_stage