# -*- coding: utf-8 -*-
"""
select the `dly_chr_lucky_body_rig_v017_OF:spine_04` then run the script
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-09-06 14:16:36"

import pymel.core as pm

src_ns = ""
dst_ns = "dly_chr_lucky_rig_OF_body:"

for src_jnt in pm.ls(sl=1, dag=1, type="joint"):
    dst_jnt = src_jnt.split("|")[-1]
    # dst_jnt = dst_jnt.replace(src_ns, dst_ns)
    dst_jnt = dst_ns + dst_jnt
    print(dst_jnt)
    if not pm.objExists(dst_jnt) or dst_jnt == src_jnt:
        continue
    # print(src_jnt,dst_jnt)
    pm.parentConstraint(src_jnt, dst_jnt)
    # pm.scaleConstraint(src_jnt, dst_jnt)
