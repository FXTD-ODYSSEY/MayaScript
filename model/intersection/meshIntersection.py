# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-09 21:07:42'

"""
查找两个模型穿插的面
"""

import pymel.core as pm
from maya import OpenMaya

def findIntersection(src,dst):

    src_dagPath = src.__apimdagpath__()
    dst_dagPath = dst.__apimdagpath__()
    
    src_itr = OpenMaya.MItMeshEdge(src_dagPath)
    src_mesh = OpenMaya.MFnMesh(src_dagPath)
    
    dst_mesh = OpenMaya.MFnMesh(dst_dagPath)
    
    util = OpenMaya.MScriptUtil()
    edge_len_ptr = util.asDoublePtr()

    face_list = set()
    pt_list = set()
    edge_list = set()
    while not src_itr.isDone():
        src_itr.getLength(edge_len_ptr)
        edge_len = util.getDouble(edge_len_ptr)

        start_pt = src_itr.point(0,OpenMaya.MSpace.kWorld)
        end_pt   = src_itr.point(1,OpenMaya.MSpace.kWorld)

        raySource          = OpenMaya.MFloatPoint(start_pt)
        rayDirection       = OpenMaya.MFloatVector(end_pt - start_pt)
        faceIds            = None
        triIds             = None
        idsSorted          = True
        space              = OpenMaya.MSpace.kWorld
        maxParam           = edge_len
        testBothDirections = True
        accelParams        = dst_mesh.autoUniformGridParams()
        sortHits           = True
        hitPoints          = OpenMaya.MFloatPointArray()
        hitRayParams       = None
        hitFaces           = OpenMaya.MIntArray()
        hitTriangles       = None
        hitBary1s          = None
        hitBary2s          = None

        # NOTE 方向向量一定要记得 normalize 否则结果不对
        rayDirection.normalize()

        gotHit = dst_mesh.allIntersections(
            raySource          ,
            rayDirection       ,
            faceIds            ,
            triIds             ,
            idsSorted          ,
            space              ,
            maxParam           ,
            testBothDirections ,
            accelParams        ,
            sortHits           ,
            hitPoints          ,
            hitRayParams       ,
            hitFaces           ,
            hitTriangles       ,
            hitBary1s          ,
            hitBary2s          ,
        )

        face_list.update(list(hitFaces))
        if gotHit:
            num = hitPoints.length()
            pt_list.update([hitPoints[i] for i in range(num)])
            edge_list.add(src_itr.index())

        src_itr.next()

    # TODO 测试获取到的碰撞点 | 这行生成的 locator 位置很奇怪
    # [pm.spaceLocator(p=(pt.x,pt.y,pt.z)) for pt in pt_list]
    pm.select(["%s.f[%s]" % (dst_dagPath.fullPathName(),face_id) for face_id in face_list])
    # pm.select(["%s.e[%s]" % (src_dagPath.fullPathName(),edge_id) for edge_id in edge_list])

if __name__ == "__main__":
    src,dst = pm.ls(pm.pickWalk(d="down"),type="mesh")
    findIntersection(src,dst)

