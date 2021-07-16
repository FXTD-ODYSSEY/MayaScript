# -*- coding: utf-8 -*-
"""
bake 的动画关键帧，找到关键帧静止的部分进行移除
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-01-07 23:35:54'


import pymel.core as pm

jnt_list = [
    u'Skel_90001_L_rig:root',
    u'Skel_90001_L_rig:spline1_jnt_skin',
    u'Skel_90001_L_rig:Lf_Leg1_jnt_skin',
    u'Skel_90001_L_rig:Lf_Leg6_jnt_skin',
    u'Skel_90001_L_rig:Lf_Leg9_jnt_skin',
    u'Skel_90001_L_rig:Rt_Leg1_jnt_skin',
    u'Skel_90001_L_rig:Rt_Leg6_jnt_skin',
    u'Skel_90001_L_rig:Rt_Leg9_jnt_skin',
    u'Skel_90001_L_rig:spline3_jnt_skin',
    u'Skel_90001_L_rig:spline5_jnt_skin',
    u'Skel_90001_L_rig:Lf_clavicle1_jnt_skin',
    u'Skel_90001_L_rig:Lf_Arm1_jnt_skin',
    u'Skel_90001_L_rig:Lf_Arm6_jnt_skin',
    u'Skel_90001_L_rig:Lf_Arm9_jnt_skin',
    u'Skel_90001_L_rig:Rt_clavicle1_jnt_skin',
    u'Skel_90001_L_rig:Rt_Arm1_jnt_skin',
    u'Skel_90001_L_rig:Rt_Arm6_jnt_skin',
    u'Skel_90001_L_rig:Rt_Arm9_jnt_skin',
    u'Skel_90001_L_rig:neck1_jnt1_skin',
    u'Skel_90001_L_rig:head_jnt_skin',
]
# jnt_crv = {jnt:jnt.history(type="animCurve") for jnt in pm.ls(jnt_list)}
# jnt_crv_list = [jnt.history(type="animCurve") for jnt in pm.ls('Skel_90001_L_rig:root',dag=1,type="joint")]
jnt_crv_list = [jnt.history(type="animCurve") for jnt in pm.ls(jnt_list)]
env = pm.Env()
frame_range = env.getTime()
frame_start = env.getMinTime()

range_list = []
for curr_frame in range(int(frame_range)):
    next_frame = curr_frame + 1
    for crv_list in jnt_crv_list:
        for crv in crv_list:
            curr_value = crv.getValue(curr_frame)
            next_value = crv.getValue(next_frame)
            # NOTE 用不等于存在轻微的数值误差
            if not -0.001 < (curr_value - next_value) < 0.001:
                break
        else:
            continue
        break
    else:
        curr_frame += frame_start
        next_frame += frame_start
        # NOTE 跳转到这里说明下一帧一样
        if len(range_list) == 0:
            range_list.append({"start":curr_frame,"end":next_frame,"flag":False})
        else:
            ran = range_list[-1]
            if ran["flag"]:
                range_list.append({"start":curr_frame,"end":next_frame,"flag":False})
            else:
                ran["end"] = next_frame
                
        continue
    
    # NOTE 跳转到这里说明下一帧不一样
    if len(range_list) > 0:
        ran = range_list[-1]
        if not ran["flag"]:
            ran["flag"] = True

[ran.pop("flag") for ran in range_list]
print(range_list)