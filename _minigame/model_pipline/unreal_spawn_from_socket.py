# -*- coding: utf-8 -*-
"""
https://answers.unrealengine.com/questions/75214/view.html
使用 locator 流程导入 模型 节省资源
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-17 10:13:14'

import os
import unreal

level_lib = unreal.EditorLevelLibrary()
util_lib = unreal.EditorUtilityLibrary()

def main():
        
    for asset in util_lib.get_selected_assets():
        name = asset.get_name()
        if not isinstance(asset,unreal.StaticMesh) or name.endswith("_loc"):
            continue
        container_path = os.path.splitext(asset.get_path_name())[0]
        container = unreal.load_asset("%s_loc" % container_path)
        if not container:
            print("失败路径 -> %s" % container_path)
            continue
        container = level_lib.spawn_actor_from_object(container,unreal.Vector(0.0, 0.0, 0.0))
        r = unreal.AttachmentRule.SNAP_TO_TARGET
        for socket in container.root_component.get_all_socket_names():
            mesh = level_lib.spawn_actor_from_object(asset,unreal.Vector(0.0, 0.0, 0.0))
            mesh.attach_to_actor(container,socket,r,r,r,False)

if __name__ == "__main__":
    main()