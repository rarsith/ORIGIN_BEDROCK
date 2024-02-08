from pxr import Gf, Kind, Sdf, Usd, UsdGeom, UsdShade
#Making a Model
stage = Usd.Stage.CreateNew("simpleShading.usda")
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

modelRoot = UsdGeom.Xform.Define(stage, "/TexModel")
Usd.ModelAPI(modelRoot).SetKind(Kind.Tokens.component)

#Adding a Mesh “Billboard”
billboard = UsdGeom.Mesh.Define(stage, "/TexModel/card")
billboard.CreatePointsAttr([(-430, -145, 0), (430, -145, 0), (430, 145, 0), (-430, 145, 0)])
billboard.CreateFaceVertexCountsAttr([4])
billboard.CreateFaceVertexIndicesAttr([0,1,2,3])
billboard.CreateExtentAttr([(-430, -145, 0), (430, 145, 0)])
texCoords = UsdGeom.PrimvarsAPI(billboard).CreatePrimvar("st",
                                    Sdf.ValueTypeNames.TexCoord2fArray,
                                    UsdGeom.Tokens.varying)
texCoords.Set([(0, 0), (1, 0), (1,1), (0, 1)])


stage.Save()

#Make a Material
material = UsdShade.Material.Define(stage, '/TexModel/boardMat')

#Add a UsdPreviewSurface
pbrShader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/PBRShader')
pbrShader.CreateIdAttr("UsdPreviewSurface")
pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")

#Add Texturing
stReader = UsdShade.Shader.Define(stage, '/TexModel/boardMat/stReader')
stReader.CreateIdAttr('UsdPrimvarReader_float2')

diffuseTextureSampler = UsdShade.Shader.Define(stage,'/TexModel/boardMat/diffuseTexture')
diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("USDLogoLrg.png")
diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(), 'result')
diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(diffuseTextureSampler.ConnectableAPI(), 'rgb')

stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
stInput.Set('st')

stReader.CreateInput('varname',Sdf.ValueTypeNames.Token).ConnectToSource(stInput)

billboard.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
UsdShade.MaterialBindingAPI(billboard).Bind(material)

stage.Save()