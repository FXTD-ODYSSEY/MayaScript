# -*- coding: utf-8 -*-
"""
https://doc.qt.io/qtforpython-5/PySide2/QtGui/QPainterPath.html?highlight=qpainterpath#PySide2.QtGui.PySide2.QtGui.QPainterPath.cubicTo

cubicTo illustration
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-08-28 17:03:53"

import math

from Qt import QtGui
from Qt import QtWidgets
from Qt import QtCore
from dayu_widgets.qt import application


class CurvePoint(QtWidgets.QGraphicsItem):
    def __init__(self, color=None):
        super(CurvePoint, self).__init__()
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.color = color or QtCore.Qt.red

    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)

    def paint(self, painter, option, widget):

        painter.setBrush(QtGui.QBrush(self.color))
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)


class CurveView(QtWidgets.QGraphicsView):
    def __init__(self):
        super(CurveView, self).__init__()
        self.setDragMode(self.ScrollHandDrag)

        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(-750, -750, 1500, 1500)

        self.start_pt = CurvePoint()
        self.end_pt = CurvePoint()
        self.start_pt.setPos(0, 0)
        self.end_pt.setPos(200, 200)
        scene.addItem(self.start_pt)
        scene.addItem(self.end_pt)
        self.c1_pt = CurvePoint(QtCore.Qt.yellow)
        self.c2_pt = CurvePoint(QtCore.Qt.yellow)
        self.c1_pt.setPos(0, 100)
        self.c2_pt.setPos(100, 0)
        scene.addItem(self.c1_pt)
        scene.addItem(self.c2_pt)
        self.setScene(scene)

    def mousePressEvent(self, event):
        pos = event.pos()
        self.press_item = self.itemAt(pos)

        return super(CurveView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if isinstance(self.press_item, CurvePoint):
            self.scene().update()

        return super(CurveView, self).mouseMoveEvent(event)

    def wheelEvent(self, event):
        scale_factor = math.pow(2.0, event.delta() / 240.0)
        factor = (
            self.matrix()
            .scale(scale_factor, scale_factor)
            .mapRect(QtCore.QRectF(0, 0, 1, 1))
            .width()
        )

        if factor < 0.07 or factor > 100:
            return

        self.scale(scale_factor, scale_factor)

    def drawBackground(self, painter, rect):
        path = QtGui.QPainterPath(self.start_pt.pos())
        c1 = self.c1_pt.pos()
        c2 = self.c2_pt.pos()
        path.cubicTo(c1, c2, self.end_pt.pos())
        painter.drawPath(path)


# class DrawWidget(QtWidgets.QWidget):
#     def paintEvent(self, event):

#         myGradient = QtGui.QLinearGradient()
#         myPen = QtGui.QPen()

#         myPath = QtGui.QPainterPath()

#         c1 = QtCore.QPoint(0, 0)
#         c2 = QtCore.QPoint(1000, 0)
#         end_point = QtCore.QPoint(1000, 0)
#         myPath.cubicTo(c1, c2, end_point)

#         painter = QtGui.QPainter(self)
#         painter.setBrush(myGradient)
#         painter.setPen(myPen)
#         painter.drawPath(myPath)


def main():
    with application():
        widget = QtWidgets.QWidget()
        widget.show()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)

        view = CurveView()
        layout.addWidget(view)


if __name__ == "__main__":
    main()
