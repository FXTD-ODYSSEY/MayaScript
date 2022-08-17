# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-08-17 21:36:34'


import maya.api.OpenMaya as om
from maya import cmds
# NOTES(timmyliang): 新建场景
cmds.file(new=1,f=1)
# NOTES(timmyliang): 创建一个球
cmds.polySphere()

# NOTES(timmyliang): 获取当前选择
selection_list = om.MGlobal.getActiveSelectionList()

dag_path = selection_list.getDagPath(0)
dag_node = om.MFnDagNode(dag_path)
print(dag_node.partialPathName())
# 打印: pSphere1

# NOTES(timmyliang): 获取 shape 节点 (连接在 shape 上)
obj = dag_node.child(0)
dep_node = om.MFnDependencyNode(obj)
print(dep_node.name())
# 打印: pSphereShape1

array = dep_node.getConnections()
for plug in array:
    print(plug.name())
# 打印: pSphereShape1.instObjGroups[0]
# 打印: pSphereShape1.inMesh
