import pymel.core as pm
import pymel.core.datatypes as dt
from maya import OpenMaya

def getCamPos():
    # NOTE 获取当前摄像机
    cur_mp = None
    for mp in pm.getPanel(type="modelPanel"):
        if pm.modelEditor(mp, q=1, av=1):
            cur_mp = mp
            break
    cam = pm.modelEditor(cur_mp, q=1,cam=1)
    cam_pos = dt.Vector(pm.xform(cam,q=1,ws=1,t=1))
    return cam_pos

    
# NOTE 获取当前选择的顶点
vtx_list = [sel for sel in pm.ls(sl=1,fl=1) if type(sel) is pm.general.MeshVertex]
mesh = sel.node()

vtx_data = []
for vtx in vtx_list:
    
    # NOTE 获取朝向摄像机的向量
    vtx_pos = vtx.getPosition(space="world")
    toCam = getCamPos() - dt.Vector(vtx_pos)
    toCam.normalize()

    # NOTE 生成 BoudingBox 来获取相邻的顶点
    vec = dt.Vector(0.1)
    min_pt = dt.Point.apicls(vtx_pos-vec)
    max_pt = dt.Point.apicls(vtx_pos+vec)
    bbox = dt.BoundingBox.apicls(min_pt,max_pt)

    vtx_data.append({'toCam':toCam,'bbox':bbox,'vtx_list':{vtx.index()}})


# NOTE 遍历所有的 bbox 获取相邻顶点
itr = OpenMaya.MItMeshVertex(mesh.__apimdagpath__())
idx_list = set()
while not itr.isDone():
    idx = itr.index()

    if idx in vtx_data:
        itr.next()
        continue

    pt = itr.position(OpenMaya.MSpace.kWorld)
    
    for data in vtx_data:
        vtx_list = data['vtx_list']
        if idx in vtx_list:
            continue
        bbox = data['bbox']
        if bbox.contains(pt):
            vtx_list.add(idx)
            break
    itr.next()

ratio = 0.5
for data in vtx_data:
    face_vtx_data = {}
    toCam = data['toCam']
    
    # NOTE 单个顶点平均化
    avg_set_list = set()
    for idx in data['vtx_list']:
        vtx = pm.PyNode("%s.vtx[%s]" % (mesh,idx))

        # NOTE 法线 ToFace
        pm.polySetToFaceNormal(vtx,su=True)
        N_data = {}
        for face in vtx.connectedFaces():
            N = face.getNormal()
            N.normalize()
            N_data[face.index()] = N
            
        avg_set_1 = set()
        avg_set_2 = set()
        for face_idx,normal in N_data.items():
            if abs(normal.dot(N)) > ratio or abs(normal.dot(toCam)) < ratio:
                avg_set_1.add("%s.vtxFace[%s][%s]" % (mesh,idx,face_idx))
            else:
                avg_set_2.add("%s.vtxFace[%s][%s]" % (mesh,idx,face_idx))

        if avg_set_1:
            pm.polyAverageNormal(avg_set_1)
        if avg_set_2:
            pm.polyAverageNormal(avg_set_2)

        avg_set_list.update(avg_set_2)

    pm.polyAverageNormal(avg_set_list)
    