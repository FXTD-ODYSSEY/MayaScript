# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-08-17 21:06:24"

import unreal

level_lib = unreal.EditorLevelLibrary
sys_lib = unreal.SystemLibrary
actors = level_lib.get_all_level_actors()

# NOTE 隐藏所有 Actor
vis_dict = {}
for actor in actors:
    vis = actor.is_temporarily_hidden_in_editor()
    vis_dict[actor] = vis
    actor.set_is_temporarily_hidden_in_editor(True)
    

# for actor,vis in vis_dict.items():
#     actor.set_is_temporarily_hidden_in_editor(vis)
    
    