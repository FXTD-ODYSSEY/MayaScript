# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-09 22:45:33'

"""
来自徐国良大大的脚本
"""

import pymel.core as pm
import maya.api.OpenMaya as om


def pynode_to_api2(pynode):
    selectionList = om.MSelectionList()
    selectionList.add(pynode.name())
    nodeDagPath = selectionList.getDagPath(0)
    return nodeDagPath


def get_inter_bbox(bbox1, bbox2):
    if not bbox1.intersects(bbox2):
        return None
    inter_min_x = max(bbox1.min().x, bbox2.min().x)
    inter_min_y = max(bbox1.min().y, bbox2.min().y)
    inter_min_z = max(bbox1.min().z, bbox2.min().z)
    inter_min = om.MPoint(inter_min_x, inter_min_y, inter_min_z, 1.0)

    inter_max_x = min(bbox1.max().x, bbox2.max().x)
    inter_max_y = min(bbox1.max().y, bbox2.max().y)
    inter_max_z = min(bbox1.max().z, bbox2.max().z)
    inter_max = om.MPoint(inter_max_x, inter_max_y, inter_max_z, 1.0)

    return om.MBoundingBox(inter_min, inter_max)


def test_mesh_intersection(current_mesh, target_mesh):
    # get intersection bbox
    inter_bbox = get_inter_bbox(current_mesh.boundingBox(), target_mesh.boundingBox())
    # check if edge of current mesh intersect to face of target mesh
    all_hit_faces = []
    all_hit_points = []
    for edge in target_mesh.edges:
        sour_point = om.MPoint(edge.getPoint(0, 'world'))
        end_point = om.MPoint(edge.getPoint(1, 'world'))
        # ignore edge not in inter bbox
        if not (inter_bbox.contains(sour_point) or inter_bbox.contains(end_point)):
            continue
        # do test
        
        current_mesh_om = om.MFnMesh(pynode_to_api2(current_mesh))
        edge_vector = end_point - sour_point
        speedup_param = current_mesh_om.autoUniformGridParams()
        hitPoints, _, hit_faces, _, _, _ = current_mesh_om.allIntersections(
            om.MFloatPoint(sour_point),  # 射线起点
            om.MFloatVector(edge_vector),  # 射线方向
            om.MSpace.kWorld,  # 世界空间
            edge_vector.length(),  # 测试距离，超出此距离的命中不算
            True,  # 不进行双向测试
            accelParams=speedup_param  # 加速参数
        )

        all_hit_points.extend(hitPoints)
        all_hit_faces.extend([current_mesh.f[face_id] for face_id in hit_faces])

    # [pm.spaceLocator(p=(pt.x,pt.y,pt.z)) for pt in all_hit_points]
    return all_hit_faces


a,b = pm.selected()

pm.select(test_mesh_intersection(a, b))
