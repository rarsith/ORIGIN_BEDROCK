import maya.cmds as cmds

file_path = "D:/__SANDBOX/USD/test_asset.maya.usda"

cmds.file(  file_path,
            force=True,
            options=";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=0;eulerFilter=0;staticSingleSample=0;startTime=1;endTime=1;frameStride=1;frameSample=0.0;defaultUSDFormat=usda;parentScope=modeling;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface,MaterialX];exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;worldspace=0;jobContext=[Arnold];materialsScopeName=mtl",            typ = "USD Export",
            pr=True,
            es=True
            )
            
            
cmds.file(  i=True,
            type="USD Import",
            ignoreVersion=True,
            ra=True,
            mergeNamespacesOnClash=False,
            namespace="test_asset",
            options=";shadingMode=[[useRegistry,rendermanForMaya],[useRegistry,MaterialX],[pxrRis,none],[useRegistry,UsdPreviewSurface],[displayColor,none],[none,none]];preferredMaterial=none;primPath=/;readAnimData=0;useCustomFrameRange=0;startTime=0;endTime=0;importUSDZTextures=0",
            pr=True,
            importFrameRate=True,
            importTimeRange="override" "D:/__SANDBOX/USD/test_asset.usd"
            )

