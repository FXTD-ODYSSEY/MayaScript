# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-12-28 16:07:39"

import unreal

import os
import json
from collections import defaultdict

# NOTE Python 3 & 2 兼容
try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog, messagebox
except:
    import ttk
    import Tkinter as tk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox

root = tk.Tk()
root.withdraw()

nested_dict = lambda: defaultdict(nested_dict)

level_lib = unreal.EditorLevelLibrary()
asset_lib = unreal.EditorAssetLibrary()
sys_lib = unreal.SystemLibrary()
content_path = sys_lib.get_project_content_directory()
asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

# options = unreal.AssetRegistryDependencyOptions(True, True, True, True, True)
# options.set_editor_property("include_hard_management_references",True)
# options.set_editor_property("include_hard_package_references",True)
# options.set_editor_property("include_searchable_names",True)
# options.set_editor_property("include_soft_management_references",True)
# options.set_editor_property("include_soft_package_references",True)


def print_string(msg, color=None):
    color = color if color else [255, 255, 255, 255]
    sys_lib.print_string(None, msg, text_color=color)


def ls_dependencies(path):
    data = asset_lib.find_asset_data(path)
    options = unreal.AssetRegistryDependencyOptions()
    dependencies = asset_registry.get_dependencies(data.package_name, options)
    return dependencies

def export_asset(obj, filename, exporter, options=None, prompt=False):
    task = unreal.AssetExportTask()
    task.set_editor_property("object", obj)
    task.set_editor_property("filename", filename)
    task.set_editor_property("exporter", exporter)
    task.set_editor_property("automated", True)
    task.set_editor_property("prompt", prompt)
    task.set_editor_property("options", options) if options else None

    check = unreal.Exporter.run_asset_export_task(task)
    if not check:
        msg = "fail export %s" % filename
        print_string(msg)
        return


def main():

    
    selected_static_actors = [
        a
        for a in level_lib.get_selected_level_actors()
        if isinstance(a, unreal.StaticMeshActor)
    ]

    if not selected_static_actors:
        unreal.EditorDialog(
            u"提示",
            u"请至少选择一个 StaticMeshActor 来导出",
            unreal.AppMsgType.OK
        )
        return
    
    fbx_path = filedialog.asksaveasfilename(
        filetypes=[
            ("FBX Files", "*.fbx")
        ],
        title=u"选择导出的路径",
    )
    if not fbx_path:
        return
    elif not fbx_path.lower().endswith(".fbx"):
        fbx_path = "%s.fbx" % fbx_path
    
    
    
    directory,base = os.path.split(fbx_path)
    fbx_name = os.path.splitext(base)[0]

    # NOTE 将选中的 MeshActor 合并
    options = unreal.EditorScriptingMergeStaticMeshActorsOptions()
    asset_path = "/Game/%s" % fbx_name
    options.set_editor_property("base_package_name", asset_path)
    options.set_editor_property("destroy_source_actors", False)
    options.set_editor_property("spawn_merged_actor", False)
    level_lib.merge_static_mesh_actors(selected_static_actors, options)

    # NOTE 导出模型
    mesh = unreal.load_asset(asset_path)
    
    fbx_exporter = unreal.StaticMeshExporterFBX()
    fbx_option = unreal.FbxExportOption()
    fbx_option.export_morph_targets = False
    fbx_option.export_preview_mesh = False
    fbx_option.level_of_detail = False
    fbx_option.collision = False
    fbx_option.export_local_time = False
    fbx_option.ascii = False
    fbx_option.vertex_color = True
    
    export_asset(mesh, fbx_path, fbx_exporter, fbx_option)
    
    texture_folder = os.path.join(directory, "%s_texture" % fbx_name)
    if not os.path.exists(texture_folder):
        os.mkdir(texture_folder)

    # NOTE 导出贴图
    tga_exporter = unreal.TextureExporterTGA()
    for material in mesh.static_materials:
        material = material.material_interface
        textures = ls_dependencies(material.get_path_name())
        texture_paths = []
        for texture_path in textures:
            if str(texture_path).startswith("/Engine/"):
                continue
            texture = unreal.load_asset(texture_path)
            if not isinstance(texture, unreal.Texture):
                continue
            texture_name = texture.get_name()
            tga_path = os.path.join(texture_folder, "%s.tga" % texture_name)
            export_asset(texture, tga_path, tga_exporter)

    # NOTE 删除模型
    asset_lib.delete_asset(asset_path)


if __name__ == "__main__":
    main()