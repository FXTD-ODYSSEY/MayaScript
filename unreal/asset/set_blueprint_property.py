
import unreal
blueprint, = unreal.EditorUtilityLibrary.get_selected_assets()

path = "%s_C" % blueprint.get_path_name()
bp_gc = unreal.load_object(None, path)
bp_cdo = unreal.get_default_object(bp_gc)

bp_cdo.set_editor_property("default_material",False)
bp_cdo.set_editor_property("default_out_line",False)
bp_cdo.set_editor_property("default_face_material",False)
bp_cdo.set_editor_property("default_face_outline_material",False)
bp_cdo.set_editor_property("enable_self_shadow",True)

