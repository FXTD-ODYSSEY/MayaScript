# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-04-24 14:32:21'


import unreal



# def export_asset(obj, filename, exporter, options=None,prompt=False):
#     task = unreal.AssetExportTask()
#     task.set_editor_property("object", obj)
#     task.set_editor_property("filename", filename)
#     task.set_editor_property("exporter", exporter)
#     task.set_editor_property("automated", True)
#     task.set_editor_property("prompt", prompt)
#     task.set_editor_property("options", options) if options else None

#     check = unreal.Exporter.run_asset_export_task(task)
#     if not check:
#         msg = "fail export %s" % filename
#         return
    
output_file = r'G:\ue_test_plugin\cpp_425_android\ue4_output.fbx'

selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
if len(selected_actors) == 0:
    print("No actor selected, nothing to export")
    quit()
 
task = unreal.AssetExportTask()
task.object = selected_actors[0].get_world()
task.filename = output_file
task.selected = True
task.replace_identical = False
task.prompt = False
task.automated = True
task.options = unreal.FbxExportOption()
task.options.vertex_color = False
task.options.collision = False
task.options.level_of_detail = False
unreal.Exporter.run_asset_export_task(task)