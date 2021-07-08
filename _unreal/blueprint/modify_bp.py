import unreal
import inspect
util_lib = unreal.EditorUtilityLibrary
red_lib = unreal.RedArtToolkitBPLibrary
bp, = unreal.EditorUtilityLibrary.get_selected_assets()

bp_gc = unreal.load_object(None, "%s_C" % bp.get_path_name())
bp_cdo = unreal.get_default_object(bp_gc)
print(dir(bp_cdo))

def loop(bp_cdo):
    for member_name in dir(bp_cdo):
        try:
            value = getattr(bp_cdo,member_name)
        except:
            value = lambda:None
        
        if not callable(value):
            yield member_name

for member in loop(bp_cdo):
    print(member)
    
    
print(dir(bp_cdo))
bp_cdo.set_editor_property("enable_self_shadow",True)


for comp in red_lib.get_cdo_inherited_components(bp_cdo):
    comp_name = comp.get_name()
    if comp_name == 'FaceRenderer':
        # materials = comp.get_editor_property("outline_multi_pass_materials")
        # comp.set_editor_property("outline_multi_pass_materials",[material])
        materials = comp.get_editor_property("layered_base_material")
        print(materials)


mesh, = unreal.EditorUtilityLibrary.get_selected_assets()
print (mesh.get_outer())
