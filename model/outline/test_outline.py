# import math
# import pymel.core as pm
# import pymel.core.datatypes as dt
# origin_edge_list = [sel for sel in pm.ls(sl=1,fl=1,ni=1) if type(sel) == pm.general.MeshEdge]

# pm.polyExtrudeEdge(origin_edge_list,ch=1,thickness=0.1)
# extrude_edge_list = [sel for sel in pm.ls(sl=1,fl=1,ni=1) if type(sel) == pm.general.MeshEdge]

# match_dict = {}
# index_list = [edge.index() for edge in origin_edge_list]
# for edge in extrude_edge_list:
#     face = edge.connectedFaces()
#     vtx_1,vtx_2 = edge.connectedVertices()
#     vec = vtx_1.getPosition(space="world") - vtx_2.getPosition(space="world")
#     normal = face.getNormal(space="world")

#     # NOTE 计算出 edge 沿着面的法线方向
#     v1 = vec.cross(normal)
#     v2 = dt.Vector(v1.x, 0, v1.z)

#     # NOTE 计算出法线方向对地面的角度
#     angle = math.acos(v1*v2/(v1.length()*v2.length()))
#     angle *= 180 / math.pi
#     for _edge in face.getEdges():
#         if _edge in index_list:
#             match_dict[_edge] = face
#             break

# # for edge,face in match_dict.items():

# # print [k.index() for k in match_dict.keys()]
# # print [k.index() for k in match_dict.values()]

# # NOTE 获取当前的摄像机
# cur_mp = None
# for mp in pm.getPanel(type="modelPanel"):
#     if pm.modelEditor(mp, q=1, av=1):
#         cur_mp = mp
#         break
        
# cam = pm.modelPanel(cur_mp,q=1,cam=1)

# cam = pm.PyNode(cam)

# crx,cry,crz = cam.getRotation(space="world")
# crx = crx * math.pi / 180.0
# cry = cry * math.pi / 180.0
# crz = crz * math.pi / 180.0
# x = math.sin(crz)
# y = -(math.sin(crx) * math.cos(crz))
# z = math.cos(crx) * math.cos(cry)

# vec = dt.Vector(x,y,z) 


# # NOTE 选择当前视图的物体
# import maya.OpenMaya as om
# import maya.OpenMayaUI as omUI
# view = omUI.M3dView.active3dView()
# useDepth = pm.selectPref(q=1,useDepth=1)
# pm.selectPref(useDepth=1)
# om.MGlobal.selectFromScreen( 0, 0, view.portWidth(), view.portHeight(),om.MGlobal.kReplaceList)
# pm.selectPref(useDepth=useDepth)

import maya.api.OpenMaya as om
import pymel.core as pm
from maya import mel
from maya import OpenMaya

def inflateMesh(mesh,scale=1):

    sel_list = om.MSelectionList()
    sel_list.add(str(mesh))

    DagPath,Obj = sel_list.getComponent(0)

    Mesh = om.MFnMesh(DagPath)
    MeshPoints = Mesh.getPoints(om.MSpace.kWorld)
    newMeshPoints = om.MFloatPointArray()

    for i in range(len(MeshPoints)):
        MeshPointNormal = Mesh.getVertexNormal(i , om.MSpace.kWorld)

        x = MeshPoints[i].x + MeshPointNormal.x * scale
        y = MeshPoints[i].y + MeshPointNormal.y * scale
        z = MeshPoints[i].z + MeshPointNormal.z * scale
        newMeshPoint = om.MFloatPoint(x,y,z)

        newMeshPoints.append(newMeshPoint)

    Mesh.setPoints(newMeshPoints, om.MSpace.kWorld)

def getActivePanel():
    cur_mp = None
    for mp in pm.getPanel(type="modelPanel"):
        if pm.modelEditor(mp, q=1, av=1):
            cur_mp = mp
            break
    return cur_mp

def getActiveCamera():
    panel = getActivePanel()
    return pm.PyNode(pm.modelPanel(panel,q=1,cam=1))

def generateProfileCurve(profile_node):
    count = profile_node.outMainCurveCount.get()
    crv_list = []
    for i in range(count):
        attr = profile_node.outMainCurves[i]
        if pm.connectionInfo(attr,isSource=1):
            continue
        crv = pm.createNode("nurbsCurve")
        pm.connectAttr(attr,"%s.create"%crv,f=1)
        attr.disconnect(crv.create)
        crv_list.append(crv.getParent())
    return crv_list

def main():
    
    size = 0.5
        
    mel.eval("""
    source "assignPfxToon.mel";
    """)
    sel_list = pm.ls(sl=1,ni=1)

    cam = getActiveCamera()

    for sel in sel_list:
        # NOTE 通过 Toon 创建轮廓
        mel.eval('assignPfxToon "" 0;')
        # NOTE 获取 Toon 节点
        profile_node = pm.ls(sl=1)[0]
        # NOTE 链接当前摄像机 外轮廓
        cam.t.connect(profile_node.cameraPoint,f=1)

        # NOTE 生成描边曲线
        base_crv_list = generateProfileCurve(profile_node)

        # NOTE 扩大模型
        inflateMesh(sel,scale=size)
        
        inflate_crv_list = generateProfileCurve(profile_node)

        # NOTE 还原模型
        inflateMesh(sel,scale=-size)

        # NOTE 曲线放样成描边模型
        mesh_list = []
        base_grp = pm.group(base_crv_list,n="base_grp")
        inflate_grp = pm.group(inflate_crv_list,n="inflate_grp")
        for base,inflate in zip(base_crv_list,inflate_crv_list):
            # NOTE 相隔太远会导致曲线为空，此时跳过
            if len(base.cv) != len(inflate.cv) and len(base.cv) == 0 and len(inflate.cv) == 0:
                continue

            pm.rebuildCurve(base,ch=0,rpo=1,rt=0,end=1,kr=1,kcp=0,kep=1,kt=0,s=0,d=3,tol=0.01)
            pm.rebuildCurve(inflate,ch=0,rpo=1,rt=0,end=1,kr=1,kcp=0,kep=1,kt=0,s=0,d=3,tol=0.01)
            

            mesh = pm.loft(base,inflate,ch=0,u=1,c=0,ar=1,d=3,ss=1,rn=0,po=1,rsn=1)
            mesh_list.append(mesh)

        # if len(mesh_list) > 2:
        #     pm.polyUnite(mesh_list,n="%s_profile"%sel,ch=0)
        # pm.delete(base_grp,inflate_grp)

        pm.delete(profile_node.getParent())

if __name__ == "__main__":
    main()