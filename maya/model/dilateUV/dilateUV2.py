# -*- coding: utf-8 -*-
"""
UV shell 膨胀
经过吴真大佬的点播，决定用新方案重写
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-12-04 09:52:53"

import os
import sys
import json
import threading
from collections import defaultdict

from Qt import QtGui, QtCore, QtWidgets

from maya import OpenMaya
import pymel.core as pm
import pymel.core.datatypes as dt


def error_log(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except:
            import traceback

            QtWidgets.QMessageBox.warning(
                None, u"警告", u"错误 \n%s" % traceback.format_exc()
            )

    return wrapper


def vecRot90CW(v):
    return dt.Vector(v.y, -v.x)


def vecRot90CCW(v):
    return dt.Vector(-v.y, v.x)


def polyIsCw(v1, v2):
    return vecRot90CW(v1) * v2 >= 0


def get_pt(pos, pos1, pos2, vec1, vec2, distant, reverse=False):
    rot = vecRot90CCW if polyIsCw(vec1, vec2) else vecRot90CW
    vec1 = rot(vec1)
    vec1.normalize()
    d = vec1 * distant
    if reverse:
        d = -d
    line1_0 = pos + d
    line1_1 = pos1 + d

    vec2 = rot(vec2)
    vec2.normalize()
    d = vec2 * distant
    if reverse:
        d = -d
    line2_0 = pos + d
    line2_1 = pos2 + d

    a1 = line1_1.x - line1_0.x
    b1 = line2_0.x - line2_1.x
    c1 = line2_0.x - line1_0.x
    a2 = line1_1.y - line1_0.y
    b2 = line2_0.y - line2_1.y
    c2 = line2_0.y - line1_0.y

    val = a2 * b1 - a1 * b2
    if val == 0:
        x = line1_0.x
        y = line1_0.y
    else:
        t = (b1 * c2 - b2 * c1) / val
        x = line1_0.x + t * (line1_1.x - line1_0.x)
        y = line1_0.y + t * (line1_1.y - line1_0.y)

    return x, y


@error_log
def main():
    sel_list = pm.ls(pm.pickWalk(d="down"), ni=1, type="mesh")
    if not sel_list:
        QtWidgets.QMessageBox.warning(None, u"警告", u"请选择一个模型")
        return
    sel = sel_list[0]
    # pm.undoInfo(ock=1)

    num_list, total = sel.getUvShellsIds()
    shell_dict = {num: i for i, num in enumerate(num_list)}
    border_dict = defaultdict(dict)
    uv_dict = {}

    for i, uv in shell_dict.items():
        pm.select(sel.map[uv])
        pm.polySelectConstraint(uv=1, bo=0, m=2)
        uv_list = pm.ls(pm.polySelectConstraint(uv=0, rs=1),fl=1)
        face_list = pm.polyListComponentConversion(fuv=1, tf=1)
        border_list = pm.ls(pm.polyListComponentConversion(fuv=1, te=1, bo=1),fl=1)
        _border_list = [e.index() for e in border_list]
        
        edge_dict = {
            edge: {
                face.getUVIndex(j): face.getUV(j) for j in range(face.polygonVertexCount())
            }
            for face in pm.ls(face_list, fl=1)
            for edge in face.getEdges()
            if edge in _border_list
        }
        
        border_dict = {}
        border_uvs = pm.polyListComponentConversion(border_list,fe=1, tuv=1)
        border_uvs = [uv for uv in pm.ls(border_uvs,fl=1) if uv in uv_list]
        for uv in border_uvs:
            edges = pm.polyListComponentConversion(uv, fuv=1, te=1)
            edges = [e for e in pm.ls(edges, fl=1) if e in border_list]
            uvs = pm.polyListComponentConversion(edges, fe=1, tuv=1)
            uvs = [_uv for _uv in pm.ls(uvs, fl=1) if _uv != uv and _uv in border_uvs]
            border_dict[uv] = uvs
            
        print(border_dict)
        break
        # print(json.dumps(edge_dict))

    return

    # TODO 遍历 polygon 找 UV 对应关系

    dag_path = sel.__apimdagpath__()
    itr = OpenMaya.MItMeshPolygon(dag_path)

    util = OpenMaya.MScriptUtil()

    edge_dict = defaultdict(list)
    while not itr.isDone():
        face_idx = itr.index()

        uv = {}
        for i in range(itr.polygonVertexCount()):
            idx_ptr = util.asIntPtr()
            u_ptr = util.asFloatPtr()
            v_ptr = util.asFloatPtr()
            itr.getUVIndex(i, idx_ptr, u_ptr, v_ptr)
            idx = util.getInt(idx_ptr)
            u = util.getFloat(u_ptr)
            v = util.getFloat(v_ptr)
            uv[idx] = (u, v)

        edges = OpenMaya.MIntArray()
        itr.getEdges(edges)
        for i in range(edges.length()):
            edge = edges[i]
            edge_dict[edge].append({"uv": uv, "face_idx": face_idx})

        itr.next()

    edge_list = []
    for edge_idx, data in edge_dict.items():
        print(len(data))
        if len(data) == 1:
            edge_list.append(edge_idx)
    print(edge_list)
    # print(json.dumps(edge_dict))

    return

    pm.progressWindow(title=u"获取 uv border", status=u"获取模型 uv border...", progress=0.0)
    for i, uv in shell_dict.items():
        pm.progressWindow(e=1, progress=i / total * 100)
        # NOTES(timmyliang) 如果 uv 不在 0,1 象限则跳过
        x, y = sel.getUV(uv)

        if not 0 < x < 1 or not 0 < y < 1:
            continue

        pm.select(sel.map[uv])
        pm.polySelectConstraint(uv=1, bo=0, m=2)
        uv_list = pm.polySelectConstraint(t=0x0010, uv=0, bo=1, m=2, rs=1)
        uv_list = [_uv.currentItemIndex() for _uv in pm.ls(uv_list, fl=1)]
        pos_list = {uv: sel.getUV(uv) for uv in uv_list}
        x = sum([pos[0] for pos in pos_list.values()]) / len(pos_list)
        y = sum([pos[1] for pos in pos_list.values()]) / len(pos_list)
        uv_dict.update(pos_list)
        borders = pm.polyListComponentConversion(fuv=1, te=1, bo=1)
        borders = pm.ls(borders, fl=1)
        for uv in uv_list:
            edges = pm.polyListComponentConversion(sel.map[uv], fuv=1, te=1)
            edges = [e for e in pm.ls(edges, fl=1) if e in borders]
            uvs = pm.polyListComponentConversion(edges, fe=1, tuv=1)
            uvs = [_uv.currentItemIndex() for _uv in pm.ls(uvs, fl=1)]
            uvs = [_uv for _uv in uvs if _uv != uv and _uv in uv_list]
            border_dict[uv] = {"uvs": uvs, "center": (x, y)}

    pm.progressWindow(ep=1)
    pm.polySelectConstraint(uv=0, bo=0, rs=1)

    distant = 0.01

    for uv, data in border_dict.items():
        uvs = data.get("uvs", [])
        if len(uvs) <= 1:
            continue
        uv1, uv2 = uvs
        x, y = data.get("center")
        center = dt.Vector(x, y)

        pos = dt.Vector(*uv_dict[uv])
        pos1 = dt.Vector(*uv_dict[uv1])
        pos2 = dt.Vector(*uv_dict[uv2])
        vec1 = pos - pos1
        vec2 = pos2 - pos

        x, y = get_pt(pos, pos1, pos2, vec1, vec2, distant)
        pt = dt.Vector(x, y)
        vec = pos - pt
        line = pos - center
        # NOTE reverse
        if vec.dot(line) > 0:
            x, y = get_pt(pos, pos1, pos2, vec1, vec2, distant, True)
        sel.setUV(uv, x, y)

    face_list = pm.polyUVOverlap(sel.faces, oc=True)
    pm.undoInfo(cck=1)

    # pm.undo()
    # pm.selectType(facet=1,ocm=1)
    # pm.hilite()
    # pm.select(face_list)


if __name__ == "__main__":
    main()
