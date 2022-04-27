# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-04-19 10:55:04'


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QUndoView,
                             QLabel, QListView, QVBoxLayout, QHBoxLayout,
                             QMenuBar, QMenu, QAction,
                             QUndoStack, QUndoCommand, QStyle)
 
class appendCommand(QUndoCommand):
    def __init__(self, model, parent=None):
        super(appendCommand, self).__init__(parent)
        self.model = model
        
    def redo(self):
        self.item = QStandardItem('new Item')
        self.setText('添加一个条目')
        self.model.appendRow(self.item)
        self.index = self.item.index()
        
    def undo(self):
        self.model.removeRow(self.index.row())
 
class DemoUndoView(QMainWindow):
    def __init__(self, parent=None):
        super(DemoUndoView, self).__init__(parent)   
        
         # 设置窗口标题
        self.setWindowTitle('实战PyQt5: QUndoView 演示')      
        # 设置窗口大小
        self.resize(480, 300)
      
        self.initUi()
        
    def initUi(self):
        mainWidget = QWidget()
        mainLayout = QHBoxLayout()
        
        #第一列，命令操作
        lLayout = QVBoxLayout()
        lLayout.addWidget(QLabel('命令操作'))
        self.listView = QListView()
        lLayout.addWidget(self.listView)
        
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        
        #第二列， undo/redo
        
        #undo 堆栈
        self.undoStack = QUndoStack(self)
 
        rLayout = QVBoxLayout()
        rLayout.addWidget(QLabel('撤销/重做'))
        self.undoView = QUndoView(self.undoStack)
        self.undoView.setCleanIcon(QApplication.style().standardIcon(QStyle.SP_DialogCloseButton))
        rLayout.addWidget(self.undoView)
        
        mainLayout.addLayout(lLayout)
        mainLayout.addLayout(rLayout)
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
        self.initMenu()
        
        
    def initMenu(self):
        menuBar = self.menuBar()
        
        # 文件栏
        fileMenu = menuBar.addMenu('文件')
        fileExit = QAction('退出', self)
        fileExit.triggered.connect(self.close)
        fileMenu.addAction(fileExit)
        
        #编辑栏
        editMenu = menuBar.addMenu('编辑')
        editAppend = QAction('添加条目', self)
        editAppend.triggered.connect(self.onEditAppend)
        editMenu.addAction(editAppend)
        editMenu.addSeparator()
        editMenu.addAction(self.undoStack.createUndoAction(self, '撤销'))
        editMenu.addAction(self.undoStack.createRedoAction(self, '重做'))
        editClear = QAction('清除', self)
        editClear.triggered.connect(self.onEditClear)
        editMenu.addAction(editClear)
        
    def onEditAppend(self):
        self.undoStack.push(appendCommand(self.model))
    
    def onEditClear(self):
        self.undoStack.clear()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoUndoView()
    window.show()
    sys.exit(app.exec())
