import unreal
import inspect
util_lib = unreal.EditorUtilityLibrary
red_lib = unreal.RedArtToolkitBPLibrary
bp, = unreal.EditorUtilityLibrary.get_selected_assets()

bp_gc = unreal.load_object(None, "%s_C" % bp.get_path_name())
bp_cdo = unreal.get_default_object(bp_gc)


widget_comp = red_lib.add_component(bp_cdo,bp_cdo.root_component,"Widget",unreal.WidgetComponent)
widget_comp.relative_location = unreal.Vector(0,0,250)
