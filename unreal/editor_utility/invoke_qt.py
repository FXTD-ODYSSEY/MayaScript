# -*- coding: utf-8 -*-
"""
Paint Qt Image into UMG and keep response
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import os
import posixpath
import tempfile
from dayu_widgets import dayu_theme

# Import local modules
from Qt import QtCore
from Qt import QtWidgets
import unreal
from unreal import RenderingLibrary as rendering_lib
from unreal import WidgetLayoutLibrary as layout_lib
from unreal import EditorAssetLibrary as asset_lib
from unreal import SlateLibrary as slate_lib
from unreal import PyToolkitBPLibrary as py_lib

asset_tool = unreal.AssetToolsHelpers.get_asset_tools()


temp_dir = posixpath.join(tempfile.gettempdir(), "unreal_qt_test")
if os.path.isdir(temp_dir):
    os.mkdir(temp_dir)
image_path = posixpath.join(temp_dir, "test.png")
image_path = r"C:\test.png"


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


@unreal.uclass()
class EditorWidget4Qt(unreal.EditorUtilityWidget):
    debug = True
    image = unreal.uproperty(unreal.Image)

    def bind_widget(self, widget):
        pixmap = widget.grab()
        pixmap.save(image_path, "PNG")
        # print(self.get_desired_size())

        # NOTES(timmyliang): set image size
        texture = rendering_lib.import_file_as_texture2d(None, image_path)
        self.image.set_brush_from_texture(texture)
        x = texture.blueprint_get_size_x()
        y = texture.blueprint_get_size_y()
        self.image.slot.set_size(unreal.Vector2D(x, y))

    @unreal.ufunction(override=True)
    def tick(self, my_geometry, delta_time):
        geo = self.get_paint_space_geometry()
        size = slate_lib.getLocalSize(geo)
        print(size)


    @unreal.ufunction(override=True)
    def construct(self):
        super(EditorWidget4Qt, self).construct()
        # NOTES(timmyliang): add image into canvas
        canvas = unreal.load_object(
            None, "{0}:WidgetTree.CanvasPanel_0".format(self.get_path_name())
        )
        self.image = unreal.Image()
        canvas.add_child_to_canvas(self.image)

    @unreal.ufunction(override=True)
    def destruct(self):
        # NOTES(timmyliang): close event
        print("destruct")
        return super(EditorWidget4Qt, self).destruct()

    @unreal.ufunction(override=True)
    def on_mouse_button_down(self, my_geometry, mouse_event):
        print("on_mouse_button_down")
        size = slate_lib.get_absolute_size(my_geometry)
        print(mouse_event)
        return super(EditorWidget4Qt, self).on_mouse_button_down(
            my_geometry, mouse_event
        )

    @unreal.ufunction(override=True)
    def on_mouse_enter(self, my_geometry, mouse_event):
        print("on_mouse_enter")
        return super(EditorWidget4Qt, self).on_mouse_enter(my_geometry, mouse_event)

    @unreal.ufunction(override=True)
    def on_mouse_move(self, my_geometry, mouse_event):
        # print("on_mouse_move")
        return super(EditorWidget4Qt, self).on_mouse_move(my_geometry, mouse_event)

    @classmethod
    def launch(cls, title=""):
        factory = unreal.EditorUtilityWidgetBlueprintFactory()
        factory.set_editor_property("parent_class", cls)
        bp_path = "/Engine/Transient/{0}".format(cls.__name__)
        editor_widget_bp = create_asset(
            bp_path, cls.debug, unreal.EditorUtilityWidgetBlueprint, factory
        )

        # NOTES(timmyliang): get blueprint generated class and get WidgetTree
        tree = unreal.find_object(
            None, "%s_C:WidgetTree" % editor_widget_bp.get_path_name()
        )
        # NOTES(timmyliang): add CanvasPanel to root_widget
        py_lib.add_root_widget(tree)
        if title:
            editor_widget_bp.rename(title)

        editor_sub = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
        widget, _ = editor_sub.spawn_and_register_tab_and_get_id(editor_widget_bp)
        return widget


def get_qt_widget():
    widget = QtWidgets.QWidget()
    dayu_theme.apply(widget)
    layout = QtWidgets.QVBoxLayout()
    widget.setLayout(layout)

    button = QtWidgets.QPushButton()
    button.setText("Hello")
    button.clicked.connect(lambda: print("hello world"))
    layout.addWidget(button)

    label = QtWidgets.QLabel("asd")
    layout.addWidget(label)
    label = QtWidgets.QLabel("asd")
    layout.addWidget(label)
    label = QtWidgets.QLabel("asd")
    layout.addWidget(label)
    label = QtWidgets.QLabel("asd")
    layout.addWidget(label)
    label = QtWidgets.QLabel("asd")
    layout.addWidget(label)
    label = QtWidgets.QLabel("asd")
    layout.addWidget(label)
    label = QtWidgets.QLabel("asd")
    layout.addWidget(label)

    return widget


def main():

    widget = EditorWidget4Qt.launch()
    widget.bind_widget(get_qt_widget())


if __name__ == "__main__":
    main()
