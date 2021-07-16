# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 15:30:31'

"""
完美解决 FBX 法线解锁 丢失问题
"""
import time
from maya import cmds
import pymel.core as pm
import pymel.core.datatypes as dt
import maya.api.OpenMaya as om
from itertools import combinations

def unlockNormal(thersold=0.01):

    curr = time.time()
    
    sel = pm.ls(sl=1,dag=1,ni=1,type="mesh")
    if not sel:
        raise 

    sel = sel[0]

    smooth_list = set()
    hard_list = set()

    edit_list = []
    # pm.progressWindow()

    # NOTE OpenMaya 加速遍历过程 
    sel_list = om.MSelectionList()
    sel_list.add(sel.fullPathName())
    dagPath = sel_list.getDagPath(0)

    # NOTE 获取 mesh 所有的法线信息
    mesh_normal = {}
    itr = om.MItMeshFaceVertex(dagPath)
    while not itr.isDone():
        face_id = itr.faceId()
        vert_id = itr.vertexId()
        normal  = itr.getNormal(space=om.MSpace.kWorld)

        if not mesh_normal.has_key(vert_id):
            mesh_normal[vert_id] = {}
        mesh_normal[vert_id][face_id] = normal
        itr.next()


    # NOTE 解锁法线 | 添加软边
    pm.polyNormalPerVertex(sel,ufn=1)
    pm.polySoftEdge(sel,a=180,ch=0)

    itr = om.MItMeshFaceVertex(dagPath)
    while not itr.isDone():
        face_id = itr.faceId()
        vert_id = itr.vertexId()
        normal  = itr.getNormal(space=om.MSpace.kWorld)
        
        _normal = mesh_normal[vert_id][face_id]

        if (_normal - normal).length() > thersold:
            edit_list.append([_normal,face_id,vert_id])
        else:
            vertex = "%s.vtx[%s]" % (dagPath.fullPathName(),vert_id)
            smooth_list.add(vertex)

        itr.next()

    mesh = om.MFnMesh(dagPath)
    for data in edit_list:
        _normal,face_id,vert_id = data
        try:
            mesh.setFaceVertexNormal(_normal,face_id,vert_id)
        except:
            import traceback
            traceback.print_exc()
            print vert_id,face_id
            raise 

    vtx_list = []
    for vtx in smooth_list:
        vtx = pm.PyNode(vtx)
        for nor_1,nor_2 in combinations(vtx.getNormals(),2):
            if (nor_1 - nor_2).length() > 0.001:
                break
        else:
            continue
        
        vtx_list.append(vtx)

    pm.polySoftEdge(vtx_list,a=180,ch=0)

    # print edit_list
    print "elapsed time : %s s" % (time.time() - curr)

if __name__ == "__main__":
    try:
        unlockNormal()
    except :
        import traceback
        traceback.print_exc()
