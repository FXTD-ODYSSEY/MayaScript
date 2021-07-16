# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 11:00:04'

"""
通过上层级遍历下层级所有的指定类型
"""

import pymel.core as pm


def selectShape(objType="nurbsCurve"):
        
    sel_list = pm.ls(sl=1,dag=1,ni=1,type=objType)
    pm.select(sel_list)

if __name__ == "__main__":
    selectShape()

