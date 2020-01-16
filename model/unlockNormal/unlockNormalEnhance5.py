# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 15:30:31'

"""
由于Maya unlock normal 会丢失当前法线
因此开发一个脚本解决这个问题
2.0 解決三角面识别不了问题
"""
import time
from maya import cmds
import pymel.core as pm
import pymel.core.datatypes as dt
import maya.api.OpenMaya as om

def unlockNormal(thersold=0.05):
    
    curr = time.time()

    sel = pm.ls(sl=1,dag=1,ni=1,type="mesh")
    if not sel:
        return
    
    sel = sel[0]

    smooth_list = []
    hard_list = []
    sp_list = {}
    
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
        normal  = itr.getNormal()

        if not mesh_normal.has_key(vert_id):
            mesh_normal[vert_id] = {}
        mesh_normal[vert_id][face_id] = normal
        itr.next()

    face_itr = om.MItMeshPolygon(dagPath)
    edge_itr = om.MItMeshEdge(dagPath)
    vert_itr = om.MItMeshVertex(dagPath)
    while not edge_itr.isDone():

        if edge_itr.onBoundary():
            edge_itr.next()
            continue
        
        smooth_flag = 0
        hard_flag = 0
        for i in range(2):
            vert_idx = edge_itr.vertexId(i)
     
            face_list = edge_itr.getConnectedFaces()

            if len(face_list) != 2:
                print dagPath,edge_itr.index()
                raise RuntimeError(u"model edge should not have 3 faces connected")
            
            face_1,face_2 = face_list

            normal_1 = mesh_normal[vert_idx][face_1]
            normal_2 = mesh_normal[vert_idx][face_2]
            
            # NOTE 法线分叉 说明是 硬边
            if normal_1 != normal_2:
                hard_flag += 1
                continue

            vert_itr.setIndex(vert_idx)

            vert_avg_normal = om.MVector(0.0, 0.0, 0.0)
            edge_avg_normal = om.MVector(0.0, 0.0, 0.0)
            face_list = vert_itr.getConnectedFaces()
            for face in face_list:
                face_itr.setIndex(face)
                normal = face_itr.getNormal()

                if face == face_1:
                    face_1_normal = normal
                    edge_avg_normal += normal
                elif face == face_2:
                    face_2_normal = normal
                    edge_avg_normal += normal

                vert_avg_normal += normal
            vert_avg_normal = vert_avg_normal/len(face_list)
            edge_avg_normal = edge_avg_normal/2

            
            vert_avg_1 = (vert_avg_normal - normal_1).length()
            vert_avg_2 = (vert_avg_normal - normal_2).length()
            edge_avg_1 = (edge_avg_normal - normal_1).length()
            edge_avg_2 = (edge_avg_normal - normal_2).length()
            # NOTE 判断顶点是否近似 average 
            if (vert_avg_1 < thersold and vert_avg_2 < thersold)\
            or (edge_avg_1 < thersold and edge_avg_2 < thersold):
                smooth_flag += 1
            else:
                # NOTE 过滤 非 hard
                _normal_1 = (face_1_normal - normal_1).length()
                _normal_2 = (face_2_normal - normal_2).length()
                if _normal_1 < thersold*5 and _normal_2 < thersold*5:
                    hard_flag += 1
                else:
                    vertex = "%s.vtx[%s]" % (dagPath.fullPathName(),vert_idx)
                    if vertex not in sp_list:
                        sp_list[vertex] = normal_1


        edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_itr.index())
        # NOTE 两个点 smooth  (百分百smooth)
        if smooth_flag > 1:
            smooth_list.append(edge)
        if hard_flag > 0:
            hard_list.append(edge)


        edge_itr.next()

        
    if not hard_list:
        return
    

    # # NOTE 解锁法线
    # pm.polyNormalPerVertex(sel,ufn=1)
    
    # # NOTE 添加软边
    # pm.polySoftEdge(sel,a=180,ch=0)

    # # NOTE 添加硬边
    # pm.polySoftEdge(hard_list,a=0,ch=0)

    # NOTE 添加硬边
    pm.polySoftEdge(sel,a=0,ch=0)

    # NOTE 解锁法线
    pm.polyNormalPerVertex(sel,ufn=1)

    # NOTE 添加软边
    pm.polySoftEdge(smooth_list,a=180,ch=0)
    
    for vtx,normal in sp_list.items():
        pm.polyNormalPerVertex(vtx,xyz=list(normal))

    print "elapsed time : %s s" % (time.time() - curr)

if __name__ == "__main__":
    try:
        unlockNormal()
    except :
        import traceback
        traceback.print_exc()
