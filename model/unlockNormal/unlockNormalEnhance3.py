# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 15:30:31'

"""
由于Maya unlock normal 会丢失当前法线
因此开发一个脚本解决这个问题
2.0 解決三角面识别不了问题 | 添加进度条
"""
import time
import pymel.core as pm
from maya import OpenMaya
import maya.api.OpenMaya as om
from itertools import combinations

def unlockNormal():
    
    curr = time.time()

    sel = pm.ls(sl=1,dag=1,ni=1,type="mesh")
    if not sel:
        return
    
    sel = sel[0]
    smooth_list = []
    
    # pm.progressWindow()

    # NOTE OpenMaya 加速遍历过程 
    sel_list = om.MSelectionList()
    sel_list.add(sel.fullPathName())
    dagPath = sel_list.getDagPath(0)

    edge_itr = om.MItMeshEdge(dagPath)
    vert_itr = om.MItMeshVertex(dagPath)
    
    exclude_list = []
    normal_data = {}
    while not edge_itr.isDone():
        idx = edge_itr.index()

        normal_list = []
        flag = 0
        for i in range(2):
            vert_idx = edge_itr.vertexId(i)
            vert_itr.setIndex(vert_idx)
            normals = vert_itr.getNormals()
            value = sum([round(val,2) for vec in normals for val in vec])
            normal_list.append(value)

            # NOTE 检查列表元素是否全部相等来判断是否是完全平滑的点
            # NOTE http://www.voidcn.com/article/p-oqthigpz-bsh.html
            if normals[1:] != normals[:-1]:
                flag += 1

        if flag == 2:
            pass

        normal_data[idx] = normal_list

        edge_itr.next()
    
    # NOTE 解锁法线
    pm.polyNormalPerVertex(sel,ufn=1)
    # NOTE 整体添加硬边
    pm.polySoftEdge(sel,a=0)

    edge_itr = om.MItMeshEdge(dagPath)
    vert_itr = om.MItMeshVertex(dagPath)
    while not edge_itr.isDone():
        flag = 0
        idx = edge_itr.index()
        normal_list = normal_data[idx]
        for i in range(2):
            vert_idx = edge_itr.vertexId(i)
            vert_itr.setIndex(vert_idx)
            normals = vert_itr.getNormals()
            value = sum([round(val,2) for vec in normals for val in vec])

            if value not in normal_list:
                flag += 1

        if flag == 2:
            edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_itr.index())
            smooth_list.append(edge) 
        edge_itr.next()

    pm.polySoftEdge(smooth_list,a=180,ch=0)
    pm.select(smooth_list)

    print "elapsed time : %s s" % (time.time() - curr)

if __name__ == "__main__":
    unlockNormal()
