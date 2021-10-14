# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-10-13 16:52:52'

import pymel.core as pm


for jnt in pm.ls(sl=1,dag=1,type="joint"):
    jnt.jointOrientX.set(0)
    jnt.jointOrientY.set(0)
    jnt.jointOrientZ.set(0)
    