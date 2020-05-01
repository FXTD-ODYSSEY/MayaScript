# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-30 20:59:07'

"""
删除选中物体下所有的约束节点
"""

from maya import cmds

for con in cmds.ls(sl=1,dag=1,ni=1,type="constraint"):
    cmds.delete(con)