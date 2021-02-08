# -*- coding: utf-8 -*-
"""
选择带 Blendshape 模型 自动打印 Blendshape 下变化的点
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-25 17:25:41'


import pymel.core as pm
import pymel.core.datatypes as dt

thersold = 0.015

sel_list = pm.ls(pm.pickWalk(d='down'),type="mesh")
for sel in sel_list:
    
    for BS in pm.ls(sel.listConnections(),type="blendShape"):
        grp = BS.inputTarget[0].inputTargetGroup
        for idx in (grp.getArrayIndices()):
            components = grp[idx].inputTargetItem[6000].inputComponentsTarget.get()
            points = grp[idx].inputTargetItem[6000].inputPointsTarget.get()
             
            if not components or not points:
                continue
            verts = ["%s.%s" % (sel,vtx) for vtx in components]
            verts = [vtx.__melobject__() for pt,vtx in zip(points,pm.ls(verts,fl=1)) if dt.Vector(pt).length() > thersold]
            print(idx,verts)
            