# -*- coding: utf-8 -*-
"""
http://forum.mgear-framework.com/t/python/802/3
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-09-27 16:17:44"

import json
from collections import defaultdict

import pymel.core as pm
from mgear.shifter import guide
from mgear.core import string

r = guide.Rig()


def draw_component(jnt,guide_grp=None):
    if not guide_grp and pm.objExists("guide"):
        guide_grp = pm.PyNode("guide")
    r.drawNewComponent(guide_grp, "control_01", False)
    matrix = jnt.getMatrix(worldSpace=1)
    comp = pm.ls(sl=1)[0]
    pm.xform(comp, ws=1, m=matrix)

    # NOTES(timmyliang) 
    comp.joint.set(True)
    comp.uniScale.set(True)
    comp.neutralRotation.set(False)
    comp.ctlSize.set(0.2)

    name = jnt.split("|")[-1]
    itr = iter(name.split("_"))
    _ = next(itr, "")
    name = next(itr, "")
    index = next(itr, "")
    side = next(itr, "")

    name = string.normalize2(name)
    side = "C" if side == "M" else side

    r.updateProperties(comp, name, side, int(index) if index else 0)

    return comp


def create_ctrl_tree(joints):
    joints = joints if isinstance(joints, list) else [joints]
    for jnt in joints:
        jnt = pm.PyNode(jnt)
        parent_comp = draw_component(jnt)
        for child in jnt.getChildren(type="joint"):

            if child.getChildren(type="joint"):
                create_ctrl_tree(child)
            else:
                comp = draw_component(child)
                comp.setParent(parent_comp)
            
def main():

    # create_ctrl_tree(pm.ls(sl=1))
    for sel in pm.ls(sl=1,dag=1):
        if hasattr(sel,"neutralRotation"):
            getattr(sel,"neutralRotation").set(False)

if __name__ == "__main__":
    main()

