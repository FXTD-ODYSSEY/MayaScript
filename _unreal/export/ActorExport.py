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


def get_selected_info():

    data = nested_dict()
    for actor in level_lib.get_selected_level_actors():
        if isinstance(actor, unreal.StaticMeshActor):
            comp = actor.get_editor_property("static_mesh_component")
            mesh = comp.get_editor_property("static_mesh")
            materials = comp.get_editor_property("override_materials")
        # elif  isinstance(actor,unreal.SkeletalMeshActor):
        #     comp = actor.get_editor_property("skeletal_mesh_component")
        #     mesh = comp.get_editor_property("skeletal_mesh")
        #     materials = comp.get_editor_property("override_materials")
        else:
            continue
        
        mesh_path = mesh.get_path_name()
        materials = set()
        materials.update(set([m.get_path_name() for m in materials if m]))
        materials.update(set(ls_dependencies(mesh_path)))
        
        for material in materials:
            if str(material).startswith("/Engine/"):
                continue
            material = unreal.load_asset(material)
            if not isinstance(material, unreal.MaterialInterface):
                continue
            textures = ls_dependencies(material.get_path_name())
            texture_paths = []
            for texture_path in textures:
                if str(texture_path).startswith("/Engine/"):
                    continue
                texture = unreal.load_asset(texture_path)
                if not isinstance(texture, unreal.Texture):
                    continue
                # texture_paths.append(str(texture_path).replace("/Game/",content_path))
                texture_paths.append(str(texture_path))
            data[mesh_path][str(material.get_name())] = texture_paths

    return data


def export_asset(obj, filename, exporter, options=None,prompt=False):
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
    
    export_path = filedialog.askdirectory(title=u"选择输出的路径")
    if not export_path:
        return
    
    info = get_selected_info()
    if not info:
        print_string("nothing can export")
        return
    
    fbx_exporter = unreal.StaticMeshExporterFBX()
    fbx_option = unreal.FbxExportOption()
    fbx_option.export_morph_targets = False
    fbx_option.export_preview_mesh = False
    fbx_option.level_of_detail = False
    fbx_option.collision = False
    fbx_option.export_local_time = False
    fbx_option.ascii = False
    fbx_option.vertex_color = True

    tga_exporter = unreal.TextureExporterTGA()
    
    for mesh_path, data in info.items():
        mesh = unreal.load_asset(mesh_path)
        mesh_name = os.path.splitext(os.path.basename(mesh_path))[0]
        fbx_path = os.path.join(export_path, "%s.fbx" % mesh_name)
        texture_folder = os.path.join(export_path, "%s_texture" % mesh_name)
        if not os.path.exists(texture_folder):
            os.mkdir(texture_folder)

        # NOTE export mesh FBX
        export_asset(mesh, fbx_path, fbx_exporter, fbx_option)
        for material,texture_paths in data.items():
            for texture_path in texture_paths:
                # NOTE export texture
                asset_data = asset_lib.find_asset_data(texture_path)
                texture_name = asset_data.asset_name
                if not str(texture_name).startswith("T_Env"):
                    continue
                tga_path = os.path.join(texture_folder,"%s.tga" % texture_name)
                texture = asset_data.get_asset()
                export_asset(texture,tga_path,tga_exporter)

    # print(info)


if __name__ == "__main__":
    main()