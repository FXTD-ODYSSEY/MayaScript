# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-09-16 16:00:09"


# from pymel.tools import mel2py
# mel_str = r'copySkinWeights  -noMirror -surfaceAssociation closestComponent -influenceAssociation oneToOne -influenceAssociation closestJoint;'
# py_str = mel2py.mel2pyStr(mel_str, pymelNamespace="pm")
# print(py_str)
# pm.copySkinWeights(surfaceAssociation='closestComponent', influenceAssociation=['oneToOne', 'closestJoint'], noMirror=1)

import pymel.core as pm

base_list = []
for mesh in pm.ls(sl=1, dag=1, type="mesh", ni=1):
    base_mesh = mesh.split(":")[-1]
    if not pm.objExists(base_mesh):
        continue
    pm.select(mesh,base_mesh,r=1)
    base_mesh = pm.PyNode(base_mesh)
    # base_list.append(base_mesh.getParent())
    pm.copySkinWeights(surfaceAssociation='closestComponent', influenceAssociation=['oneToOne', 'closestJoint'], noMirror=1)

# pm.select(base_list)
