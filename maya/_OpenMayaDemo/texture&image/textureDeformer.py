
# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-23 23:52:23'

"""
http://www.polygon.me/2017/04/texture-based-deformer.html
"""

import maya.OpenMaya as om  
import maya.OpenMayaFX as omfx  

obj_sel = om.MSelectionList()  
obj_sel.add('pSphere1')  
obj_dag = om.MDagPath()  
obj_sel.getDagPath(0, obj_dag)  
itr = om.MItMeshVertex(obj_dag)  

length = itr.count()  
scaler = 1  

#declare arrays  
vtx_pos_array = om.MPointArray()  
vtx_nor_array = om.MVectorArray()  
uv_array = om.MIntArray()  
uColArray = om.MDoubleArray()  
vColArray = om.MDoubleArray()  

#set array lengths  
vtx_pos_array.setLength(length)  
vtx_nor_array.setLength(length)  
uColArray.setLength(length)  
vColArray.setLength(length)  

#declare vars for itr  
global_count = 0  
v_pos = om.MPoint()  
n_vec = om.MVector()  

#horrible MScriptUtil shenanigans  
uv_list = [0, 0]  
uv_util = om.MScriptUtil()  
uv_util.createFromList(uv_list, 2)  
uv = uv_util.asFloat2Ptr()  

#iterate to get uv positions  
while not itr.isDone():  
    itr.getUV(uv, 'map1')  
    v_pos =      itr.position(om.MSpace.kWorld)  
    vtx_pos_array.set(v_pos, global_count)  
    itr.getNormal(n_vec, om.MSpace.kWorld)  
    vtx_nor_array.set(n_vec, global_count)       
    u = uv_util.getFloat2ArrayItem(uv, 0, 0)  
    v = uv_util.getFloat2ArrayItem(uv, 0, 1)       
    uColArray.set(u, global_count)  
    vColArray.set(v, global_count)  
    global_count += 1  
    itr.next()  

#get color attribute from node        
imgObj = om.MObject()  
sel = om.MSelectionList()  
om.MGlobal.getSelectionListByName('lambert2', sel)  
sel.getDependNode(0, imgObj)  
fnThisNode = om.MFnDependencyNode(imgObj)  
attr = fnThisNode.attribute( "color" )  

#set up output arrays for avalDynamics2dTexture  
outColours = om.MVectorArray()  
outAlphas = om.MDoubleArray()  

#do it!  
omfx.MDynamicsUtil.evalDynamics2dTexture(imgObj, attr, uColArray, vColArray, outColours, outAlphas)  
    
itr.reset()  
global_count = 0  

#iterate over the mesh to deform it  
while not itr.isDone():  
    point = vtx_pos_array[global_count]  
    normal = vtx_nor_array[global_count]  
    colour = outColours[global_count]  
    col_avg = ((colour.x + colour.y + colour.z) /3)  
    pos = om.MPoint(point.x + (normal.x * col_avg * scaler), point.y + (normal.y * col_avg * scaler), point.z + (normal.z * col_avg * scaler))  
    itr.setPosition(pos, om.MSpace.kWorld)  
    global_count += 1  
    itr.next()       