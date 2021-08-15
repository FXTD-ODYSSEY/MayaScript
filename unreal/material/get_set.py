
import unreal

def main():
        
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


    outline_material,=unreal.EditorUtilityLibrary.get_selected_assets()
    # TODO 测试设置
    attr = "EnableReceiveSelfShadow_ST"
    # attr = "EnableReceiveSelfShadow_UI"
    switch_setter(outline_material,attr,True)
    mat_lib.update_material_instance(outline_material)
    outline = switch_getter(outline_material,attr)
    print(outline)
    # outline_material = unreal.load_asset('/Game/Test/redirectors/L/Materials/M_Chopper01_L_body_Outline.M_Chopper01_L_body_Outline')
    # switch_setter(outline_material, "UseTextureColor", True)
    # switch_setter(outline_material, "UseTangetAsNormal", True)
    # texture = unreal.load_asset('/Game/Test/NewFolder9/St/Textures/T_B0000B01_MihawkVSZoro01_St_body_Base')
    # texture_setter(outline_material,"Base",texture)
    # outline_switches = mat_lib.get_static_switch_parameter_names(outline_material)



    # material, = unreal.EditorUtilityLibrary.get_selected_assets()
    # print(texture)

if __name__ == '__main__':
    main()
