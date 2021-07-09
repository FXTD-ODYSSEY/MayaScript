# -*- coding: utf-8 -*-
"""
断开骨骼的约束
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-07-08 11:04:46'

import pymel.core as pm

for jnt in pm.ls(sl=1,dag=1,ni=1,type="joint"):
    print(jnt
    for attr in 'tr':
        for axis in 'xyz':
            attribute = getattr(jnt,attr + axis)
            if not attribute.isLocked():
                pm.mel.CBdeleteConnection(attribute)