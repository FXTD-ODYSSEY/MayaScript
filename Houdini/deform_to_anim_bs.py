# -*- coding: utf-8 -*-
"""
convert fx to blendshape deform
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-23 22:27:39'


import hou

total = 120
bs = hou.node("/obj/geo1/blendshapes1")
bs.parm("nblends").set(total)

mountain = hou.node("/obj/geo1/mountain1")
geo = bs.parent()

for i in range(1, total):
    timeshift = geo.createNode("timeshift")
    frame = timeshift.parm("frame")
    frame.deleteAllKeyframes()
    frame.set(i)
    timeshift.setInput(0, mountain)
    bs.setInput(i, timeshift)

    blend = bs.parm("blend%s" % i)
    blend.deleteAllKeyframes()
    hou_keyframe = hou.Keyframe()
    hou_keyframe.setFrame(i - 1)
    hou_keyframe.setValue(0)
    hou_keyframe.setExpression("constant()")
    blend.setKeyframe(hou_keyframe)
    hou_keyframe = hou.Keyframe()
    hou_keyframe.setFrame(i)
    hou_keyframe.setValue(1)
    hou_keyframe.setExpression("constant()")
    blend.setKeyframe(hou_keyframe)
    hou_keyframe = hou.Keyframe()
    hou_keyframe.setFrame(i + 1)
    hou_keyframe.setValue(0)
    hou_keyframe.setExpression("constant()")
    blend.setKeyframe(hou_keyframe)
