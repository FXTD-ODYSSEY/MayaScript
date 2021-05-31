
import unreal

red_lib = unreal.RedArtToolkitBPLibrary
mat_lib = unreal.MaterialEditingLibrary

texture_getter = mat_lib.get_material_instance_texture_parameter_value
texture_setter = mat_lib.set_material_instance_texture_parameter_value

switch_getter = mat_lib.get_material_instance_static_switch_parameter_value
switch_setter = red_lib.set_material_instance_static_switch_parameter_value

vector_getter = mat_lib.get_material_instance_vector_parameter_value
vector_setter = mat_lib.set_material_instance_vector_parameter_value

scalar_getter = mat_lib.get_material_instance_scalar_parameter_value
scalar_setter = mat_lib.set_material_instance_scalar_parameter_value


mesh,=unreal.EditorUtilityLibrary.get_selected_assets()
outline_material = unreal.load_asset('/Game/Test/redirectors/L/Materials/M_Chopper01_L_body_Outline.M_Chopper01_L_body_Outline')
switch_setter = red_lib.set_material_instance_static_switch_parameter_value
switch_setter(outline_material, "UseTextureColor", True)
switch_setter(outline_material, "UseTangetAsNormal", True)
outline_switches = mat_lib.get_static_switch_parameter_names(outline_material)



material, = unreal.EditorUtilityLibrary.get_selected_assets()
texture = texture_getter(material,"BaseMap")
print(texture)
