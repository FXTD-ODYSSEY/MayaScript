# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-06-01 14:01:01"


import sys

MODULE = r"C:\Program Files\Autodesk\FBX\FBX Python SDK\2020.1\lib\Python27_x64"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None


import time
import os

DIR = os.path.dirname(__file__)

import FbxCommon
from fbx import FbxNodeAttribute



def main():
    # FbxLayerElementMaterial
    # fbx_path = os.path.join(DIR, "Layers.fbx")
    fbx_path = r"X:\Characters\Roles\Actor\Mihawk01\Combine\Rig\SK_Mihawk01_L.fbx"

    manager, scene = FbxCommon.InitializeSdkObjects()
    result = FbxCommon.LoadScene(manager, scene, fbx_path)
    if not result:
        return

    # lSceneInfo.mTitle = "Example scene"
    # lSceneInfo.mSubject = "Illustrates the creation and animation of a deformed cylinder."
    # lSceneInfo.mAuthor = "ExportScene01.exe sample program."
    # lSceneInfo.mRevision = "rev. 1.0"
    # lSceneInfo.mKeywords = "deformed cylinder"
    # lSceneInfo.mComment = "no particular comments required."
    
    info = scene.GetSceneInfo()
    print(info)
    print(info.mTitle)
    print(info.mSubject)
    print(info.mAuthor)
    print(info.mRevision)
    print(info.mKeywords)
    print(info.mComment)
    
    
    # # NOTE 读取 FBX 贴图路径
    # data = {}
    # for i in range(scene.GetNodeCount()):
    #     node = scene.GetNode(i)
    #     mesh = node.GetNodeAttribute()
    #     if not mesh or mesh.GetAttributeType() != FbxNodeAttribute.eMesh:
    #         continue
    #     name = node.GetName()
    #     attr = mesh.GetElementTangent()
    #     data[node.GetName()] = attr.GetDirectArray()
    #     # modify_mesh_tangent(mesh)
    # print(data)
    # # output_file = os.path.join(DIR, "tangent_cube2.fbx")
    # # FbxCommon.SaveScene(manager, scene, output_file,0)


if __name__ == "__main__":
    main()
