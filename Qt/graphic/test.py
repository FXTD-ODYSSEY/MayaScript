# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/57946850
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-01-30 17:37:43'
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QGraphicsView, QGraphicsScene, 
                             QFrame, QSizePolicy, QApplication, QSlider, QPushButton)


class MainGraphicsWidget(QGraphicsView):
    def __init__(self, parent=None):
        super(MainGraphicsWidget, self).__init__(parent)

        self._scene = QGraphicsScene() 
        self.setScene(self._scene)
        self.transpSlider = QtWidgets.QSlider(
            QtCore.Qt.Horizontal,
            minimum=10,
            maximum=100,
            value=100,
            valueChanged=self.onValueChanged,
        )
        self.mainButton = QPushButton('I want it to be "Test" button \n QUIT')
        self.mainButton.resize(150, 150)
        self.mainButton.clicked.connect(parent.close)

        self._scene.addWidget(self.mainButton)
        self._scene.addWidget(self.transpSlider)
        self.transpSlider.move(300, 100)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        c = QColor(220, 30, 30)
        c.setAlphaF(1) 
        self.setBackgroundBrush(QBrush(c))
        self.setFrameShape(QFrame.NoFrame)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

    @QtCore.pyqtSlot(int)
    def onValueChanged(self, value):
        c = QColor(220, 30, 30)
        c.setAlphaF(value * 0.01) 
        self.setBackgroundBrush(QBrush(c))
        window.setWindowOpacity(value * 0.03)   
        self.setStyleSheet("MainGraphicsWidget {{background-color: rgba(0, 215, 55, {});}}".format(value))  


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_NoSystemBackground, False)      
        self.setStyleSheet("MainWindow {background-color: rgba(0, 215, 55, 70);}")   

        self.graphicsWidget = MainGraphicsWidget(self)  

        self.window = 'transp_test'
        self.title  = 'transparent UI'
        self.size   = (1000, 650)
        self.setWindowTitle(self.title)
        self.resize(QSize(*self.size))

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)       
        self.mainLayout.addWidget(self.graphicsWidget)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(600, 100, 600, 600)
    window.show()
    sys.exit(app.exec_())