from pxr import Usd

# stage.GetRootLayer().Save()
variant_a = "D:/PERSONAL_WORK_AREA/PROJECTS/ZMEU_CUBE/dataops/incoming/20Aug2024/240820_Plates_test/geometries/rock_aa/variants/varA.usdc"
variant_b = "D:/PERSONAL_WORK_AREA/PROJECTS/ZMEU_CUBE/dataops/incoming/20Aug2024/240820_Plates_test/geometries/rock_aa/variants/varB.usdc"
variant_c = "D:/PERSONAL_WORK_AREA/PROJECTS/ZMEU_CUBE/dataops/incoming/20Aug2024/240820_Plates_test/geometries/rock_aa/variants/varC.usdc"

variant_d = "D:/PERSONAL_WORK_AREA/PROJECTS/ZMEU_CUBE/dataops/incoming/20Aug2024/240820_Plates_test/geometries/rock_aa/variants/varD.usdc"
variant_e = "D:/PERSONAL_WORK_AREA/PROJECTS/ZMEU_CUBE/dataops/incoming/20Aug2024/240820_Plates_test/geometries/rock_aa/variants/varE.usdc"
variant_f = "D:/PERSONAL_WORK_AREA/PROJECTS/ZMEU_CUBE/dataops/incoming/20Aug2024/240820_Plates_test/geometries/rock_aa/variants/varF.usdc"

variants_paths = [variant_a, variant_b, variant_c, variant_d, variant_e, variant_f]
variant_set_name = 'myOtherVariantSet'
variants = ["varA", "varB", "varC", "varD", "varE", "varF" ]
variant_name = 'myVariant'

variants_pairs = zip(variants, variants_paths)
print(list(variants_pairs))


# Open the main stage
main_stage_path = 'D:/PERSONAL_WORK_AREA/PROJECTS/maya_anchor/torus-layer1.usda'
main_stage = Usd.Stage.Open(main_stage_path)

# Define a new variant set


# Create or access the variant set
root_prim = main_stage.GetPrimAtPath('/torus_grp')
existing_var_sets = root_prim.GetVariantSets()

# if existing_var_sets.HasVariantSet(variant_set_name):
    # var_set = existing_var_sets.GetVariantSet(variant_set_name)
    # del(var_set)
    # var_set.ClearVariantSelections()
    # var_set.RemoveVariantSet(variant_set_name)

variant_set = root_prim.GetVariantSets().AddVariantSet(variant_set_name)

if not variant_set:
    variant_set = root_prim.GetVariantSets().createVariantSet(variant_set_name)

for variant, var_path in zip(variants, variants_paths):
    variant_set.AddVariant(variant)
    variant_set.SetVariantSelection(variant)
    with variant_set.GetVariantEditContext():
        root_prim.GetPayloads().AddPayload(var_path)
    
        
print(main_stage.GetRootLayer().ExportToString())




# Save changes to the main stage
main_stage.GetRootLayer().Save()
