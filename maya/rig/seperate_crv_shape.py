# -*- coding: utf-8 -*-
"""
分离曲线 shape 节点
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-03-14 19:41:51"

import pymel.core as pm

# NOTES(timmyliang): 修复重名
shape = pm.PyNode(
    "DigitalHuman_Hua_hair:Hua_l_Hair_L3_splineDescription|DigitalHuman_Hua_hair:Hua_l_SplineGrp0|DigitalHuman_Hua_hair:Hua_l_SplineGrp0"
)
shape.rename("DigitalHuman_Hua_hair:Hua_l_SplineGrp48112")

# NOTES(timmyliang): 将曲线分离
node = pm.PyNode(
    "DigitalHuman_Hua_hair:Hua_l_Hair_L3_splineDescription|DigitalHuman_Hua_hair:Hua_l_SplineGrp0"
)
for i, shape in enumerate(node.getShapes()):
    group = pm.group(em=1, w=1, n="{0}_transform".format(shape))
    shape.setParent(group, r=1, s=1)
