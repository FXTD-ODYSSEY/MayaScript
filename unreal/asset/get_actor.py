# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-10 21:06:49'

import unreal
level_lib = unreal.EditorLevelLibrary
world = level_lib.get_editor_world()
world_path = world.get_path_name()
actors = level_lib.get_selected_level_actors()
for actor in actors:
    name = actor.get_name()
    path = actor.get_path_name()
    _actor = unreal.load_object(None,path)
    print(_actor)
    level_lib.set_selected_level_actors([_actor])
    # prefix = "%s:PersistentLevel" % world_path
    # if str(path).startswith(prefix):
    #     print(path)
