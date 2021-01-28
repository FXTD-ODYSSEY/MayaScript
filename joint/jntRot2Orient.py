# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-01-18 11:05:38'

import pymel.core as pm

# NOTE 选择根骨骼自动遍历下面所有的子骨骼
jnt_list = pm.ls(sl=1,dag=1,ni=1,type="joint")
for jnt in jnt_list:
    r = jnt.r.get()
    jnt.jointOrient.set(r)
    jnt.r.set(0,0,0)