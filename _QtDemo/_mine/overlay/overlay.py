# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from functools import partial

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-04-04 17:19:43"

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

import os
import sys
from functools import partial
from collections import namedtuple

from Qt import QtCore, QtWidgets, QtGui
from Qt.QtCompat import load_ui


class ResizeEventFilter(QtCore.QObject):

    resized = QtCore.Signal(QtCore.QEvent)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            self.resized.emit(event)
        return super().eventFilter(obj, event)


class QOverlay(QtWidgets.QWidget):

    DIRECTION = namedtuple("Direction", "E S W N")(0, 1, 2, 3)
    STRETCH = namedtuple("Stretch", "NoStretch Vertical Horizontal Center Auto")(
        0, 1, 2, 3, 4
    )
    

    def __init__(self, parent=None):
        super(QOverlay, self).__init__(parent=parent)
        QtCore.QTimer.singleShot(0, self.initialize)
        self.stretch = self.STRETCH.Auto
        # TODO https://stackoverflow.com/q/27855137
        # self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def traverse_layout(self, layout):

        target = None
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if isinstance(item, QtWidgets.QLayout):
                target = self.traverse_layout(item)
                if target:
                    break
            elif isinstance(item, QtWidgets.QWidgetItem) and item.widget() is self:
                target = (layout, i)
                break

        return target

    def initialize(self):
        # NOTE 将组件放到最上面 https://stackoverflow.com/a/31197643
        self.raise_()

        layout = self.parentWidget().layout()
        info = self.traverse_layout(layout)
        if not info:
            return

        # NOTE 从 layout 中提取出来
        parent_layout, index = info
        direction = self.property("direction")
        direction = direction.upper() if isinstance(direction, str) else ""
        direction = self.DIRECTION._asdict().get(direction, 0)
        value = 1 if direction <= 1 else -1
        item = parent_layout.itemAt(index - value)
        assert item,"%s wrong overlay direction" % (self)
        parent_layout.takeAt(index)
        
        stretch = self.property("stretch")
        stretch = self.STRETCH._asdict().get(stretch)
        stretch and self.setStretch(stretch)

        parent_widget = parent_layout.parentWidget()
        filter = ResizeEventFilter(self)
        parent_widget.installEventFilter(filter)
        # NOTE 强制更新位置
        data = {
            "direction": direction,
            "item": item,
            "geometry": item.geometry(),
            "layout": parent_layout,
            "original_pos": self.pos(),
        }
        filter.resized.connect(partial(self.resize_overlay, data))
        QtWidgets.QApplication.processEvents()
        self.resize_overlay(data, None)
        self.resize_overlay(data, None)

    def resize_overlay(self, data, event):
        direction = data.get("direction")
        item = data.get("item")
        geometry = data.get("geometry")
        layout = data.get("layout")
        original_pos = data.get("original_pos")

        width = self.geometry().width()
        height = self.geometry().height()
        spacing = layout.spacing()

        new_geometry = item.geometry()
        delta_x = new_geometry.x() - geometry.x()
        delta_y = new_geometry.y() - geometry.y()
        delta_width = new_geometry.width() - geometry.width()
        delta_height = new_geometry.height() - geometry.height()

        x = 0
        y = 0
        if direction == self.DIRECTION.W:
            x = delta_x + width + spacing
            y = delta_y
        elif direction == self.DIRECTION.E:
            x = delta_width + delta_x - width - spacing
            y = delta_y
        elif direction == self.DIRECTION.N:
            x = delta_x
            y = delta_y + height + spacing
        elif direction == self.DIRECTION.S:
            x = delta_x
            y = delta_height + delta_y - height - spacing

        self.move(original_pos + QtCore.QPoint(x, y))

        if self.stretch == self.STRETCH.Auto:
            if direction in [1, 3]:
                self.setFixedWidth(new_geometry.width())
            else:
                self.setFixedHeight(new_geometry.height())
        elif self.stretch == self.STRETCH.Horizontal:
            self.setFixedWidth(new_geometry.width())
        elif self.stretch == self.STRETCH.Vertical:
            self.setFixedHeight(new_geometry.height())
        elif self.stretch == self.STRETCH.Center:
            self.move(original_pos )
            self.setFixedWidth(new_geometry.width())
            self.setFixedHeight(new_geometry.height())

    def setStretch(self, stretch):
        self.stretch = stretch


class OverlayBase(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OverlayBase, self).__init__(parent)
        DIR, file_name = os.path.split(__file__)
        file_name = os.path.splitext(file_name)[0]
        load_ui(os.path.join(DIR, "%s.ui" % file_name), self)
        # self.Overlay.setStretch(self.Overlay.STRETCH.Center)


def main():
    UI = OverlayBase()
    UI.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main()
    app.exec_()

    # print(QtWidgets.QLayout.__base__)
    # print(dir(QtCore.QRect))