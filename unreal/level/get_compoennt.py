# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-18 16:46:57'

import unreal
from Qt import QtCore
mesh= unreal.load_asset('/Game/Test/NewFolder9/aaa_magellan002_body_d1.aaa_magellan002_body_d1')
m = unreal.load_asset('/Game/Test/NewFolder9/M_UVCapture_Inst.M_UVCapture_Inst')
override_materials  = [m]
for actor in unreal.EditorLevelLibrary.get_selected_level_actors():
    comp = actor.get_editor_property("static")
    # materials = comp.get_editor_property("override_materials")
    comp.set_editor_property("static_mesh",mesh)
    comp = actor.get_editor_property("static")
    comp.set_editor_property("override_materials",override_materials)