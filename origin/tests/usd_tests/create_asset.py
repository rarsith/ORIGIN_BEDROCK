from pxr import Usd, UsdGeom

asset_name = "Knife"


stage = Usd.Stage.CreateNew(asset_name+".usda")
knife = UsdGeom.Xform.Define(stage, "/Knife")
# Assuming you have a UsdShade.Material named "knifeMaterial"
# materialPath = "/Materials/knifeMaterial"
# UsdShade.MaterialBindingAPI(knife.GetPrim()).Bind(materialPath)
stage.GetRootLayer().Save()