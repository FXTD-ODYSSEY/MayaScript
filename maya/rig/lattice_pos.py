# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-10-16 17:36:25"

import pymel.core as pm
import pymel.core.datatypes as dt


def create_lattice_mesh(lattice):

    pos_list = []
    transform = lattice.getParent()
    matrix = transform.getMatrix()
    cp = lattice.controlPoints
    for i in range(cp.numElements()):
        attr = cp.elementByLogicalIndex(i)
        x = attr.xValue.get()
        y = attr.yValue.get()
        z = attr.zValue.get()
        pt = dt.Point(x, y, z) * matrix
        pos_list.append(pt.totuple())

    return pm.polyCreateFacet(p=pos_list)


def move_lattice_point(mesh, lattice):
    pm.undoInfo(ock=1)
    lattice.nodeState.set(2)
    transform = lattice.getParent()
    matrix = transform.getMatrix()
    cp = lattice.controlPoints
    for i in range(cp.numElements()):
        pos = mesh.vtx[i].getPosition(space="world")
        pt = dt.Point(*pos) * matrix.inverse()
        attr = cp.elementByLogicalIndex(i)
        attr.xValue.set(pt.x)
        attr.yValue.set(pt.y)
        attr.zValue.set(pt.z)
    lattice.nodeState.set(0)
    pm.undoInfo(cck=1)


# def create_lattice_mesh():

#     pos_list = []
#     for lattice in pm.ls(sl=1,dag=1,type="lattice"):
#         transform = lattice.getParent()
#         matrix = transform.getMatrix()
#         cp = lattice.controlPoints
#         for i in range(cp.numElements()):
#             attr = cp.elementByLogicalIndex(i)
#             x = attr.xValue.get()
#             y = attr.yValue.get()
#             z = attr.zValue.get()
#             pt = dt.Point(x,y,z) * matrix
#             pos_list.append(pt.totuple())

#     return pm.polyCreateFacet(p=pos_list)

# def move_lattice_point(mesh):
#     pm.undoInfo(ock=1)
#     for lattice in pm.ls(sl=1,dag=1,type="lattice"):
#         lattice.nodeState.set(2)
#         transform = lattice.getParent()
#         matrix = transform.getMatrix()
#         cp = lattice.controlPoints
#         for i in range(cp.numElements()):
#             pos = mesh.vtx[i].getPosition(space="world")
#             pt = dt.Point(*pos) * matrix.inverse()
#             attr = cp.elementByLogicalIndex(i)
#             attr.xValue.set(pt.x)
#             attr.yValue.set(pt.y)
#             attr.zValue.set(pt.z)
#         lattice.nodeState.set(0)
#     pm.undoInfo(cck=1)

if __name__ == "__main__":
    # create_lattice_mesh()
    mesh = pm.PyNode("polySurface2")
    move_lattice_point(mesh)
