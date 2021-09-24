# -*- coding: utf-8 -*-
"""
获取选中模型的世界坐标
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-09-14 19:33:13'


import pymel.core as pm
selected_objects = pm.selected()
obj = selected_objects[0]
print(pm.xform(obj,q=1,ws=1,matrix=1))