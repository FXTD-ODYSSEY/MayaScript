# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-02 09:18:32'

"""
让曲线的性状节点与父节点名称保持一致（后缀加Shape）
"""

import pymel.core as pm

for crv in pm.ls(type="nurbsCurve"):
    parent = crv.getParent()
    crv_name = str(parent) + "Shape"
    if crv_name != str(crv):
        crv.rename(crv_name)
