# -*- coding: utf-8 -*-
"""
导入 FBX 
手动导入大量 FBX 名称会有对不上
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-17 13:59:15'

import os
import unreal


asset_tool = unreal.AssetToolsHelpers.get_asset_tools()

def buildImportTask(filename='', destination_path=''):
    options = unreal.FbxImportUI()
    options.set_editor_property(
        "mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)

    task = unreal.AssetImportTask()
    task.set_editor_property("factory", unreal.FbxFactory())
    name = os.path.basename(os.path.splitext(filename)[0])
    # NOTE 设置 automated 为 True  不会弹窗
    task.set_editor_property("automated", True)
    task.set_editor_property("destination_name", name)
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("filename", filename)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", False)
    task.options = options
    return task

def main():
    
    path = r"G:\_minigame\scene\test"
    export_path = '/Game/Map'
    for i,fbx in enumerate(os.listdir(path)):
        if not fbx.endswith(".fbx"):
            continue
        
        task = buildImportTask(os.path.join(path,fbx),export_path)
        asset_tool.import_asset_tasks([task])


if __name__ == "__main__":
    main()
