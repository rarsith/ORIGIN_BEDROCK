"""
Query().all_shows.names
Update().all_shows.names
Query().current_show.structures
Query().parent.name

Query.projects.all.names
Query.

Query().path.to_root

Query().path.all_ascendants.to_root
Query().path.all_descendants.types

Query().path.to_parent.name
Query().path.to_parent.type
Query().path.to_parent.config
Query().path.to_parent.definitions
Query().path.to_parent.templates
Query().path.to_parent.data


Query().all_tasks.names
Query().all_tasks.statuses
Query().task.imports_from
Query().task.output_slots.names


Query().task.output_slot(name).data
Update().task.output_slot(name).data
Remove().task.output_slot(name).data
Create().task.output_slot(name).data






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
