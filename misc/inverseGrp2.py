# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-25 20:58:42'

"""
生成抵消位移组
"""

import pymel.core as pm


def inverseGrp(objType="nurbsCurve",controller=""):
        
    sel_list = pm.ls(sl=1,dag=1,ni=1,type=objType)
    if not pm.objExists(controller):
        controller = ""

    for sel in sel_list:
        if hasattr(sel,"getTransform"):
            sel = sel.getTransform()
        inverse = pm.group(sel,n="%s_inverse"%sel)
        mul = pm.createNode("multiplyDivide",n="%s_inverse_mul"%sel)
        mul.input2X.set(-1)
        mul.input2Y.set(-1)
        mul.input2Z.set(-1)
        sel.t.connect(mul.input1)
        mul.output.connect(inverse.t)

        if not controller:
            continue

        offset = pm.group(inverse,n="%s_ofst"%sel)

        pm.parentConstraint(controller,offset,mo=1)

if __name__ == "__main__":
    inverseGrp(controller="Controller_Move")