# -*- coding: utf-8 -*-
"""
重置顶点位置
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-11-19 10:40:55"

import pymel.core as pm
import pymel.core.nodetypes as nt
from maya import OpenMaya

def iter_verts(mesh):
    obj = mesh.__apimobject__()
    itr = OpenMaya.MItMeshVertex(obj)
    while not itr.isDone():
        yield itr.index()
        itr.next()


def main():
        
    selections = pm.ls(sl=1,fl=1)

    if not selections:
        return

    sel = selections[0]
    if hasattr(sel, 'getShape'):
        sel = sel.getShape()
    
    if isinstance(sel, nt.Mesh):
        selections = iter_verts(sel)
        mesh = sel
    elif isinstance(sel, pm.MeshVertex):
        selections = [v.index() for v in selections]
        mesh = sel.node()
    else:
        return
    
    pm.undoInfo(ock=1)
    for index in selections:
        mesh.pnts[index].pntx.set(0)
        mesh.pnts[index].pnty.set(0)
        mesh.pnts[index].pntz.set(0)

    pm.undoInfo(cck=1)

if __name__ == "__main__":
    main()