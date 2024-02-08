### This version creates just the Material prim and UsdPreviewSurface Shader.


from pxr import Sdf, UsdShade, Usd


stage: Usd.Stage = Usd.Stage.CreateInMemory()
root_layer: Sdf.Layer = stage.GetRootLayer()



mtl_path = Sdf.Path("/World/Looks/PreviewSurface")
mtl = UsdShade.Material.Define(stage, mtl_path)
shader = UsdShade.Shader.Define(stage, mtl_path.AppendPath("Shader"))
shader.CreateIdAttr("UsdPreviewSurface")
shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set([1.0, 0.0, 0.0])
shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.5)
shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)
mtl.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")


#### This version also creates UsdUVTexture Shader prim and connects it to the diffuse property of the UsdPreviewSurface.

from pxr import Sdf, UsdShade

mtl_path = Sdf.Path("/World/Looks/PreviewSurface")
mtl = UsdShade.Material.Define(stage, mtl_path)
shader = UsdShade.Shader.Define(stage, mtl_path.AppendPath("Shader"))
shader.CreateIdAttr("UsdPreviewSurface")
shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 0.0, 0.0))
shader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.5)
shader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

diffuse_tx = UsdShade.Shader.Define(stage,mtl_path.AppendPath("DiffuseColorTx"))
diffuse_tx.CreateIdAttr('UsdUVTexture')
diffuse_tx.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("C:/path/to/texture.png")
diffuse_tx.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuse_tx.ConnectableAPI(), 'rgb')
mtl.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")