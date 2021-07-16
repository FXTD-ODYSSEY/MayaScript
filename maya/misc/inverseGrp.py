# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-25 20:58:42'

"""
生成抵消位移组
"""

import pymel.core as pm

def inverseGrp(objType="nurbsCurve"):
        
    sel_list = pm.ls(sl=1,dag=1,ni=1,type=objType)

    for sel in sel_list:
        if hasattr(sel,"getTransform"):
            sel = sel.getTransform()
        grp = pm.group(sel,n="%s_inverse"%sel)
        node = pm.createNode("multiplyDivide",n="%s_inverse_mul"%sel)
        node.input2X.set(-1)
        node.input2Y.set(-1)
        node.input2Z.set(-1)
        sel.t.connect(node.input1)
        node.output.connect(grp.t)

if __name__ == "__main__":
    inverseGrp()