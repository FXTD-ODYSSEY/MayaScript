# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-22 12:29:35'

"""

"""

import sys
import pymel.core as pm
from collections import defaultdict

sel_list = pm.ls(pm.pickWalk(d="down"),type="mesh")
sel = sel_list[0] if sel_list else sys.exit(0)

mesh_normal = defaultdict(dict)
for vtxFace in sel.vtxFace:
    vert_id,face_id = vtxFace.currentItemIndex()
    mesh_normal[vert_id][face_id] = pm.polyNormalPerVertex(vtxFace,q=1,normalXYZ=1)

print(mesh_normal)
    
