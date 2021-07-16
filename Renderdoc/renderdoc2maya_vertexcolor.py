# -*- coding: utf-8 -*-
"""
reconstruct vertex color with renderdoc csv information
# TODO cannot figure out the IDX relationship
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-12-02 09:11:05"

import pymel.core as pm
import csv
from maya import OpenMaya


def main():

    mesh_list = pm.ls(pm.pickWalk(d="down"), ni=1, type="mesh")
    if not mesh_list:
        return

    csv_path = r"C:\Users\timmyliang\Desktop\file_test\2020-12-1\head.csv"
    pm.progressWindow(title=u"设置顶点色", status=u"设置顶点色...", progress=0.0)

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        data_list = {
            int(row[" IDX"]): (
                float(row[" COLOR.x"]),
                float(row[" COLOR.y"]),
                float(row[" COLOR.z"]),
                float(row[" COLOR.w"]),
            )
            for row in reader
        }

    mesh = mesh_list[0]
    mfn = mesh.__apimfn__()
    itr = OpenMaya.MItMeshFaceVertex(mesh.__apimobject__())

    face_list = OpenMaya.MIntArray()
    vertex_list = OpenMaya.MIntArray()
    colors = OpenMaya.MColorArray()

    index = -1
    total = len(mesh.vtxFace)
    pm.progressWindow(title=u"设置顶点色", status=u"设置顶点色...", progress=0.0)
    while not itr.isDone():
        index += 1
        pm.progressWindow(e=1, progress=index / total * 100)
        vert_id = itr.vertId()
        face_id = itr.faceId()
        vertex_list.append(vert_id)
        face_list.append(face_id)

        color = data_list.get(vert_id)
        if not color:
            colors.append(OpenMaya.MColor(0, 0, 0))
            itr.next()
            continue
        r, g, b,a = color
        
        colors.append(OpenMaya.MColor(r, g, b))

        itr.next()

    mfn.setFaceVertexColors(colors, face_list, vertex_list)
    pm.progressWindow(ep=1)


if __name__ == "__main__":
    main()
