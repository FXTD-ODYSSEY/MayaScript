# -*- coding: utf-8 -*-
"""
自动对称模型顶点
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-08-11 19:43:31'

from maya import cmds
from maya import OpenMaya
import pymel.core as pm
import pymel.core.datatypes as dt

def main(thersold = 0.01):
        
    # NOTE 选择模型
    pm.pickWalk(d="down")
    for sel in pm.ls(sl=1,type="mesh"):
        bbox = pm.exactWorldBoundingBox(sel)
        x = (bbox[0] + bbox[3])/2
        y = (bbox[1] + bbox[4])/2
        z = (bbox[2] + bbox[5])/2
        pt = OpenMaya.MPoint(x, y, z)
        
        node = sel.node()
        itr = OpenMaya.MItMeshVertex(node.__apimdagpath__())

        l_dict = {}
        c_dict = {}
        r_dict = {}
        while not itr.isDone():
            pt_pos = itr.position(OpenMaya.MSpace.kWorld)
            pt_idx = itr.index()
            pt_x = pt_pos.x
            if pt_x - x > 0 :
                l_dict[pt_idx] = pt_pos
            elif abs(pt_x - x) < thersold:
                c_dict[pt_idx] = pt_pos
            else:
                r_dict[pt_idx] = pt_pos
            itr.next()
        
        match_dict = {}
        for l_idx,l_pos in l_dict.items():
            l_len = (pt - l_pos).length()
            l_len_x = abs(l_pos.x - x)
            for r_idx,r_pos in r_dict.items():
                r_len = (pt - r_pos).length()
                r_len_x = abs(r_pos.x - x)
                if abs(l_len - r_len) < thersold and abs(l_len_x - r_len_x) < thersold :
                    match_dict[l_idx] = r_idx
                    break
        
        for l,r in match_dict.items():
            l_pos = sel.vtx[l].getPosition()
            sel.vtx[r].setPosition(dt.Point(-l_pos.x , l_pos.y , l_pos.z))


if __name__ == "__main__":
    main()