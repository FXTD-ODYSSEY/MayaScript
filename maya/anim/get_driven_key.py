# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-08-18 17:30:44'

import pymel.core as pm

anim_crv = pm.PyNode("pSphere1_translateX")
for key in range(anim_crv.numKeys()):
    time = anim_crv.getTime(key)
    # time = pm.keyframe(anim_crv,q=1,floatChange=1)
    print(time * 24)
    # print(type(time))
    print(dir(time))
    
    

