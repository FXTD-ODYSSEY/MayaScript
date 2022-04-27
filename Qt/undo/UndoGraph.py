# -*- coding: utf-8 -*-
"""
https://blog.csdn.net/islinyoubiao/article/details/105446700
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-04-19 10:53:27'


 
from PyQt5.QtWidgets import (QApplication, QWidget, QUndoCommand, QUndoStack, QUndoView,
                             QGraphicsItem, QGraphicsScene, QGraphicsView,
                             QGraphicsPolygonItem, QPushButton, QAction,
                             QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import (QPoint, QPointF, QLine, QLineF,
                          QRect, QRectF, pyqtSignal, Qt, QObject)
from PyQt5.QtGui import (QPixmap, QPen, QPainter, QKeySequence,
                         QPolygon, QPolygonF, QColor, QBrush)
import random
 
 
class MyShape(QGraphicsPolygonItem):
    def __init__(self, parent=None):
        super(MyShape, self).__init__(parent)
        # self.Type = self.UserType + 1
        self.m_boxItem = QPolygonF()
        self.m_boxItem.append(QPointF(0, 0))
        self.m_boxItem.append(QPointF(30, 0))
        self.m_boxItem.append(QPointF(30, 30))
        self.m_boxItem.append(QPointF(0, 30))
        self.m_boxItem.append(QPointF(0, 0))
        self.setPolygon(self.m_boxItem)
        self.color = QColor(random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        self.brush = QBrush(self.color)
        self.setBrush(self.brush)
 
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
 
    # def type(self):
    #     return self.Type
 
 
class MyScene(QGraphicsScene):
    itemMoveSignal = pyqtSignal(MyShape, QPointF)
 
    def __init__(self):
        super(MyScene, self).__init__()
        self.m_Item = None
        self.m_oldPos = QPointF()
 
    def mousePressEvent(self, event):
        mousePos = QPointF(event.buttonDownScenePos(Qt.LeftButton).x(),
                           event.buttonDownScenePos(Qt.LeftButton).y())
        itemList = []
        itemList = self.items(mousePos)
        if len(itemList) > 0:
            self.m_Item = itemList[0]
        if (self.m_Item is not None) & (event.button() == Qt.LeftButton):
            self.m_oldPos = self.m_Item.pos()
        super(MyScene, self).mousePressEvent(event)
 
    def mouseReleaseEvent(self, event):
        if (self.m_Item is not None) & (event.button() == Qt.LeftButton):
            if self.m_oldPos != self.m_Item.pos():
                self.itemMoveSignal.emit(self.m_Item, self.m_oldPos)
            self.m_Item = None
        super(MyScene, self).mouseReleaseEvent(event)
 
 
class AddCommand(QUndoCommand):
    def __init__(self, scene):
        super(AddCommand, self).__init__()
        self.scene = scene
        self.shape = MyShape()
        self.m_initPos = QPointF(random.randint(1, 10), random.randint(1, 10))
        self.setText("add item")
 
    def redo(self):
        self.scene.addItem(self.shape)
        self.shape.setPos(self.m_initPos)
        self.scene.clearSelection()
        # self.update()
 
    def undo(self):
        self.scene.removeItem(self.shape)
        self.scene.update()
 
 
class MoveCommand(QUndoCommand):
    def __init__(self, item, oldPos):
        super(MoveCommand, self).__init__()
        self.shape = item
        self.m_oldPos = oldPos
        self.m_newPos = self.shape.pos()
 
    def redo(self):
        self.shape.setPos(self.m_newPos)
        self.setText("Move Item %d %d" % (self.shape.pos().x(), self.shape.pos().y()))
 
    def undo(self):
        self.shape.setPos(self.m_oldPos)
        # self.shape.scene().update()
        self.setText("Move Item %d %d" % (self.shape.pos().x(), self.shape.pos().y()))
 
 
class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.button = QPushButton(self)
        self.undoAction = QAction()
        self.redoAction = QAction()
        self.scene = MyScene()
        self.brush = QBrush(Qt.gray)
        self.scene.setSceneRect(QRectF(0, 0, 200, 300))
        self.scene.setBackgroundBrush(self.brush)
        self.scene.itemMoveSignal.connect(self.ShapeMoved)
        self.undoStack = QUndoStack()
 
        # init action
        self.undoAction = self.undoStack.createUndoAction(self, "Undo")
        self.undoAction.setShortcut(QKeySequence.Undo)
 
        self.redoAction = self.undoStack.createRedoAction(self, "Redo")
        self.redoAction.setShortcut(QKeySequence.Redo)
 
        self.addAction(self.undoAction)
        self.addAction(self.redoAction)
 
        # init ui
        self.button.setText("Add Shape")
        self.button.clicked.connect(self.AddItem)
 
        self.view = QGraphicsView()
        self.view.setScene(self.scene)
 
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.button)
        self.vlayout.addWidget(self.view)
 
        self.hlayout = QHBoxLayout()
        self.undoView = QUndoView(self.undoStack)
        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addWidget(self.undoView)
 
        self.setLayout(self.hlayout)
 
    def AddItem(self):
        add = AddCommand(self.scene)
        self.undoStack.push(add)
 
    def ShapeMoved(self, item, pos):
        move = MoveCommand(item, pos)
        self.undoStack.push(move)
 
 
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Form()
    form.setWindowTitle("Undo/Todo")
    form.show()
    sys.exit(app.exec_())
 