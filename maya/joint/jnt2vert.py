# -*- coding: utf-8 -*-
"""
选中骨骼获取蒙皮影响的顶点
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-10-16 10:07:00"

from collections import defaultdict
import pymel.core as pm



def get_jnt_weight(skin):
    jnt_vertex_dict = defaultdict(set)
    jnt_list = skin.getInfluence()
    mesh = skin.listConnections(type="mesh")[0]
    for i, weights in enumerate(skin.getWeights(mesh)):
        for jnt, weight in zip(jnt_list, weights):
            if weight > 0.01:
                jnt_vertex_dict[jnt].add("%s.vtx[%i]" % (mesh, i))

    return jnt_vertex_dict


def main():

    jnt_list = pm.ls(sl=1, type="joint")
    if not jnt_list:
        pm.warning("please select a joint")
        return

    skin_dict = defaultdict(set)
    for jnt in jnt_list:
        itr = iter(jnt.listConnections(type="skinCluster"))
        skin = next(itr, None)
        if not skin:
            pm.warning("skin cluster not found -> skip [%s]" % jnt)
            continue
        skin_dict[skin].add(jnt)

    vertices = set()
    for skin, joints in skin_dict.items():
        jnt_vertex_dict = get_jnt_weight(skin)
        for jnt in joints:
            vertices.update(jnt_vertex_dict.get(jnt, set()))

    pm.select(vertices)


if __name__ == "__main__":
    main()

