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
import pymel.core as pm
import maya.api.OpenMaya as om

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

    # NOTE 获取 mesh 所有的法线信息
    itr = om.MItMeshFaceVertex(dagPath)
    mesh_normal = {}
    while not itr.isDone():
        face_id = itr.faceId()
        vert_id = itr.vertexId()
        normal  = itr.getNormal()

        if not mesh_normal.has_key(vert_id):
            mesh_normal[vert_id] = {}
        mesh_normal[vert_id][face_id] = normal
        itr.next()

    edge_itr = om.MItMeshEdge(dagPath)
    vert_itr = om.MItMeshVertex(dagPath)
    while not edge_itr.isDone():
        
        # NOTE 测试
        # if edge_itr.index() != 43:
        #     edge_itr.next()
        #     continue

        if edge_itr.onBoundary():
            edge_itr.next()
            continue

        for i in range(2):
            vert_idx = edge_itr.vertexId(i)
            vert_itr.setIndex(vert_idx)
            try:
                face_1,face_2 = edge_itr.getConnectedFaces()
            except:
                print dagPath,edge_itr.index()
                import traceback
                traceback.print_exc()
                raise
            normal_1 = mesh_normal[vert_idx][face_1]
            normal_2 = mesh_normal[vert_idx][face_2]
            if normal_1 != normal_2:
                break
        else:
            edge = "%s.e[%s]" % (dagPath.fullPathName(),edge_itr.index())
            smooth_list.append(edge) 
            
        edge_itr.next()

        

    # NOTE 解锁法线
    pm.polyNormalPerVertex(sel,ufn=1)
    # NOTE 添加软边边
    pm.polySoftEdge(smooth_list,a=180,ch=0)

    # pm.select(smooth_list)

    print "elapsed time : %s s" % (time.time() - curr)

if __name__ == "__main__":
    unlockNormal()
