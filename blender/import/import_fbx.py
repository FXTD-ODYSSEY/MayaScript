import bpy

fbx_path = r"G:\file_test\2021-08-17\Char_ouputTest_rig.fbx"
fbx = bpy.ops.import_scene.fbx(filepath=fbx_path)
print(fbx)
