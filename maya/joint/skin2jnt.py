# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-23 19:23:58'

import pymel.core as pm

mesh_list = pm.ls(pm.pickWalk(d="down"),type="mesh")

jnt_list = {jnt for mesh in mesh_list for skin in mesh.history(type="skinCluster") for jnt in skin.inputs(type="joint")}
    
pm.select(jnt_list)
