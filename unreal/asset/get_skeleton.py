# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-08-09 15:36:57"


import unreal
(skeleton,) = unreal.EditorUtilityLibrary.get_selected_assets()
for bone in skeleton.get_editor_property('bone_tree'):
    print(bone)