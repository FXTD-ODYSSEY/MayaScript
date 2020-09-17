# -*- coding: utf-8 -*-
"""
查询一样的模型
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-17 00:00:27'

import json
from collections import defaultdict

import pymel.core as pm

material_list = [
    'bas_ca_wall_stone_3m_00_mat1'
]

for mat in material_list:
    pm.hyperShade(objects=mat)
    data = defaultdict(list)
    for mesh in pm.ls(sl=1,objectsOnly=1):
        verts = mesh.numVertices()
        transform = mesh.getTransform()
        data[verts].append(transform.fullPathName())
    print(json.dumps(data))
        
    # sel_list = [s.getParent() for s in pm.ls(sl=1,objectsOnly=1)]
    # pm.polyEvaluate()
    # pm.select(sel_list)