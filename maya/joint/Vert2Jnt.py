# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-22 14:10:13'

""" 
将选中的模型点 转换为骨骼
"""

import pymel.core as pm

sel_list = pm.ls(sl=1,fl=1)
pm.select(cl=1)
jnt_list = []
for sel in sel_list:
    if type(sel)== pm.general.MeshVertex:
        pos = sel.getPosition(space="world")
        jnt = pm.joint()
        jnt.t.set(pos)
        jnt_list.append(jnt)
        pm.select(cl=1)

pm.select(jnt_list)