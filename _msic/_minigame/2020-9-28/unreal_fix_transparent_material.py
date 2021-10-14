# -*- coding: utf-8 -*-
"""
修复 unreal 导入的材质 opacity 连接错误的修正
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-28 08:40:07'

import unreal

mat_lib = unreal.MaterialEditingLibrary()
MP_OPACITY = unreal.MaterialProperty.MP_OPACITY
BLEND_TRANSLUCENT = unreal.BlendMode.BLEND_TRANSLUCENT

for material in unreal.EditorUtilityLibrary.get_selected_assets():
    if not isinstance(material,unreal.Material):
        continue

    blend_mode = material.get_editor_property("blend_mode")
    if blend_mode != BLEND_TRANSLUCENT:
        continue
    
    # NOTE 这个是 第二个贴图节点 
    material_path = material.get_full_name().split(' ')[-1]
    path = "%s:MaterialExpressionTextureSample_1" % material_path
    texture = unreal.load_object(None,path)
    if not texture:
        print("texture None : %s" % material_path)
        continue
    
    mat_lib.connect_material_property(texture, "A", MP_OPACITY)
    unreal.MaterialEditingLibrary.recompile_material(material)
