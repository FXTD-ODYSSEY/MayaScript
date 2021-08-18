# -*- coding: utf-8 -*-
"""
https://blender.stackexchange.com/questions/58202/how-can-i-import-an-addon-into-a-blender-script
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-17 14:19:08'

import bpy
from addon_utils import check, paths, enable
enable("space_view3d_copy_attributes")
def get_all_addons(display=False):
    """
    Prints the addon state based on the user preferences.
    """
    paths_list = paths()
    addon_list = []
    for path in paths_list:
        for mod_name, mod_path in bpy.path.module_names(path):
            is_enabled, is_loaded = check(mod_name)
            addon_list.append(mod_name)
            if display:  #for example
                print("%s default:%s loaded:%s " % (mod_name, is_enabled, is_loaded))                
    return(addon_list)
#print all the addons and show if enabled and default
addons = get_all_addons(True)


['add_camera_rigs', 'add_curve_extra_objects', 'add_curve_ivygen', 'add_curve_sapling', 'add_mesh_BoltFactory', 'add_mesh_discombobulator', 'add_mesh_extra_objects', 'add_mesh_geodesic_domes', 'amaranth', 'animation_add_corrective_shape_key', 'animation_animall', 'ant_landscape', 'archimesh', 'archipack', 'blender_id', 'blenderkit', 'bone_selection_sets', 'btrace', 'camera_turnaround', 'curve_assign_shapekey', 'curve_simplify', 'curve_tools', 'cycles', 'depsgraph_debug', 'development_edit_operator', 'development_icon_get', 'development_iskeyfree', 'greasepencil_tools', 'io_anim_bvh', 'io_anim_camera', 'io_anim_nuke_chan', 'io_coat3D', 'io_curve_svg', 'io_export_dxf', 'io_export_paper_model', 'io_export_pc2', 'io_import_BrushSet', 'io_import_dxf', 'io_import_images_as_planes', 'io_import_palette', 'io_mesh_atomic', 'io_mesh_ply', 'io_mesh_stl', 'io_mesh_uv_layout', 'io_scene_fbx', 'io_scene_gltf2', 'io_scene_obj', 'io_scene_x3d', 'io_shape_mdd', 'lighting_dynamic_sky', 'lighting_tri_lights', 'magic_uv', 'materials_library_vx', 'materials_utils', 'measureit', 'mesh_auto_mirror', 'mesh_bsurfaces', 'mesh_f2', 'mesh_inset', 'mesh_looptools', 'mesh_snap_utilities_line', 'mesh_tiny_cad', 'mesh_tissue', 'mesh_tools', 'node_arrange', 'node_presets', 'node_wrangler', 'object_boolean_tools', 'object_carver', 'object_collection_manager', 'object_color_rules', 'object_edit_linked', 'object_fracture_cell', 'object_print3d_utils', 'object_scatter', 'object_skinify', 'paint_palette', 'power_sequencer', 'precision_drawing_tools', 'real_snow', 'render_auto_tile_size', 'render_copy_settings', 'render_freestyle_svg', 'render_povray', 'render_ui_animation_render', 'rigify', 'space_clip_editor_refine_solution', 'space_view3d_3d_navigation', 'space_view3d_align_tools', 'space_view3d_brush_menus', 'space_view3d_copy_attributes', 'space_view3d_math_vis', 'space_view3d_modifier_tools', 'space_view3d_pie_menus', 'space_view3d_spacebar_menu', 'space_view3d_stored_views', 'sun_position', 'system_blend_info', 'system_demo_mode', 'system_property_chart', 'ui_translate', 'viewport_vr_preview', 'screencast_keys', 'send2ue', 'ue2rigify']


