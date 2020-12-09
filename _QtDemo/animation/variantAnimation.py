# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/46961642
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-12-04 21:34:44'


import sys
from Qt import QtCore,QtGui,QtWidgets

# class AnimateBetweenNums(QtCore.QVariantAnimation):
#     def __init__(self):
#         QtCore.QVariantAnimation.__init__(self)

#     def updateCurrentValue(self, value):
#         print (value)

class MyProgressbar(QtWidgets.QWidget):
    def __init__(self):
        super(MyProgressbar, self).__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(2, 2)
        self.anim = QtCore.QVariantAnimation()
        self.anim.setDuration(1000)
        self.anim.valueChanged.connect(self.updateValue)
        self.value = 50

    def setValue(self, value):
        self.anim.setStartValue(self.value)
        self.anim.setEndValue(value)
        self.anim.start()

    def updateValue(self, value):
        self.value = value
        self.repaint()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()
        till = int(((w / 100.0) * self.value))

        #the bar
        qp.setPen(QtGui.QColor(255, 255, 255))
        qp.setBrush(QtGui.QColor(0, 228, 47))
        qp.drawRect(0, 0, till, h)

        #the box
        pen = QtGui.QPen(QtGui.QColor(75,80,100), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)


class Example(QtWidgets.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        hbox = QtWidgets.QVBoxLayout()
        self.button10 = QtWidgets.QPushButton("10")
        hbox.addWidget(self.button10)
        self.button70 = QtWidgets.QPushButton("70")
        hbox.addWidget(self.button70)
        self.progress = MyProgressbar()
        hbox.addWidget(self.progress)
        self.setLayout(hbox)
        self.setGeometry(300, 300, 390, 210)
        self.show()
        self.button10.clicked.connect(self.changeValue10)
        self.button70.clicked.connect(self.changeValue70)

    def changeValue10(self, value):
        self.progress.setValue(10)

    def changeValue70(self, value):
        self.progress.setValue(70)

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()