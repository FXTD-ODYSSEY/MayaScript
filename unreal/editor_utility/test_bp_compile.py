
import posixpath
import unreal
from unreal import EditorAssetLibrary as asset_lib
from unreal import PyToolkitBPLibrary as py_lib
from unreal import EditorLoadingAndSavingUtils as ls_utils

asset_tool = unreal.AssetToolsHelpers.get_asset_tools()

def create_asset(asset_path="", unique_name=True, asset_class=None, asset_factory=None):

    if unique_name:
        asset_path, _ = asset_tool.create_unique_asset_name(asset_path, "")
    if not asset_lib.does_asset_exist(asset_path=asset_path):
        path, name = posixpath.split(asset_path)
        return asset_tool.create_asset(
            asset_name=name,
            package_path=path,
            asset_class=asset_class,
            factory=asset_factory,
        )
    return unreal.load_asset(asset_path)
    
# path = '/Game/NewFolder/NewEditorUtilityWidgetBlueprint1.NewEditorUtilityWidgetBlueprint1'
# editor_widget_bp = unreal.load_object(None,path)
# canvas = py_lib.add_root_widget(tree)

@unreal.uclass()
class CustomEditorWidget(unreal.EditorUtilityWidget):
    pass

factory = unreal.EditorUtilityWidgetBlueprintFactory()
factory.set_editor_property("parent_class", CustomEditorWidget)
editor_widget_bp = create_asset(
    '/Game/NewFolder/NewEditorUtilityWidgetBlueprint1',
    False,
    unreal.EditorUtilityWidgetBlueprint,
    factory,
)
asset_lib.save_asset(editor_widget_bp.get_path_name())
ls_utils.reload_packages([editor_widget_bp.get_outer()])

# asset_lib.consolidate_assets(editor_widget_bp,[editor_widget_bp])

canvas = unreal.load_object(
    None, "%s_C:WidgetTree.CanvasPanel_0" % editor_widget_bp.get_path_name()
)
print("canvas",canvas)

