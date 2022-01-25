# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-22 15:25:32'

""" 
选择骨骼生成和模型生成毛囊
"""

import maya.api.OpenMaya as om
import pymel.core as pm

mesh = "pSphere1"
sel_list = om.MSelectionList()
sel_list.add(str(mesh))
obj = sel_list.getDependNode(0)
node = om.MFnDependencyNode(obj)
plug = om.MPlug( obj, node.attribute("blindDoubleData") )
print(plug)

sData = plug.asMObject()
pdFn = om.MFnPluginData( sData )
data = pdFn.data()
print("DATA",data)
print(data.__class__)

