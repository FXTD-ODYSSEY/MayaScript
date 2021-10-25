# -*- coding: utf-8 -*-
"""
获取选中骨骼层级靠得过近的骨骼
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-10-16 12:39:32"


import pymel.core as pm
import pymel.core.datatypes as dt


def get_closest_jnt(jnt_list, thresold=0.2):

    jnt_dict = {}
    jnt_list = jnt_list[:]
    for src_jnt in jnt_list[:]:
        jnt_list.remove(src_jnt)
        src_pt = dt.Point(pm.xform(src_jnt, q=1, ws=1, t=1))
        distance = 9999
        target_jnt = None
        for dst_jnt in jnt_list:
            dst_pt = dt.Point(pm.xform(dst_jnt, q=1, ws=1, t=1))
            dist = (dst_pt - src_pt).length()
            if dist < distance:
                distance = dist
                target_jnt = dst_jnt

        if distance < thresold:
            jnt_dict[src_jnt] = target_jnt
    return jnt_dict


if __name__ == "__main__":
    jnt_list = pm.ls(sl=1, dag=1, type="joint")
    get_closest_jnt(jnt_list)
