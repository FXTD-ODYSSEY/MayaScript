# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-14 21:00:30'

"""
选择物体位置生成 locator
"""

import pymel.core as pm

for sel in pm.selected():
    pos = pm.xform(sel,q=1,t=1,ws=1)
    loc = pm.spaceLocator()
    pm.xform(loc,t=pos,ws=1)