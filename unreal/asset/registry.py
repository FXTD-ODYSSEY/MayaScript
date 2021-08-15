# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-10 16:30:14'


# import unreal
# asset_tool = unreal.AssetToolsHelpers.get_asset_tools()
# asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
# path = '/Game/ArtResources/Characters/Roles/Actor/Sanji01/BluePrints/Actor/90065_A.90065_A'
# data = asset_registry.get_asset_by_object_path(path)

# print(data.is_u_asset())
# print(data.is_valid())

import unreal

asset_reg = unreal.AssetRegistryHelpers.get_asset_registry()
path ='/Game/ArtResources/Characters/Roles/Actor/Mihawk01/Combine'
# NOTE 罗列出关联的 physic
kwargs = {"class_names": ["PhysicsAsset"], "package_paths": [path],'recursive_paths':True}
for data in asset_reg.get_assets(unreal.ARFilter(**kwargs)):
    print(data.object_path)
    
    