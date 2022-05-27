from __future__ import print_function
import posixpath
from functools import partial
import unreal

asset_lib = unreal.EditorAssetLibrary
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


def main():
    directory = "/Game/test"
    name = "TestWidget3"
    path = posixpath.join(directory, name)
    factory = unreal.EditorUtilityWidgetBlueprintFactory()
    widget_BP = create_asset(path, True, unreal.EditorUtilityWidgetBlueprint, factory)
    bp_path = '/Game/test/test'
    widget_BP = unreal.load_object(None,bp_path)
    # NOTE 改名强制 compile
    widget_BP.rename("%s_" % posixpath.basename(bp_path))

    # NOTE 生成界面
    editor_sub = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
    widget, id = editor_sub.spawn_and_register_tab_and_get_id(widget_BP)
    print(widget)
    canvas = unreal.load_object(
        None, "%s:WidgetTree.CanvasPanel_0" % widget.get_path_name()
    )
    print(canvas)
    layout = unreal.VerticalBox()
    button = unreal.Button()

    # NOTE 添加按钮点击事件
    delegate = button.on_clicked
    delegate.add_callable(lambda: print("button click"))

    block = unreal.TextBlock()
    block.set_text("test")
    button.add_child(block)
    layout.add_child(button)
    slot = canvas.add_child_to_canvas(layout)

    # NOTE 构筑 Vertical Layout 撑满效果
    slot.set_anchors(unreal.Anchors(maximum=[1, 1]))
    slot.set_offsets(unreal.Margin())

if __name__ == "__main__":
    main()
