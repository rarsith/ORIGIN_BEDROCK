'''
Creates an asset file that consists of a top level layer and sublayers for
shading and geometry.
'''

from __future__ import print_function

import pathlib
from pxr import Kind, Sdf, Usd, UsdGeom


def usd_create_metadata(prim, attr_name, value_string):
    prim.SetAssetInfoByKey(attr_name, value_string)

def create_asset_simple(assetName, assetDir, assetKind, file_format="usda"):
    assetFilePath = os.path.join(assetDir, '{0}.{1}'.format(assetName, file_format))

    rootLayer = Sdf.Layer.CreateNew(assetFilePath, args={'format': file_format})
    assetStage = Usd.Stage.Open(rootLayer)

    assetPrim = UsdGeom.Xform.Define(assetStage, '/{0}'.format(assetName)).GetPrim()
    assetStage.SetDefaultPrim(assetPrim)

    UsdGeom.SetStageUpAxis(assetStage, UsdGeom.Tokens.y)

    ###
    usd_create_metadata(assetPrim, "version", "v0001")
    ###

    model = Usd.ModelAPI(assetPrim)
    if assetKind:
        model.SetKind(assetKind)

    model.SetAssetName(assetName)
    model.SetAssetIdentifier('{0}/{1}.{2}'.format(assetName, assetName, file_format))


    assetStage.GetRootLayer().Save()


def get_files(root_path, level=None):
    from pathlib import Path
    path = Path(root_path)

    # Check if the specified path is a directory
    if not path.is_dir():
        print(f"{path} is not a valid directory.")
        return

    # If a level is specified, go up to that level
    if level is not None:
        path = path.parent
        for _ in range(level):
            path = path.parent

    # Get the list of files in the directory
    files = [file.name for file in path.iterdir() if file.is_file()]

    # Print the list of files
    for file in files:
        print(file)
    return files


def convert_path(path_to_convert) -> str:
    path_conv = pathlib.Path(path_to_convert)
    unix_path = pathlib.PurePosixPath(path_conv)
    return str(unix_path)


def reference_layers(usd_file_target, layers_paths_to_reference, rel_path=False):
    base_stage = Usd.Stage.Open(usd_file_target)

    for layer in layers_paths_to_reference:
        relative_path = os.path.relpath(layer, os.path.dirname(usd_file_target))
        unix_path = convert_path(relative_path)
        base_stage.GetRootLayer().subLayerPaths.append(str(unix_path))

    base_stage.GetRootLayer().Save()

def add_payload(usd_file_target, payload_usd_path) -> None:
    base_stage = Usd.Stage.Open(usd_file_target)
    default_prim = base_stage.GetDefaultPrim()

    relative_path = os.path.relpath(payload_usd_path, os.path.dirname(usd_file_target))
    unix_path = convert_path(relative_path)

    default_prim.GetPayloads().AddPayload(unix_path)

    base_stage.GetRootLayer().Save()


def add_reference(usd_file_target, reference_usd_path) -> None:
    base_stage = Usd.Stage.Open(usd_file_target)
    default_prim = base_stage.GetDefaultPrim()

    relative_path = os.path.relpath(reference_usd_path, os.path.dirname(usd_file_target))
    unix_path = convert_path(relative_path)

    default_prim.GetReferences().AddReference(unix_path)

    base_stage.GetRootLayer().Save()


# def create_variant_set(usd_file_target, variant_set_name, variants, payload_var_files=False) -> None:
#     base_stage = Usd.Stage.Open(usd_file_target)
#     default_prim = base_stage.GetDefaultPrim()
#
#     variant_set = default_prim.GetVariantSets().AddVariantSet(variant_set_name)
#
#     for variant in variants:
#         variant_set.AddVariant(variant)
#     variant_set.SetVariantSelection(variants[0])
#     base_stage.GetRootLayer().Save()





def _CreateAsset(assetName, assetDir, assetKind, addShadingVariantLayer):
    assetFilePath = os.path.join(assetDir, '%s.usda' % assetName)

    print("Creating asset at %s" % assetFilePath)
    # Make the layer ascii - good for readability, plus the file is small
    rootLayer = Sdf.Layer.CreateNew(assetFilePath, args = {'format':'usda'})
    assetStage = Usd.Stage.Open(rootLayer)

    # Define a prim for the asset and make it the default for the stage.
    assetPrim = UsdGeom.Xform.Define(assetStage, '/%s' % assetName).GetPrim()
    assetStage.SetDefaultPrim(assetPrim)
    # Lets viewing applications know how to orient a free camera properly
    UsdGeom.SetStageUpAxis(assetStage, UsdGeom.Tokens.y)

    # Usually we will "loft up" the kind authored into the exported geometry
    # layer rather than re-stamping here; we'll leave that for a later
    # tutorial, and just be explicit here.
    model = Usd.ModelAPI(assetPrim)
    if assetKind:
        model.SetKind(assetKind)
    
    model.SetAssetName(assetName)
    model.SetAssetIdentifier('%s/%s.usda' % (assetName, assetName))
    
    refs = []
    if addShadingVariantLayer:
        # if we're going to add it, then shading is stronger than geom and needs
        # to be added first
        refs.append('./%s.shadingVariants.usda' % assetName)

    refs.append('./%s.maya.usda' % assetName)

    _CreateAndReferenceLayers(assetPrim, assetDir, refs)

    assetStage.GetRootLayer().Save()


def _CreateAndReferenceLayers(assetPrim, assetDir: str, refs: list):
    from pxr import Usd
    for refLayerPath in refs:
        referencedStage = Usd.Stage.CreateNew(os.path.join(assetDir, refLayerPath))
        referencedAssetPrim = referencedStage.DefinePrim(assetPrim.GetPath())
        referencedStage.SetDefaultPrim(referencedAssetPrim)
        referencedStage.GetRootLayer().Save()

        assetPrim.GetReferences().AddReference(refLayerPath)

    # If you want to print things out, you can do:
    #print(rootLayer.ExportToString())


if __name__ == '__main__':
    import os

    # SETTINGS VARIABLES
    SINGLE_USER = True #(False: the project will be condered MULTIUSER which will make it tasks Statuses Dependent)
    PROJECT_ROOT = r"D:\__SANDBOX\USD"
    ORIGIN_SCENE_ID = "ORIGIN"
    PUBLISHES_PATH = r"publishes\data"
    USD_VARIANT_SET_NAME = "var_set"
    USD_VARIANT_NAME_DELIMITER = "__"
    ENTITY_INTERFACE_SUFFIX = "interface"

    # PIPELINE VARIABLES
    PROJECT = "USD_asset_schemas"
    BRANCH = "templates"
    CATEGORY = "assetCategory"
    ASSET_NAME = "assetName"
    TASK_NAME = "taskName"
    STREAM_ID = "streamName"
    STREAM_FULL_NAME = "assetCategory_assetName_taskName__streamName"
    APPROVED_VERSION = "v001"


    def path_resolve_asset_root():

        return os.path.join(PROJECT_ROOT, PROJECT, BRANCH, CATEGORY, ASSET_NAME)


    def path_resolve_task():
        task_root = path_resolve_asset_root()

        return os.path.join(task_root, TASK_NAME)


    def path_resolve_publishes():
        task_root = path_resolve_task()

        return os.path.join(task_root, PUBLISHES_PATH)


    def file_resolve_full_stream_name():
        stream_base_name = "_".join([CATEGORY, ASSET_NAME, TASK_NAME])

        return "__".join([stream_base_name, STREAM_ID])


    def path_resolve_active_stream():
        publishes_root = path_resolve_publishes()
        stream_full_name = file_resolve_full_stream_name()

        return os.path.join(publishes_root, stream_full_name)


    def name_resolve_version():
        stream_full_name = file_resolve_full_stream_name()
        in_stream_version = "_".join([stream_full_name, APPROVED_VERSION])

        return in_stream_version


    def path_resolve_allowed_publish():
        active_stream = path_resolve_active_stream()
        published_version = name_resolve_version()

        return os.path.join(active_stream, published_version)


    def file_name_resolve_origin(file_format="txt"):
        origin_file_name = "_".join([CATEGORY, ASSET_NAME, ORIGIN_SCENE_ID])

        return f"{origin_file_name}.{file_format}"

    def file_name_resolve_interface(file_format="usda"):
        interface_file_name = "_".join([ASSET_NAME, STREAM_ID, ENTITY_INTERFACE_SUFFIX])

        return f"{interface_file_name}.{file_format}"

    def get_file_origin():
        pub_path = path_resolve_allowed_publish()
        origin_file_name = file_name_resolve_origin()

        return os.path.join(pub_path, origin_file_name)


    def path_resolve_var_sets():
        publish_path = path_resolve_allowed_publish()
        var_sets = os.path.join(publish_path, USD_VARIANT_SET_NAME)

        return var_sets


    def path_get_published_variant_sets():
        from pathlib import Path

        to_var_sets = path_resolve_var_sets()
        p = Path(to_var_sets).glob('**/*')
        var_paths = [str(x) for x in p if x.is_dir()]

        return var_paths


    def files_get_published_variant_set(file_path: str) -> list:
        from pathlib import Path

        p = Path(file_path).glob('**/*')
        var_files = [str(x) for x in p if x.is_file()]

        return var_files


    def get_variant_name_from_file(full_file_path: str) -> str:
        file_from_path = os.path.split(full_file_path)[-1]
        file_name = os.path.splitext(file_from_path)[0]
        var_name = file_name.split("_")[-1]

        return var_name


    def dict_compute_from_var_sets(var_sets_root_paths: list) -> dict:
        var_sets_dict = {}
        for each_path in var_sets_root_paths:
            get_var_files = files_get_published_variant_set(each_path)
            get_parent_dir = os.path.split(each_path)[1]
            var_set_name = get_parent_dir.split(USD_VARIANT_NAME_DELIMITER)[-1]
            var_sets_dict[var_set_name] = get_var_files

        return var_sets_dict


    def add_payload_to_prim(prim, payload_usd_path) -> None:
        target_file_dir = path_resolve_allowed_publish()
        relative_path = os.path.relpath(payload_usd_path, target_file_dir)
        unix_path = convert_path(relative_path)

        prim.GetPayloads().AddPayload(unix_path)


    def create_variant_set(usd_file_target: str, variant_set_data: dict) -> None:
        base_stage = Usd.Stage.Open(usd_file_target)
        default_prim = base_stage.GetDefaultPrim()

        for variant_set, variants_paths in variant_set_data.items():
            variant_set = default_prim.GetVariantSets().AddVariantSet(variant_set)
            for variant in variants_paths:
                var_name = get_variant_name_from_file(variant)
                variant_set.AddVariant(var_name)
                variant_set.SetVariantSelection(var_name)
                with variant_set.GetVariantEditContext():
                    add_payload_to_prim(default_prim, variant)

        base_stage.GetRootLayer().Save()


    asset_name = "taskOutputName"

    asset_root_dir = path_resolve_asset_root()

    ASSET_ROOT = path_resolve_asset_root()

    interface_usd_file = os.path.join(ASSET_ROOT, 'assetName_streamName_interface.usda')#r"D:\__SANDBOX\USD\USD_asset_schemas\asset_A\assetA_interface.usda"

    usd_files_to_reference = [r"D:\__SANDBOX\USD\USD_asset_schemas\templates\assetName\taskName\publishes\data\assetCategory_assetName_taskName__streamName\assetCategory_assetName_taskName__streamName_v001\taskOutputName.usda"]

    geo_variants = ["high", "mid", "low"]
    geo_var_set_name = "geometry_var"
    asset_kind = Kind.Tokens.component
    asset_shading_variant = True

    
    # _CreateAsset(asset_name, asset_dir, asset_kind, asset_shading_variant)

    # create_asset_simple(asset_name, asset_root_dir, asset_kind, file_format="usda")
    # reference_layers(usd_file, usd_files_to_reference)
    # add_payload(usd_file, "D:\\__SANDBOX\\USD\\USD_asset_schemas\\asset_A\\assetA_payload.usda")
    # create_variant_set(usd_file, geo_var_set_name, geo_variants)



    # for usd_source in usd_files_to_reference:
    #     add_reference(interface_usd_file, usd_source)


    test_file_path = 'D:\\__SANDBOX\\USD\\USD_asset_schemas\\templates\\assetCategory\\assetName\\taskName\\publishes\\data\\assetCategory_assetName_taskName__streamName\\assetCategory_assetName_taskName__streamName_v001\\var_set\\var_set__varNameA\\var_preview.usdc'
    get_variant_name_from_file(test_file_path)


    # get_files(asset_root_dir, 0)

    get_pub = path_get_published_variant_sets()
    path_list = dict_compute_from_var_sets(get_pub)

    target_usd_file = r"D:\__SANDBOX\USD\USD_asset_schemas\templates\assetCategory\assetName\taskName\publishes\data\assetCategory_assetName_taskName__streamName\assetCategory_assetName_taskName__streamName_v001\taskOutputName.usda"
    create_variant_set(usd_file_target=target_usd_file, variant_set_data=path_list)

    # print(path)


    # main()
