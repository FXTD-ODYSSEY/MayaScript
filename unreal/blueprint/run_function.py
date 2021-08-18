# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-18 19:44:01'

import unreal



bp, = unreal.EditorUtilityLibrary.get_selected_assets()
bp_path = bp.get_path_name()
gc = unreal.load_object(None, "%s_C" % bp_path)
cdo = unreal.get_default_object(gc)

cdo.call_method("TestCall",args=(unreal.World(),))



