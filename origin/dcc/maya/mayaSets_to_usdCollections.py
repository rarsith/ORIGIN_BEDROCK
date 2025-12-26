from pxr import Usd, UsdGeom, UsdUtils

    # Create a new USD stage
# stage = Usd.Stage.CreateNew("C:/tmp/mySphere04.usda")
usd_scene_path = "D:/__SANDBOX/__test_scenes/AlienHead/DATA_PACKAGE/geo/alien_head_usdSets_test_001.usdc"

stage = Usd.Stage.Open(usd_scene_path)

# Define root scope
geo = UsdGeom.Scope.Define(stage, "/main")
geo.GetPrim().SetMetadata("kind", "group")

# Define main xform
main = UsdGeom.Xform.Define(stage, "/main")
geo_xform = UsdGeom.Xform.Define(stage, "/main/geo")

# Apply CollectionAPI on /main/geo/
geo_xform_prim = geo_xform.GetPrim()
# Usd.CollectionAPI.Apply(geo_xform_prim, "myCubeSet")
# Usd.CollectionAPI.Apply(geo_xform_prim, "mySphereSet")
# Usd.CollectionAPI.Apply(geo_xform_prim, "myCylinderSet")

# Define sphere
sphere_xform = UsdGeom.Xform.Define(stage, "/main/geo/sphere_grp/pSphere1")
sphere_mesh = UsdGeom.Mesh.Define(stage, "/main/geo/sphere_grp/pSphere1/pSphereShape1")

# Define cube
cube_xform = UsdGeom.Xform.Define(stage, "/main/geo/cube_grp/pCube1")
cube_mesh = UsdGeom.Mesh.Define(stage, "/main/geo/cube_grp/pCube1/pCubeShape1")

# Define cylinder
cylinder_xform = UsdGeom.Xform.Define(stage, "/main/geo/cylinder_grp/pCylinder1")
cylinder_mesh = UsdGeom.Mesh.Define(stage, "/main/geo/cylinder_grp/pCylinder1/pCylinderShape1")


# Add cube transformations
# cube_xform.AddTranslateOp().Set((2.3597617, 0, 0))
# cube_xform.AddScaleOp().Set((1, 1.9202895, 1))

# Define collections
# initial_shading_group = Usd.CollectionAPI(geo_xform_prim, "initialShadingGroup")
# initial_shading_group.CreateIncludesRel().SetTargets([cube_mesh.GetPath(), sphere_mesh.GetPath(), cylinder_mesh.GetPath()])

my_cube_set = Usd.CollectionAPI(geo_xform_prim, "myCubeSet")
my_cube_set.CreateIncludesRel().SetTargets([cube_xform.GetPath()])

my_sphere_set = Usd.CollectionAPI(geo_xform_prim, "mySphereSet")
my_sphere_set.CreateIncludesRel().SetTargets([sphere_xform.GetPath()])

my_cylinder_set = Usd.CollectionAPI(geo_xform_prim, "myCylinderSet")
my_cylinder_set.CreateIncludesRel().SetTargets([cylinder_xform.GetPath()])

# Save USD file
stage.GetRootLayer().Save()

# Run script to generate the USD file
