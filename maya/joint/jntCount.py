# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-30 20:59:07'

"""
计算选中下骨骼下的所有骨骼的数量
"""

from maya import cmds

print (len(cmds.ls(sl=1,dag=1,ni=1,type="joint")))