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
    mesh = pm.ls(sl=1,dag=1,ni=1,type="mesh")
    if not mesh:
        return
    
    mesh = mesh[0]
    smooth_list = []
    
    # pm.progressWindow()

    # NOTE OpenMaya 加速遍历过程 
    sel_list = om.MSelectionList()
    sel_list.add(mesh.fullPathName())
    dagPath = sel_list.getDagPath(0)

    edge_itr = om.MItMeshEdge(dagPath)
    vert_itr = om.MItMeshVertex(dagPath)
    
    normal_data = {}
    while not edge_itr.isDone():
        for i in range(2):
            vert_idx = edge_itr.vertexId(i)
            vert_itr.setIndex(vert_idx)
            normals = vert_itr.getNormals()
            edges = vert_itr.getConnectedEdges()

            for nor,edge in zip(normals,edges):
                if edge == edge_itr.index():
                    if i == 0:
                        normal_list = [nor]
                    else:
                        normal_list.append(nor)
                        normal_data[edge_itr.index()] = normal_list
                    break

        # if length > 0.0001:
        #     edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_itr.index())
        #     smooth_list.append(edge) 
        edge_itr.next()

    # print normal_data
    # NOTE 解锁法线
    pm.polyNormalPerVertex(mesh,ufn=1)
    # NOTE 整体添加硬边
    pm.polySoftEdge(mesh,a=0,ch=0)

    edge_itr = om.MItMeshEdge(dagPath)
    while not edge_itr.isDone():
        flag = 0
        for i in range(2):
            vert_idx = edge_itr.vertexId(i)
            vert_itr.setIndex(vert_idx)
            normals = vert_itr.getNormals()
            edges = vert_itr.getConnectedEdges()

            for nor,edge in zip(normals,edges):
                if edge == edge_itr.index():
                    _nor = normal_data[edge_itr.index()][i]
                    if (nor - _nor).length() < 0.01:
                        flag += 1
                        break

        if flag == 2:
            edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_itr.index())
            smooth_list.append(edge) 
        edge_itr.next()


    # pm.polySoftEdge(smooth_list,a=180,ch=0)
    pm.select(smooth_list)

    print "elapsed time : %s s" % (time.time() - curr)

if __name__ == "__main__":
    unlockNormal()