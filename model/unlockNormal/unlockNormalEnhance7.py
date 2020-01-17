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
    mesh_normal = {}
    itr = om.MItMeshFaceVertex(dagPath)
    while not itr.isDone():
        face_id = itr.faceId()
        vert_id = itr.vertexId()
        normal  = itr.getNormal()

        if not mesh_normal.has_key(vert_id):
            mesh_normal[vert_id] = {}
        # mesh_normal[vert_id][face_id] = [round(data,2) for data in normal]
        mesh_normal[vert_id][face_id] = normal
        itr.next()
    
    # output = r"F:\MayaTecent\MayaScript\model\unlockNormal\data.json"
    # with open(output,'w') as f:
    #     json.dump(mesh_normal,f,indent=4) 
    # return

    pm.progressWindow(	
        title='Unlock model normal',
        progress=0.0,
        status='colleting data...',
        isInterruptable=True )
        
    face_itr = om.MItMeshPolygon(dagPath)
    edge_itr = om.MItMeshEdge(dagPath)
    vert_itr = om.MItMeshVertex(dagPath)
    while not edge_itr.isDone():

        if edge_itr.onBoundary():
            edge_itr.next()
            continue
        
        edge_id = edge_itr.index()
        edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_id)

        if pm.progressWindow( query=True, isCancelled=True ) :
            pm.progressWindow(endProgress=1)
            break
        amount = float(edge_id)/edge_itr.count()*100
        pm.progressWindow( e=1, progress=amount)

        smooth_flag = 0
        hard_flag = 0
        for i in range(2):
            vert_id = edge_itr.vertexId(i)
     
            face_list = edge_itr.getConnectedFaces()

            if len(face_list) != 2:
                print dagPath,edge_itr.index()
                raise RuntimeError(u"model edge should not have 3 faces connected")
            
            face_1,face_2 = face_list

            normal_1 = mesh_normal[vert_id][face_1]
            normal_2 = mesh_normal[vert_id][face_2]

            # vertex = "%s.vtx[%s]" % (dagPath.fullPathName(),vert_id)
            
            # NOTE 法线分叉 说明不是 软边边
            if normal_1 == normal_2:
                vert_itr.setIndex(vert_id)

                vert_avg_normal = om.MVector(0.0, 0.0, 0.0)
                edge_avg_normal = om.MVector(0.0, 0.0, 0.0)
                face_list = vert_itr.getConnectedFaces()
                for face in face_list:
                    face_itr.setIndex(face)
                    normal = face_itr.getNormal()

                    if face in [face_1,face_2]:
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
                    smooth_vtx_list.add(vert_id)
                # NOTE 特殊调整的且统一的法线
                else:
                    edit_list.add(vert_id)
            else:
                # NOTE 硬边或特殊调整的法线
                edit_list.add(vert_id)
                break


        # NOTE 两个点 smooth  (百分百smooth)
        if smooth_flag > 1:
            smooth_list.append(edge)
            

        edge_itr.next()

    # if not smooth_list:
    #     return

    pm.progressWindow( e=1,status='Unlocking...',progress=0)
    
    # NOTE 解锁法线
    pm.polyNormalPerVertex(sel,ufn=1)
            
    # NOTE 添加软边
    pm.polySoftEdge(smooth_list,a=180,ch=0)

    mesh = om.MFnMesh(dagPath)
    total = len(edit_list)
    normal_list = []
    face_list = []
    vtx_list = []
    for i,vert_id in enumerate(edit_list):
        if pm.progressWindow( query=True, isCancelled=True ) :
            pm.progressWindow(endProgress=1)
            break
        amount = float(i)/total * 100
        pm.progressWindow( e=1, progress=amount)
        for face_id,normal in mesh_normal[vert_id].items():
            normal_list.append(normal)
            face_list.append(face_id)
            vtx_list.append(vert_id)
    # NOTE 多个设置比起单个法线设置要快很多
    mesh.setFaceVertexNormals(normal_list,face_list,vtx_list)

    pm.progressWindow( e=1,status='Fixing...',progress=0)

    vtx_list = []
    vert_itr = om.MItMeshVertex(dagPath)
    for i,vert_id in enumerate(smooth_vtx_list):
        if vert_id in edit_list:
            continue
        if pm.progressWindow( query=True, isCancelled=True ) :
            pm.progressWindow(endProgress=1)
            break
        amount = float(i)/total * 100
        pm.progressWindow( e=1, progress=amount)

        vert_itr.setIndex(vert_id)
        for nor_1,nor_2 in combinations(vert_itr.getNormals(),2):
            if (nor_1 - nor_2).length() > thersold:
                break
        else:
            continue
        vertex = "%s.vtx[%s]" % (dagPath.fullPathName(),vert_id)
        vtx_list.append(vertex)

    # pm.select(["%s.vtx[%s]" % (dagPath.fullPathName(),vert_id) for vert_id in edit_list])
    pm.polySoftEdge(vtx_list,a=180,ch=0)

    pm.flushUndo()
    pm.progressWindow(endProgress=1)

    print "elapsed time : %s s" % (time.time() - curr)

if __name__ == "__main__":
    try:
        unlockNormal()
    except :
        import traceback
        traceback.print_exc()
