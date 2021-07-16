# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-03-16 10:56:58"


import sys

MODULE = r"C:\Program Files\Autodesk\FBX\FBX Python SDK\2020.1\lib\Python27_x64"
sys.path.insert(0, MODULE) if MODULE not in sys.path else None


import time
import os

DIR = os.path.dirname(__file__)

import fbx
import FbxCommon
from fbx import FbxSurfaceMaterial
from fbx import FbxLayerElement
from fbx import FbxLayeredTexture
from fbx import FbxTexture
from fbx import FbxCriteria
from fbx import FbxNodeAttribute


def get_texture(pGeometry):
    textures = {}
    lNbMat = pGeometry.GetNode().GetSrcObjectCount(
        FbxCriteria.ObjectType(FbxSurfaceMaterial.ClassId)
    )
    for lMaterialIndex in range(lNbMat):
        lMaterial = pGeometry.GetNode().GetSrcObject(
            FbxCriteria.ObjectType(FbxSurfaceMaterial.ClassId), lMaterialIndex
        )
        if lMaterial:
            for lTextureIndex in range(FbxLayerElement.sTypeTextureCount()):
                lProperty = lMaterial.FindProperty(
                    FbxLayerElement.sTextureChannelNames(lTextureIndex)
                )
                if not lProperty.IsValid():
                    continue
                lLayeredTextureCount = lProperty.GetSrcObjectCount(
                    FbxCriteria.ObjectType(FbxLayeredTexture.ClassId)
                )
                lNbTextures = lProperty.GetSrcObjectCount(
                    FbxCriteria.ObjectType(FbxTexture.ClassId)
                )
                for j in range(lNbTextures):
                    lTexture = lProperty.GetSrcObject(
                        FbxCriteria.ObjectType(FbxTexture.ClassId), j
                    )
                    if lTexture:
                        textures[lMaterial.GetName()] = lTexture.GetRelativeFileName()

    return textures


def main():
    FBX_file = os.path.join(DIR, "ShT_Tower_A.fbx")
    manager, scene = FbxCommon.InitializeSdkObjects()
    result = FbxCommon.LoadScene(manager, scene, FBX_file)
    if not result:
        return

    nodes = scene.GetRootNode()
    if not nodes:
        return

    # NOTE 读取 FBX 贴图路径
    data = {}
    for i in range(nodes.GetChildCount()):
        node = nodes.GetChild(i)
        if not node.GetNodeAttribute():
            continue
        mesh = node.GetNodeAttribute()
        attribute_type = mesh.GetAttributeType()
        if attribute_type != FbxNodeAttribute.eMesh:
            continue
        data[node.GetName()] = get_texture(mesh)

    print(data)


if __name__ == "__main__":
    main()
