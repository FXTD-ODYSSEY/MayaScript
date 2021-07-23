# -*- coding: utf-8 -*-
"""
设置 skeletalmesh 的 reduction 属性
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-07-19 21:24:27'


import unreal

# NOTES(timmyliang) 选择一个模型修改
(mesh,) = unreal.EditorUtilityLibrary.get_selected_assets()
infos = mesh.get_editor_property("lod_info")
info = infos[0]
reduction_settings = info.get_editor_property("reduction_settings")

verts = unreal.SkeletalMeshTerminationCriterion.SMTC_NUM_OF_VERTS
# NOTES(timmyliang) 修改 Termination Criterion 为 vertices
reduction_settings.set_editor_property("termination_criterion",verts)
# NOTES(timmyliang) 
reduction_settings.set_editor_property("num_of_vert_percentage",0.2)

info.set_editor_property("reduction_settings",reduction_settings)
infos[0] = info
mesh.set_editor_property("lod_info",infos)



