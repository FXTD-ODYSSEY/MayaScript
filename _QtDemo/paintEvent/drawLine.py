# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 10:02:23'

"""
https://stackoverflow.com/questions/49952610/pyqt5-draw-a-line-by-clicking-qpushbutton
"""
import os
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()

import sys
MODULE = os.path.join(repo,"_vendor","Qt")
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

from Qt.QtWidgets import QMainWindow,QPushButton, QApplication
from Qt.QtCore import QSize, Qt, QLine, QPoint
from Qt.QtGui import QPainter, QPen

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 300)) 

        pybutton = QPushButton('button', self)
        pybutton.clicked.connect(self.draw_line)
        pybutton.resize(100,100)
        pybutton.move(100, 100) 
        self.line = QLine()

    def draw_line(self):
        button = self.sender()
        self.line = QLine(QPoint(), button.pos())
        self.update()

    def paintEvent(self,event):
        QMainWindow.paintEvent(self, event)
        if not self.line.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            painter.drawLine(self.line)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())