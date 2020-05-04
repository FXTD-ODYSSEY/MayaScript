# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 10:02:23'

"""
https://stackoverflow.com/questions/48002748/pyqt5-how-to-click-a-button-to-move-the-paint
"""

import os
def getGitRepo(p):
    return p if [f for f in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if f == '.git'] else None if os.path.dirname(p) == p else getGitRepo(os.path.dirname(p))
repo = getGitRepo(__file__)

import sys
MODULE = os.path.join(repo,"_vendor","Qt")
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

from Qt.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout
from Qt.QtGui import QPainter, QColor, QBrush
from Qt.QtCore import QRect, QPoint

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 400)
        self.setWindowTitle('Colours')
        self.btnPaint = QPushButton("Paint", self)
        self.btnMove = QPushButton("Move x+1 y+1", self)
        self.rect = QRect()

        self.btnPaint.clicked.connect(self.onPaint)
        self.btnMove.clicked.connect(self.onMove)

        self.hlayout = QHBoxLayout(self)
        self.hlayout.addWidget(self.btnPaint)
        self.hlayout.addWidget(self.btnMove)
        self.hlayout.addStretch(1)
        self.show()

    def onPaint(self):
        if self.rect.isNull():
            self.rect = QRect(10, 15, 80, 45)
            self.update()

    def onMove(self):
        if not self.rect.isNull():
            self.rect.translate(QPoint(1, 1))
            self.update()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.setPen(QColor("#d4d4d4"))
        qp.setBrush(QColor(200, 0, 0))
        qp.drawRect(self.rect)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())