# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-23 19:23:58'

import pymel.core as pm

mesh = pm.ls(sl=1)[0]

skin = mesh.history(type="skinCluster")[0]

pm.select(skin.inputs(type="joint"))
