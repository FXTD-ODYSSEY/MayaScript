# -*- coding: utf-8 -*-
"""
选中材质执行

"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-01-20 10:02:33"

# Import local modules
import unreal
from unreal import MaterialEditingLibrary as mat_lib

MP_OPACITY = unreal.MaterialProperty.MP_OPACITY
BLEND_TRANSLUCENT = unreal.BlendMode.BLEND_TRANSLUCENT

# for material in unreal.EditorUtilityLibrary.get_selected_assets():
#     if not isinstance(material,unreal.Material):
#         continue

#     blend_mode = material.get_editor_property("blend_mode")
#     if blend_mode != BLEND_TRANSLUCENT:
#         continue

#     # NOTE 这个是 第二个贴图节点
#     material_path = material.get_full_name().split(' ')[-1]
# path = "%s:MaterialExpressionTextureSample_1" % material_path
#     texture = unreal.load_object(None,path)
#     if not texture:
#         print("texture None : %s" % material_path)
#         continue

#     mat_lib.connect_material_property(texture, "A", MP_OPACITY)
#     unreal.MaterialEditingLibrary.recompile_material(material)


def main():

    vector_getter = mat_lib.get_material_instance_vector_parameter_value
    vector_setter = mat_lib.set_material_instance_vector_parameter_value

    # NOTES(timmyliang): 获取选中的资产
    assets = unreal.EditorUtilityLibrary.get_selected_assets()

    for material in assets:
        if not isinstance(material, unreal.Material):
            continue

        # num = mat_lib.get_num_material_expressions(material)
        names = mat_lib.get_vector_parameter_names(material)
        material_path = material.get_path_name()
        for index, name in enumerate(names):
            path = "{0}:MaterialExpressionVectorParameter_{1}".format(
                material_path, index
            )
            vector_node = unreal.load_object(None, path)
            
            function_node = mat_lib.create_material_expression(
                material, unreal.MaterialExpressionMaterialFunctionCall
            )
            vector_node.get_editor_property("MaterialExpressionEditorX")

            print(vector_node.get_editor_property("parameter_name"))

        mat_lib.recompile_material(material)
        mat_lib.layout_material_expressions(material)


if __name__ == "__main__":
    main()
