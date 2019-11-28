# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 10:41:51'

"""
获取选择的中心位置
"""

import pymel.core as pm
import pymel.core.datatypes as dt


def getCenter(objType="nurbsCurve"):
        
    sel_list = pm.ls(sl=1,dag=1,ni=1,type=objType)
    box = dt.BoundingBox()

    for sel in sel_list:

        if not hasattr(sel,"boundingBox"):
            continue
        
        point = sel.boundingBox().center()
        box.expand(point)
        
    loc = pm.spaceLocator()
    loc.t.set(box.center())

if __name__ == "__main__":
    getCenter()

