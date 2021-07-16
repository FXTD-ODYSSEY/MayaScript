# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-20 10:08:56'

""" 
获取曲线 ControlPoint 的位置
"""

import pymel.core as pm

if __name__ == "__main__":
    jnt_list = pm.ls(sl=1,type="joint")
    crv = pm.curve( p=[jnt.getTranslation() for jnt in jnt_list])
    pm.closeCurve(crv,ch=0,rpo=1) 

    info = pm.createNode("curveInfo")
    crv.worldSpace[0].connect(info.inputCurve)

    for i,jnt in enumerate(jnt_list):
        loc = pm.spaceLocator(n="%s_loc"%jnt)
        loc.setParent(crv)
        loc.v.set(0)
        info.controlPoints[i].connect(loc.t)
        grp = pm.group(jnt,n="%s_crv_loc"%jnt)
        pm.parentConstraint(loc,grp,mo=1)
