# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-16 16:51:39'

"""

"""

import maya.cmds as mc
def csl_quaternionSlerp():
    selectCtrls = mc.ls(sl=1,l=1)
    for selectCtrl in selectCtrls:
        selectCtrlAttrs = mc.keyframe(selectCtrl,query=True,name=True)
        if selectCtrlAttrs==None:
            mc.error(u'【所选物体无动画曲线】=='+selectCtrl)
        else:
            for selectCtrlAttr in selectCtrlAttrs:
                if "_rotate" in selectCtrlAttr:
                    mc.rotationInterpolation( selectCtrlAttr, convert='quaternionSlerp' )
                    print(u'==【成功转为四元数】=='+selectCtrlAttr)
csl_quaternionSlerp()