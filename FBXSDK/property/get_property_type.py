import fbx
import inspect

for name, member in inspect.getmembers(fbx):
    if name.startswith("e") and isinstance(member, fbx.EFbxType):
        print(name, member)
fbx_prop_map = {
    "FbxBool": fbx.FbxPropertyBool1,
    "FbxInt": fbx.FbxPropertyInteger1,
    "FbxFloat": fbx.FbxPropertyFloat1,
    "FbxDouble": fbx.FbxPropertyDouble1,
    "FbxDouble2": fbx.FbxPropertyDouble2,
    "FbxDouble3": fbx.FbxPropertyDouble3,
    "FbxDouble4": fbx.FbxPropertyDouble4,
    "FbxAMatrix": fbx.FbxPropertyXMatrix,
    "FbxTime": fbx.FbxPropertyFbxTime,
    "FbxDateTime": fbx.FbxPropertyDateTime,
    "FbxEnum": fbx.FbxPropertyEnum,
    "FbxString": fbx.FbxPropertyString,
    "EFbxRotationOrder": fbx.FbxPropertyEFbxRotationOrder,
    "FbxReference": fbx.FbxPropertyFbxReference,
    "FbxBlob": fbx.FbxPropertyBlob,
}


fbx_data_type = {
    member: name[1:]
    for name, member in inspect.getmembers(fbx)
    if name.startswith("e") and isinstance(member, fbx.EFbxType)
}

