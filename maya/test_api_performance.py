# -*- coding: utf-8 -*-
"""
create a sphere with random offset
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-07-20 13:09:04"


import random
import time


def log_time(func):
    def decorator(*args, **kwargs):
        curr = time.time()
        res = func(*args, **kwargs)
        print("[{0}] elapsed time: {1}".format(func.__name__, time.time() - curr))
        return res

    return decorator


@log_time
def openmaya_1(sx=50, sy=50):
    from maya import OpenMaya

    OpenMaya.MGlobal.executeCommand("polySphere -sx {sx} -sy {sy}".format(sx=sx, sy=sy))
    selection_list = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getActiveSelectionList(selection_list)
    sphere_dag_path = OpenMaya.MDagPath()
    selection_list.getDagPath(0, sphere_dag_path)
    itr = OpenMaya.MItMeshVertex(sphere_dag_path)

    while not itr.isDone():
        pt = itr.position()
        rand = (random.random() - 0.5) / 20
        itr.setPosition(pt + OpenMaya.MVector(rand, rand, rand))
        itr.next()


@log_time
def openmaya_2(sx=50, sy=50):
    from maya.api import OpenMaya
    from maya import cmds

    cmds.polySphere(sx=sx, sy=sy)
    selection_list = OpenMaya.MGlobal.getActiveSelectionList()
    sphere_dag_path = selection_list.getDagPath(0)
    itr = OpenMaya.MItMeshVertex(sphere_dag_path)

    while not itr.isDone():
        pt = itr.position()
        rand = (random.random() - 0.5) / 20
        itr.setPosition(pt + OpenMaya.MVector(rand, rand, rand))
        itr.next()


@log_time
def maya_cmds(sx=50, sy=50):
    from maya import cmds

    sphere = cmds.polySphere(sx=sx, sy=sy)[0]
    for vtx in cmds.ls("{0}.vtx[*]".format(sphere), fl=True):
        pt = cmds.pointPosition(vtx)
        rand = (random.random() - 0.5) / 20
        cmds.xform(vtx, t=(pt[0] + rand, pt[1] + rand, pt[2] + rand))


if __name__ == "__main__":
    sx = 150
    sy = 150
    maya_cmds(sx, sy)
    openmaya_1(sx, sy)
    openmaya_2(sx, sy)
