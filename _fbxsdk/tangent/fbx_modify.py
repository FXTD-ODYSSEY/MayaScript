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


def modify_material_index(mesh):
    count = mesh.GetElementMaterialCount()
    for i in range(count):
        layer = mesh.GetElementMaterial(i)
        array = layer.GetIndexArray()
        array.SetAt(1, 0)
        array.SetAt(2, 0)
        array.SetAt(3, 0)
        array.SetAt(4, 0)
        print(list(array))

def modify_mesh_tangent(mesh):
    # NOTE 将法线信息存储到切线上
    if not mesh.GetElementTangentCount():
        mesh.GenerateTangentsData()
    tangent = mesh.GetElementTangent()
    tangent_array = tangent.GetDirectArray()
    normal = mesh.GetElementNormal()
    normal_array = normal.GetDirectArray()
    tangent_array.Clear()
    for normal in normal_array:
        tangent_array.Add(normal)

def main():
    # FbxLayerElementMaterial
    # fbx_path = os.path.join(DIR, "Layers.fbx")
    fbx_path = r"F:\MayaTecent\MayaScript\_fbxsdk\tangent\bs_test.fbx"

    manager, scene = FbxCommon.InitializeSdkObjects()
    result = FbxCommon.LoadScene(manager, scene, fbx_path)
    if not result:
        return

    data = {}
    for i in range(scene.GetNodeCount()):
        node = scene.GetNode(i)
        mesh = node.GetNodeAttribute()
        if not mesh or mesh.GetAttributeType() != FbxNodeAttribute.eMesh:
            continue
        
        print(node.GetName())
        for i in range(mesh.GetDeformerCount()):
            deformer = mesh.GetDeformer(i)
            print(deformer)

    # print(data)
    # output_file = os.path.join(DIR, "tangent_cube2.fbx")
    # FbxCommon.SaveScene(manager, scene, output_file)


if __name__ == "__main__":
    main()
