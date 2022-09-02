# -*- coding: utf-8 -*-
"""
需要开启 auto keyframe
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-08-25 15:23:50'


import pymel.core as pm
from mgear.core import anim_utils

env = pm.Env()

max_time = env.getMaxTime()
min_time = env.getMinTime()

namespace = "dly_chr_lucky_body_rig_v017_OF"

r_control = pm.PyNode(f"{namespace}:armUI_R0_ctl")
l_control = pm.PyNode(f"{namespace}:armUI_L0_ctl")
for frame in range(int(min_time), int(max_time) + 1):
    print(frame)
    pm.currentTime(frame)
    r_control.arm_blend.set(0)
    l_control.arm_blend.set(0)
    anim_utils.ikFkMatch(
        f"{namespace}:rig",
        "arm_blend",
        f"{namespace}:armUI_R0_ctl",
        [f"{namespace}:arm_R0_fk0_ctl", f"{namespace}:arm_R0_fk1_ctl", f"{namespace}:arm_R0_fk2_ctl"],
        f"{namespace}:arm_R0_ik_ctl",
        f"{namespace}:arm_R0_upv_ctl",
    )
    anim_utils.ikFkMatch(
        f"{namespace}:rig",
        "arm_blend",
        f"{namespace}:armUI_L0_ctl",
        [f"{namespace}:arm_L0_fk0_ctl", f"{namespace}:arm_L0_fk1_ctl", f"{namespace}:arm_L0_fk2_ctl"],
        f"{namespace}:arm_L0_ik_ctl",
        f"{namespace}:arm_L0_upv_ctl",
    )
    # if frame > 200:
    #     break
