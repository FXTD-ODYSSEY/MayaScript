# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-25 15:42:22'

"""
选顶点生成曲线
"""

import pymel.core as pm

# NOTE 开启顺序获取
if not pm.selectPref(q=1,tso=1):
    pm.selectPref(tso=1)

vtx_list = []
for vtx in pm.ls(sl=1,fl=1,os=1):
    if type(vtx) == pm.general.MeshVertex:
        vtx_list.append(vtx)

    
# NOTE 生成曲线
curve = pm.curve(d=1,p=[vtx.getPosition(space="world") for vtx in vtx_list])
# NOTE 闭合曲线
pm.closeCurve(curve,ch=0,rpo=1)

