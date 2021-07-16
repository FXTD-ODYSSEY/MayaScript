# -*- coding: utf-8 -*-
"""
BaseMap X:/Characters/Roles/Actor/Chopper01/St/Textures/TGA/T_Chopper01_St_body_Base.tga
SssMap X:/Characters/Roles/Actor/Chopper01/St/Textures/TGA/T_Chopper01_St_body_Sss.tga
IlmMap X:/Characters/Roles/Actor/Chopper01/St/Textures/TGA/T_Chopper01_St_body_Ilm.tga
DetailMap X:/Characters/line/T_CHR_Line02.psd
X:/Shaders/IH_Character_ST.fx
BaseMap X:/Characters/Roles/Actor/Chopper01/L/Textures/TGA/T_Chopper01_L_body_Base.tga
SssMap X:/Characters/Roles/Actor/Chopper01/L/Textures/TGA/T_Chopper01_L_body_Sss.tga
IlmMap X:/Characters/Roles/Actor/Chopper01/L/Textures/TGA/T_Chopper01_L_body_Ilm.tga
DetailMap X:/Characters/line/T_CHR_Line02.psd
X:/Shaders/IH_Character_L.fx
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-05-19 16:46:55'



import sys

MODULE = r"C:\Program Files\Autodesk\FBX\FBX Python SDK\2020.1\lib\Python27_x64"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None


import time
import os

import fbx
import FbxCommon
from fbx import FbxCriteria, FbxTexture, FbxImplementation, FbxVideo


def iterate_properties(root):
    prop = root
    while prop.IsValid():
        prop = root.GetNextDescendent(prop)
        yield prop


def main():
    FBX_file = (
        r"X:\Characters\Roles\Actor\Chopper01\Combine\Rig\SK_Chopper01_Combine.fbx"
    )
    manager, scene = FbxCommon.InitializeSdkObjects()
    result = FbxCommon.LoadScene(manager, scene, FBX_file)
    if not result:
        return

    texture_type = FbxCriteria.ObjectType(FbxTexture.ClassId)
    impl_type = FbxCriteria.ObjectType(FbxImplementation.ClassId)
    video_type = FbxCriteria.ObjectType(FbxVideo.ClassId)
    for i in range(scene.GetMaterialCount()):
        material = scene.GetMaterial(i)
        for prop in iterate_properties(material.RootProperty):
            # print(prop.GetName())
            count = prop.GetSrcObjectCount(texture_type)
            for j in range(count):
                texture = prop.GetSrcObject(texture_type, j)
                path = texture.GetFileName()
                print(prop.GetName(), path)
        
        # NOTE 获取 dx11 fx文件 路径
        impl = material.GetDstObject(impl_type, 0)
        if not impl:
            continue
        table = impl.GetTable(0)
        url = table.FindProperty("DescAbsoluteURL")
        video = url.GetSrcObject(video_type, 0)
        if not video:
            continue
        fx_file = video.GetFileName()
        print(fx_file)

if __name__ == "__main__":
    main()
