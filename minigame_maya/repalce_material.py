# -*- coding: utf-8 -*-
"""
选择对应的模型 
将 颜色贴图 连接到 透明通道 上
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-16 22:23:11'

import pymel.core as pm
import pymel.core.nodetypes as nt
for sel in pm.ls(sl=1):
    shape = sel.getShape()
    for shading in shape.shadingGroups():
        for mat in shading.connections():
            if not isinstance(mat,nt.Phong):
                continue
            print(mat)
            f = mat.color.connections()
            if not f:
                continue
            f = f[0]
            try:
                f.outTransparency.connect(mat.transparency)
            except:
                pass
