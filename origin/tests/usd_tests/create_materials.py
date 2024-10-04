from pxr import Usd, UsdShade

stage = Usd.Stage.CreateNew("materials.usda")
material = UsdShade.Material.Define(stage, "/Materials/knifeMaterial")
# Define shader networks and parameters here
stage.GetRootLayer().Save()