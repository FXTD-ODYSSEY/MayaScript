# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-07-21 14:27:14'


import unreal
bp, = unreal.EditorUtilityLibrary.get_selected_assets()
bp_gc = unreal.load_object(None,"%s_C" % bp.get_path_name())
bp_cdo = unreal.get_default_object(bp_gc)

print(bp_cdo.get_class().get_outer().get_name())
