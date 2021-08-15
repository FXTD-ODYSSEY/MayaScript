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
red_lib = unreal.RedArtToolkitBPLibrary
(physic,) = unreal.EditorUtilityLibrary.get_selected_assets()
setups = red_lib.get_physics_asset_skeletal_body_setup(physic)
for setup in setups:
    bone = setup.get_editor_property("bone_name")
    if bone == "root":
        setup.set_editor_property('consider_for_bounds',False)