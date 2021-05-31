# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-05-12 21:33:52'

import fbx
import FbxCommon

def clear_uv(output_file):
    # NOTE 删除第一张 UV 
    manager, scene = FbxCommon.InitializeSdkObjects()
    result = FbxCommon.LoadScene(manager, scene, output_file)
    if not result:
        return
    nodes = scene.GetRootNode()
    mesh = nodes.GetChild(0).GetMesh()
    uv = mesh.GetElementUV(0)
    mesh.RemoveElementUV(uv)
    FbxCommon.SaveScene(manager, scene, output_file)