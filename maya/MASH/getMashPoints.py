# -*- coding: utf-8 -*-
"""
获取 MASH 生成的顶点位置~
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-08-26 23:23:27'

import MASH.api as mapi
from maya import OpenMaya
import pymel.core as pm

# NOTE 删除之前生成的 loc 
pm.delete([grp for grp in pm.ls(assemblies=1) if grp.startswith("frame")])

data = {}
min_time = pm.playbackOptions(q=1,min=1)
max_time = pm.playbackOptions(q=1,max=1)
for i in range(int(min_time),int(max_time)+1):
    pm.currentTime(i,update=1)
    
    mashNetwork = mapi.Network("MASH1")
    # NOTE 这个是 MASH1_Repro 节点
    node = pm.PyNode(mashNetwork.instancer)
    # NOTE 获取 MPlug 属性
    obj = node.inputPoints.__apiobject__().asMObject()
    inputPointsData = OpenMaya.MFnArrayAttrsData(obj)
    positions = inputPointsData.getVectorData("position")
    
    loc_list = []
    # TODO 不能直接 for 循环 | 会导致 Maya 崩溃
    for i in range(positions.length()):
        pt = positions[i]
        loc = pm.spaceLocator()
        loc.t.set((pt.x,pt.y,pt.z))
        loc_list.append(loc)
    pm.group(loc_list,n="frame_%s" % i)
    data[i] = mashNetwork.position
print (data)
