# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-10 16:50:48'

import unreal
level_lib = unreal.EditorLevelLibrary
comps = level_lib.get_all_level_actors_components()
world = level_lib.get_editor_world()
print(world.get_outer().get_path_name())

        
threshold = 0.1
for comp in comps:
    if not isinstance(comp,unreal.PrimitiveComponent):
        continue
    scale = comp.get_editor_property("bounds_scale")
    if scale - 1 > threshold:
        level_lib.set_selected_level_actors([comp.get_outer()])
        print(comp.get_outer())

        # scomp.set_editor_property("bounds_scale",1)
