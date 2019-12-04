# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-25 15:24:13'

"""
ungroup joint
"""

import pymel.core as pm


def ungroupParent(objType="joint"):
    
    curr_sel = pm.ls(sl=1)

    for sel in pm.ls(sl=1,dag=1,ni=1,type=objType):
        if type(sel)  == pm.nodetypes.Joint:
            grp = sel.getParent()
        else:
            grp = sel.getParent().getParent()
        pm.ungroup(grp)
    
    pm.select(curr_sel)

if __name__ == "__main__":
    ungroupParent("nurbsCurve")