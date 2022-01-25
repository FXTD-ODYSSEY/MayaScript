# -*- coding: utf-8 -*-
"""
选中材质实例执行

src_attr 复制材质源的颜色属性
dst_attrs 粘贴颜色到对应的属性上
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-01-20 10:02:33'

# Import local modules
import unreal
from unreal import MaterialEditingLibrary as mat_lib

src_attr = "Param"
dst_attrs = ["color1","color2"]

def main():
    
    vector_getter = mat_lib.get_material_instance_vector_parameter_value
    vector_setter = mat_lib.set_material_instance_vector_parameter_value

    # NOTES(timmyliang): 获取选中的资产
    assets = unreal.EditorUtilityLibrary.get_selected_assets()
    
    for material in assets:
        if not isinstance(material, unreal.MaterialInstance):
            continue
        value = vector_getter(material,src_attr)
        for dst_attr in dst_attrs:
            vector_setter(material,dst_attr,value)

if __name__ == '__main__':
    main()
