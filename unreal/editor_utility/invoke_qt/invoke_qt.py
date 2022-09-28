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
from functools import partial

# Import local modules
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets
from Qt.QtTest import QTest

import unreal
from unreal import RenderingLibrary as rendering_lib
from unreal import WidgetLayoutLibrary as layout_lib
from unreal import WidgetLibrary as widget_lib
from unreal import EditorAssetLibrary as asset_lib
from unreal import SlateLibrary as slate_lib
from unreal import InputLibrary as input_lib
from unreal import PyToolkitBPLibrary as py_lib


META = {"Category": "UMG4Qt"}
CONFIG = {"static": True, "meta": META}
PATH = "/Game/NewFolder/UMG4Qt"
image_path = r"C:\test.png"


class SuperButton(QtWidgets.QPushButton):
    def HoverEvent(self, event):
        print("hover")
        return super(SuperButton, self).HoverEvent(event)


def get_qt_widget():
    widget = QtWidgets.QWidget()
    dayu_theme.apply(widget)
    layout = QtWidgets.QVBoxLayout()
    widget.setLayout(layout)

    button = SuperButton()
    button.setText("Hello")
    button.setStyleSheet(
        """
        QPushButton::hover {
            background-color: red;
        }
    """
    )
    button.clicked.connect(lambda: print("hello world"))
    layout.addWidget(button)

    edit = QtWidgets.QLineEdit()
    edit.setFocus()
    layout.addWidget(edit)

    combo = QtWidgets.QComboBox()
    for i in range(11):
        combo.addItem("item {0}".format(i + 1))
    layout.addWidget(combo)

    list_widget = QtWidgets.QListWidget()
    for i in range(120):
        list_widget.addItem("item {0}".format(i + 1))
    layout.addWidget(list_widget)
    return widget


def UVector2QPoint(vector):
    return QtCore.QPoint(vector.x, vector.y)


@unreal.uclass()
class UMG4QtBPLibrary(unreal.BlueprintFunctionLibrary):
    qt_widget = None
    mouse_mapping = {
        "Left Mouse Button": QtCore.Qt.LeftButton,
        "Right Mouse Button": QtCore.Qt.RightButton,
        "Middle Mouse Button": QtCore.Qt.MiddleButton,
    }

    @classmethod
    def launch(cls, qt_widget, title=""):
        # qt_widget.show()
        
        # NOTES(timmyliang): make sure not affected by the window title bar
        qt_widget.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        cls.apply_widget(qt_widget)
        editor_widget_bp = unreal.load_object(None, PATH)
        title = title if title else qt_widget.windowTitle()
        if title:
            editor_widget_bp.rename(title)
        editor_sub = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
        widget, _ = editor_sub.spawn_and_register_tab_and_get_id(editor_widget_bp)
        return widget

    @classmethod
    def apply_widget(cls, widget):
        cls.qt_widget = widget

    @classmethod
    def resize_event(cls, widget, size):
        # NOTES(timmyliang): reset size for each tick
        cls.qt_widget.resize(size.x, size.y)
        pixmap = cls.qt_widget.grab()
        pixmap.save(image_path, "PNG")

        # NOTES(timmyliang): set image
        texture = rendering_lib.import_file_as_texture2d(None, image_path)
        image = widget.get_editor_property("QtImage")
        image.set_brush_from_texture(texture)

    @classmethod
    def get_widget(cls, pos=None):
        pos = (
            pos
            if isinstance(pos, QtCore.QPoint)
            else UMG4QtBPLibrary.qt_widget.mapFromGlobal(QtGui.QCursor.pos())
        )
        return UMG4QtBPLibrary.qt_widget.childAt(pos)

    @classmethod
    def post_event(cls, callback):
        widget = UMG4QtBPLibrary.get_widget()
        if isinstance(widget, QtWidgets.QWidget):
            event = callback(widget)
            if event:
                QtWidgets.QApplication.postEvent(widget, event)

    @unreal.ufunction(
        params=[unreal.EditorUtilityWidget, unreal.Vector2D, unreal.Vector2D],
        **CONFIG,
    )
    def handle_tick(widget, pos, size):
        UMG4QtBPLibrary.qt_widget.move(pos.x, pos.y)
        UMG4QtBPLibrary.resize_event(widget, size)

    @unreal.ufunction(params=[unreal.Text], ret=unreal.EventReply, **CONFIG)
    def handle_mouse_button_down(press_type):
        def factory(widget):
            screen_pos = QtGui.QCursor.pos()
            local_pos = widget.mapFromGlobal(screen_pos)
            button_type = UMG4QtBPLibrary.mouse_mapping.get(str(press_type))
            return QtGui.QMouseEvent(
                QtCore.QEvent.MouseButtonPress,
                local_pos,
                screen_pos,
                button_type,
                button_type,
                QtCore.Qt.NoModifier,
            )

        UMG4QtBPLibrary.post_event(factory)
        return widget_lib.handled()

    @unreal.ufunction(params=[unreal.Text], ret=unreal.EventReply, **CONFIG)
    def handle_mouse_button_up(press_type):
        def factory(widget):
            screen_pos = QtGui.QCursor.pos()
            local_pos = widget.mapFromGlobal(screen_pos)
            button_type = UMG4QtBPLibrary.mouse_mapping.get(str(press_type))
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.setFocus()
            return QtGui.QMouseEvent(
                QtCore.QEvent.MouseButtonRelease,
                local_pos,
                screen_pos,
                button_type,
                button_type,
                QtCore.Qt.NoModifier,
            )

        UMG4QtBPLibrary.post_event(factory)
        return widget_lib.handled()

    @unreal.ufunction(params=[unreal.Vector2D], ret=unreal.EventReply, **CONFIG)
    def handle_mouse_move(old_pos):
        old_pos = UVector2QPoint(old_pos)

        def factory(widget):
            screen_pos = QtGui.QCursor.pos()
            return QtGui.QHoverEvent(
                QtCore.QEvent.HoverMove,
                widget.mapFromGlobal(screen_pos),
                widget.mapFromGlobal(old_pos),
            )

        UMG4QtBPLibrary.post_event(factory)
        return widget_lib.handled()

    @unreal.ufunction(params=[float], ret=unreal.EventReply, **CONFIG)
    def handle_mouse_wheel(delta):
        delta *= 120

        def factroy(widget):
            screen_pos = QtGui.QCursor.pos()
            local_pos = widget.mapFromGlobal(screen_pos)
            event = QtGui.QWheelEvent(
                local_pos, delta, QtCore.Qt.NoButton, QtCore.Qt.NoModifier
            )
            return event

        UMG4QtBPLibrary.post_event(factroy)
        return widget_lib.handled()

    @unreal.ufunction(params=[unreal.Text], ret=unreal.EventReply, **CONFIG)
    def handle_key_down(key):
        print(key)
        # TODO(timmyliang): listen key input from native windows event
        # def factroy(widget):
        #     event = QtGui.QKeyEvent(
        #         QtCore.Qt.KeyPress
        #     )
        #     return event

        # UMG4QtBPLibrary.post_event(factroy)
        return widget_lib.handled()

    @unreal.ufunction(params=[unreal.Text], ret=unreal.EventReply, **CONFIG)
    def handle_key_up(key):
        print(key)
        # def factroy(widget):
        #     event = QtGui.QKeyEvent(
        #         QtCore.Qt.KeyPress
        #     )
        #     return event

        # UMG4QtBPLibrary.post_event(factroy)
        return widget_lib.handled()


def main():
    widget = get_qt_widget()
    UMG4QtBPLibrary.launch(widget)


if __name__ == "__main__":
    main()
