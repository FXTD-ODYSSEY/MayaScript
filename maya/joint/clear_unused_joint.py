# -*- coding: utf-8 -*-
"""

"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-06-27 17:05:04"

# Import third-party modules
import pymel.core as pm

# NOTES(timmyliang): get mesh
mesh = pm.PyNode("wrap_Mesh").getShape()
# NOTES(timmyliang): get joint hierarchy
all_joints = pm.ls("wrap_head", type="joint", dag=1)

# NOTES(timmyliang): get influence joint include parent (keep parent for hierarchy)
jnt_set = {
    part
    for skin in mesh.history(type="skinCluster")
    for jnt in pm.skinCluster(skin, inf=1, q=1)
    for part in jnt.longName().split("|")
    if part
}

# NOTES(timmyliang): select unused joint
pm.select([jnt for jnt in all_joints if str(jnt) not in jnt_set])
