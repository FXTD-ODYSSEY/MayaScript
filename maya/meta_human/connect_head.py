# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-08-19 10:32:32'

import os
import pymel.core as pm


for jnt in pm.ls(sl=1,dag=1,type='joint'):
    head_jnt = jnt.replace(jnt.namespace(),'lucky_facegood_rig:') 
    if pm.objExists(head_jnt):
        pm.parentConstraint(jnt,head_jnt,mo=0)
