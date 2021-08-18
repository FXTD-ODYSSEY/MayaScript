# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-17 19:02:48'

import unreal
render_lib = unreal.RenderingLibrary
level_lib = unreal.EditorLevelLibrary

material_path = '/Game/Test/NewFolder9/NewMaterial.NewMaterial'
rt_path = '/Game/Test/NewFolder9/NewTextureRenderTarget2D.NewTextureRenderTarget2D'


material = unreal.load_asset(material_path)
rt = unreal.load_asset(rt_path)


world = level_lib.get_editor_world()
render_lib.draw_material_to_render_target(world,rt,material)
