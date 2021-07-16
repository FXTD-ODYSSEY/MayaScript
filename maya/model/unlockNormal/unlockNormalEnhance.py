# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 15:30:31'

"""
由于Maya unlock normal 会丢失当前法线
因此开发一个脚本解决这个问题·
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
    
    # NOTE OpenMaya 加速遍历过程 
    # NOTE Benchmark 选择400个面的基础球体
    # NOTE OpenMaya elapsed time : 0.010999917984 s
    # NOTE PyMel    elapsed time : 2.47600007057 s

    # NOTE OpenMaya 方案
    sel_list = om.MSelectionList()
    sel_list.add(mesh.fullPathName())
    dagPath = sel_list.getDagPath(0)

    edge_itr = om.MItMeshEdge(dagPath)
    vert_itr = om.MItMeshVertex(dagPath)
    
    while not edge_itr.isDone():
        flag = 0
        for i in range(2):
            vert_idx = edge_itr.vertexId(i)
            vert_itr.setIndex(vert_idx)
            for nor_1,nor_2 in combinations(vert_itr.getNormals(),2):
                if (nor_1 - nor_2).length() < 0.001:
                    flag += 1
                    break
            else:
                continue
        
        if flag == 2:
            edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_itr.index())
            smooth_list.append(edge) 
        edge_itr.next()
    
    # NOTE PyMel 方案
    # for edge in mesh.edges:
    #     flag = 0
    #     for vtx in edge.connectedVertices():
    #         for nor_1,nor_2 in combinations(vtx.getNormals(),2):
    #             if (nor_1 - nor_2).length() < 0.001:
    #                 flag += 1
    #                 break
    #         else:
    #             continue

    #     if flag == 2:
    #         smooth_list.append(edge)

    pm.polyNormalPerVertex(mesh,ufn=1)
    pm.polySoftEdge(smooth_list,a=180,ch=0)
    # pm.select(smooth_list)

    print "elapsed time : %s s" % (time.time() - curr)

if __name__ == "__main__":
    unlockNormal()