# -*- coding: utf-8 -*-
"""
返回材质中所有的 MaterialExpression

"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-01-20 10:02:33"

# Import local modules
from collections import defaultdict
import unreal
from unreal import MaterialEditingLibrary as mat_lib

MP_OPACITY = unreal.MaterialProperty.MP_OPACITY
BLEND_TRANSLUCENT = unreal.BlendMode.BLEND_TRANSLUCENT


def main():

    expression_count = {
        cls.__name__:10 for cls in unreal.MaterialExpression.__subclasses__()
    }
    expression_count.update({
        "MaterialExpressionMultiply":100,
        "MaterialExpressionLinearInterpolate":100,
    })
    for material in unreal.EditorUtilityLibrary.get_selected_assets():
        if not isinstance(material, unreal.Material):
            continue
        data = defaultdict(list)
        material_path = material.get_path_name()

        for expression_type,count in expression_count.items():
            for index in range(count):
                path = "{0}:{typ}_{index}".format(
                    material_path, index=index, typ=expression_type
                )
                expression = unreal.load_object(None, path)
                if expression:
                    data[expression_type].append(path)

        print(dict(data))


if __name__ == "__main__":
    main()
