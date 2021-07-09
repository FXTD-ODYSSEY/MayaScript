# -*- coding: utf-8 -*-
"""
list asset dependencies
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-07-08 11:26:32'

import unreal
asset_lib = unreal.EditorAssetLibrary
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

def ls_dependencies(path):
    data = asset_lib.find_asset_data(path)
    options = unreal.AssetRegistryDependencyOptions()
    dependencies = asset_registry.get_dependencies(data.package_name, options)
    return dependencies

def ls_referencers(path):
    data = asset_lib.find_asset_data(path)
    options = unreal.AssetRegistryDependencyOptions()
    dependencies = asset_registry.get_referencers(data.package_name, options)
    return dependencies

asset, = unreal.EditorUtilityLibrary.get_selected_assets()
depend =ls_dependencies(asset.get_path_name())
print(depend)

