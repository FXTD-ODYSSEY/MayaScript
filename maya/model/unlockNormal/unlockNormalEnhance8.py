# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 15:30:31'

"""
完美解决 FBX 法线解锁 丢失问题
"""
import time
import json
import pymel.core as pm
import pymel.core.datatypes as dt
import maya.api.OpenMaya as om
from itertools import combinations

def getAvgVertNormal(face_list,face_itr):
    vert_avg_normal = om.MVector()
    for face in face_list:
        face_itr.setIndex(face)
        normal = face_itr.getNormal()
        vert_avg_normal += normal
    vert_avg_normal = vert_avg_normal/len(face_list)
    return vert_avg_normal

def getMeshNormals(dagPath):
    mesh_normal = {}
    itr = om.MItMeshFaceVertex(dagPath)
    while not itr.isDone():
        face_id = itr.faceId()
        vert_id = itr.vertexId()
        normal  = itr.getNormal()

        if not mesh_normal.has_key(vert_id):
            mesh_normal[vert_id] = {}
        mesh_normal[vert_id][face_id] = normal
        itr.next()
    return mesh_normal

def unlockNormal(thersold=0.05):
    
    curr = time.time()

    sel = pm.ls(sl=1,dag=1,ni=1,type="mesh")
    if not sel:
        return
    
    sel = sel[0]

    smooth_list = []
    hard_list = []
    smooth_vtx_list = set()
    edit_list = set()
    


    # NOTE OpenMaya 加速遍历过程 
    sel_list = om.MSelectionList()
    sel_list.add(sel.fullPathName())
    dagPath = sel_list.getDagPath(0)

    # NOTE 获取 mesh 所有的法线信息
    mesh_normal = getMeshNormals(dagPath)

    # # NOTE 解锁法线
    # pm.polyNormalPerVertex(sel,ufn=1)
    # hard_vert_list = set()

    # itr = om.MItMeshFaceVertex(dagPath)
    # while not itr.isDone():
    #     face_id = itr.faceId()
    #     vert_id = itr.vertexId()
    #     normal  = itr.getNormal()

    #     if (normal - mesh_normal[vert_id][face_id]).length() < thersold:
    #         hard_vert_list.add("%s.vtx[%s]" % (dagPath.fullPathName(),vert_id))

    #     itr.next()


    # pm.polySoftEdge(sel,a=180,ch=0)
    # soft_vert_list = set()

    # itr = om.MItMeshFaceVertex(dagPath)
    # while not itr.isDone():
    #     face_id = itr.faceId()
    #     vert_id = itr.vertexId()
    #     normal  = itr.getNormal()

    #     if (normal - mesh_normal[vert_id][face_id]).length() < thersold:
    #         soft_vert_list.add("%s.vtx[%s]" % (dagPath.fullPathName(),vert_id))

    #     itr.next()

    # print list(hard_vert_list)
    # print list(soft_vert_list)

    # return  
    # NOTE -----------------

    pm.progressWindow(	
        title='Unlock model normal',
        progress=0.0,
        status='colleting data...',
        isInterruptable=True )
        
    face_itr = om.MItMeshPolygon(dagPath)
    edge_itr = om.MItMeshEdge(dagPath)
    vert_itr = om.MItMeshVertex(dagPath)
    mesh = om.MFnMesh(dagPath)

    avg_vert_list = set()
    avg_edge_list = set()
    nonAvg_vert_list = set()
    modify_vert_list = set()
    edge_list = []
    while not vert_itr.isDone():
        vert_id = vert_itr.index()
        if pm.progressWindow( query=True, isCancelled=True ) :
            pm.progressWindow(endProgress=1)
            break
        amount = float(vert_id)/vert_itr.count()*100
        pm.progressWindow( e=1, progress=amount)

        # normals = vert_itr.getNormals()
        normals = mesh_normal[vert_id].values()

        normals_set = set()

        [normals_set.add(nor.length()) for nor in normals]

        vtx = "%s.vtx[%s]" % (dagPath.fullPathName(),vert_id)
        if len(normals_set) != 1:
            for edge in vert_itr.getConnectedEdges():
                if edge not in edge_list:
                    edge_list.append("%s.e[%s]" % (dagPath.fullPathName(),edge))

            # nonAvg_vert_list.add("%s.vtx[%s]" % (dagPath.fullPathName(),vert_id))
            nonAvg_vert_list.add(vert_id)
        # else:
        #     normal = normals[0]
        #     face_list = vert_itr.getConnectedFaces()
        #     if (normal - getAvgVertNormal(face_list,face_itr)).length() > thersold:
        #         modify_vert_list.add(vtx)
        #     else:
        #         avg_vert_list.add(vtx)
        #         for edge in vert_itr.getConnectedEdges():
        #             avg_edge_list.add("%s.e[%s]" % (dagPath.fullPathName(),edge))

        vert_itr.next()

    # print nonAvg_vert_list
    # pm.select(nonAvg_vert_list)
    pm.polyNormalPerVertex(sel,ufn=1)
    pm.polySoftEdge(sel,a=180,ch=0)

    normal_list = []
    face_list = []
    vtx_list = []
    for i,vert_id in enumerate(nonAvg_vert_list):
        # if i > 20:
        #     break
        for face_id,normal in mesh_normal[vert_id].items():
            normal_list.append(normal)
            face_list.append(face_id)
            vtx_list.append(vert_id)
    # NOTE 多个设置比起单个法线设置要快很多
    mesh.setFaceVertexNormals(normal_list,face_list,vtx_list)

    
    # pm.select(avg_edge_list)
    # dul = pm.duplicate(sel,rr=1)[0]
    # # NOTE 解锁法线
    # pm.polyNormalPerVertex(sel,ufn=1)
    # # NOTE 添加软边
    # pm.polySoftEdge(sel,a=180,ch=0)

    # pm.select(dul,r=1)
    # pm.select(vert_list,r=1)
    # pm.transferAttributes(transferNormals=1 ,sampleSpace=4 ,searchMethod=3)

    # while not edge_itr.isDone():

    #     if edge_itr.onBoundary():
    #         edge_itr.next()
    #         continue
        
    #     edge_id = edge_itr.index()
    #     edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_id)

    #     if pm.progressWindow( query=True, isCancelled=True ) :
    #         pm.progressWindow(endProgress=1)
    #         break
    #     amount = float(edge_id)/edge_itr.count()*100
    #     pm.progressWindow( e=1, progress=amount)

    #     smooth_flag = 0
    #     hard_flag = 0
    #     for i in range(2):
    #         vert_id = edge_itr.vertexId(i)
     
    #         face_list = edge_itr.getConnectedFaces()

    #         if len(face_list) != 2:
    #             print dagPath,edge_itr.index()
    #             raise RuntimeError(u"model edge should not have 3 faces connected")
            
    #         face_1,face_2 = face_list

    #         normal_1 = mesh_normal[vert_id][face_1]
    #         normal_2 = mesh_normal[vert_id][face_2]

    #         # vertex = "%s.vtx[%s]" % (dagPath.fullPathName(),vert_id)
            
    #         # NOTE 法线分叉 说明不是 软边边
    #         if normal_1 == normal_2:
    #             vert_itr.setIndex(vert_id)

    #             vert_avg_normal = om.MVector(0.0, 0.0, 0.0)
    #             edge_avg_normal = om.MVector(0.0, 0.0, 0.0)
    #             face_list = vert_itr.getConnectedFaces()
    #             for face in face_list:
    #                 face_itr.setIndex(face)
    #                 normal = face_itr.getNormal()

    #                 if face in [face_1,face_2]:
    #                     edge_avg_normal += normal

    #                 vert_avg_normal += normal
    #             vert_avg_normal = vert_avg_normal/len(face_list)
    #             edge_avg_normal = edge_avg_normal/2

                
    #             vert_avg_1 = (vert_avg_normal - normal_1).length()
    #             vert_avg_2 = (vert_avg_normal - normal_2).length()
    #             edge_avg_1 = (edge_avg_normal - normal_1).length()
    #             edge_avg_2 = (edge_avg_normal - normal_2).length()
    #             # NOTE 判断顶点是否近似 average 
    #             if (vert_avg_1 < thersold and vert_avg_2 < thersold)\
    #             or (edge_avg_1 < thersold and edge_avg_2 < thersold):
    #                 smooth_flag += 1
    #                 smooth_vtx_list.add(vert_id)
    #             # NOTE 特殊调整的且统一的法线
    #             else:
    #                 edit_list.add(vert_id)
    #         else:
    #             # NOTE 硬边或特殊调整的法线
    #             edit_list.add(vert_id)
    #             break


    #     # NOTE 两个点 smooth  (百分百smooth)
    #     if smooth_flag > 1:
    #         smooth_list.append(edge)
            

    #     edge_itr.next()

    # # if not smooth_list:
    # #     return

    # pm.progressWindow( e=1,status='Unlocking...',progress=0)
    
    # # NOTE 解锁法线
    # pm.polyNormalPerVertex(sel,ufn=1)
            
    # # NOTE 添加软边
    # pm.polySoftEdge(smooth_list,a=180,ch=0)

    # mesh = om.MFnMesh(dagPath)
    # total = len(edit_list)
    # normal_list = []
    # face_list = []
    # vtx_list = []
    # for i,vert_id in enumerate(edit_list):
    #     if pm.progressWindow( query=True, isCancelled=True ) :
    #         pm.progressWindow(endProgress=1)
    #         break
    #     amount = float(i)/total * 100
    #     pm.progressWindow( e=1, progress=amount)
    #     for face_id,normal in mesh_normal[vert_id].items():
    #         normal_list.append(normal)
    #         face_list.append(face_id)
    #         vtx_list.append(vert_id)
    # # NOTE 多个设置比起单个法线设置要快很多
    # mesh.setFaceVertexNormals(normal_list,face_list,vtx_list)

    # pm.progressWindow( e=1,status='Fixing...',progress=0)

    # vtx_list = []
    # vert_itr = om.MItMeshVertex(dagPath)
    # for i,vert_id in enumerate(smooth_vtx_list):
    #     if vert_id in edit_list:
    #         continue
    #     if pm.progressWindow( query=True, isCancelled=True ) :
    #         pm.progressWindow(endProgress=1)
    #         break
    #     amount = float(i)/total * 100
    #     pm.progressWindow( e=1, progress=amount)

    #     vert_itr.setIndex(vert_id)
    #     for nor_1,nor_2 in combinations(vert_itr.getNormals(),2):
    #         if (nor_1 - nor_2).length() > thersold:
    #             break
    #     else:
    #         continue
    #     vertex = "%s.vtx[%s]" % (dagPath.fullPathName(),vert_id)
    #     vtx_list.append(vertex)

    # # pm.select(["%s.vtx[%s]" % (dagPath.fullPathName(),vert_id) for vert_id in edit_list])
    # pm.polySoftEdge(vtx_list,a=180,ch=0)

    # pm.flushUndo()
    pm.progressWindow(endProgress=1)

    print "elapsed time : %s s" % (time.time() - curr)

if __name__ == "__main__":
    try:
        unlockNormal()
    except :
        import traceback
        traceback.print_exc()
