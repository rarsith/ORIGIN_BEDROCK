"""

Query - attr values
Create - new database entry
Update - attr values
Add - attr values
Set - replaces attr values
Remove - deletes attr values
Publish - complex - creates db entry based on the context (current Task), contains all task output_slots versioned
    and status controlled


## Assets Tasks dependencies

taskName = [taskNameA, taskNameB]
e.g: "modeling" = ["concept"]
e.g: "texturing" = ["modeling"]
e.g: "rigging" = ["modeling"]
e.g: "grooming" = ["modeling"]
e.g: "lookdev" = ["modeling", "texturing", "grooming"]
e.g: "setup_hair" = ["grooming"]
e.g: "setup_cloth" = ["modeling"]
e.g: "setup_fx" = ["modeling", "grooming"]

## Shots Tasks dependencies
assetName -> taskName -> override_layer = ["taskNameA"]

sequence assignments:
    - assets.environment

shot assignments:
    - assets.slots (each asset used from the project .assets location)
    - assets.environmentAssemblies.overrides (position, replacements, offsets)
    - background/foreground plate.split
    - lighting (publishable lights.layer.usd)
    - hdr env
    - sound


-- prerequisites: plate_io -> master_plate, preview_plate, anim_plate, proxy_plate, original

e.g. "matchmove" = ["plate_io", "assetName.stream.lidar"] -> camera_track, camera_cg, witness_camA, witness_camB..., distorsion, undisorted_plate, ref_cones
e.g. "rotomation" = ["plate_io", "matchmove", camera_cg, "assetName.stream.lidar"] -> assetName -> overrideLayer -> rotomation.assetName.rotom_layerName.usd (cache)
e.g. "layout" = ["plate_io", "matchmove", "assetName.stream.lidar"] -> camera_cg, set_dressing(assemblies), shot_content_slots
e.g. "animation" = ["plate_io", "layout", "assetName.rigging"] -> assetName.anim_cache_layerName.usd
e.g. "cfx" = ["plate_io", "animation.assetName.anim_cache_layerName.usd"]
        -> cfx.assetName.muscle_layerNameA.usd
        -> cfx.assetName.cloth_layerNameA.usd, cfx.assetName.cloth_layerNameB.usd
        -> cfx.assetName.hair_layerNameA.usd
e.g. "fx" = ["plate_io", "cfx" = [assetName.cfx_cache_layerName.usd"],"animation" = ["assetName.anim_cache_layerName.usd"], "rotomation"= [assetName.rotom_layerName.usd]]
        -> fx.fxAssetName_layerName.usd
        -> fx.assetName.fxAssetName_layerName.usd

e.g. "lighting" = [camera_cg, ]




"""
