import unreal
util_lib = unreal.EditorUtilityLibrary
red_lib = unreal.RedArtToolkitBPLibrary
bp, = unreal.EditorUtilityLibrary.get_selected_assets()

parent = red_lib.get_blueprint_parent_class(bp)
print(parent)
material = unreal.load_asset('/Game/ArtResources/Characters/Roles/Actor/Sanji01/L/Materials/M_Sanji01_L_body.M_Sanji01_L_body')


bp_gc = unreal.load_object(None, "%s_C" % bp.get_path_name())
bp_cdo = unreal.get_default_object(bp_gc)
for comp in red_lib.get_cdo_inherited_components(bp_cdo):
    comp_name = comp.get_name()
    if comp_name == 'FaceRenderer':
        # materials = comp.get_editor_property("outline_multi_pass_materials")
        # comp.set_editor_property("outline_multi_pass_materials",[material])
        materials = comp.get_editor_property("layered_base_material")
        print(materials)


mesh, = unreal.EditorUtilityLibrary.get_selected_assets()
print (mesh.get_outer())
