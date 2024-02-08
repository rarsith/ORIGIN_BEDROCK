from pxr import Usd, UsdGeom, UsdShade

path_knife= r'E:\Local_projects\PycharmProjects\ORIGIN_ENERVO\tests\usd_tests\knife.usda'
path_materials = r'E:\Local_projects\PycharmProjects\ORIGIN_ENERVO\tests\usd_tests\materials.usda'
path_third_scene = r'E:\Local_projects\PycharmProjects\ORIGIN_ENERVO\tests\usd_tests\third_scene.usda'

# Create the knife geometry USD
knifeStage = Usd.Stage.CreateNew(path_knife)
knife = UsdGeom.Xform.Define(knifeStage, "/Knife")
materialPath = "/Materials/knifeMaterial"
# UsdShade.MaterialBindingAPI(knife.GetPrim()).Bind(materialPath)
knifeStage.GetRootLayer().Save()

# Create the materials USD
materialsStage = Usd.Stage.CreateNew(path_materials)
material = UsdShade.Material.Define(materialsStage, "/Materials/knifeMaterial")
# Define shader networks and parameters here
materialsStage.GetRootLayer().Save()

# Create the third USD scene
thirdStage = Usd.Stage.CreateNew(path_third_scene)

# Reference the knife geometry USD
knifeRef = knifeStage.GetRootLayer().defaultPrim
thirdStage.GetRootLayer().subLayerPaths.append(path_knife)
thirdStage.DefinePrim("/KnifeRef", "Xform")
thirdStage.GetPrimAtPath("/KnifeRef").GetReferences().AddReference(knifeRef)

# Reference the materials USD
materialsRef = materialsStage.GetRootLayer().defaultPrim
thirdStage.GetRootLayer().subLayerPaths.append(path_materials)
thirdStage.GetPrimAtPath("/KnifeRef").GetReferences().AddReference(materialsRef)

# Assign the material to the knife geometry
knifePrim = thirdStage.GetPrimAtPath("/KnifeRef/Knife")
if knifePrim:
    materialPath = "/KnifeRef/Materials/knifeMaterial"
    UsdShade.MaterialBindingAPI(knifePrim).Bind(materialPath)

thirdStage.GetRootLayer().Save()
