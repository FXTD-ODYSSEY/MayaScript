# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/55259329
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-04-18 22:34:03'


import os
from Qt import QtCore, QtGui, QtWidgets

class RotateMe(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super(RotateMe, self).__init__(*args, **kwargs)
        self._pixmap = QtGui.QPixmap()
        self._animation = QtCore.QVariantAnimation(
            self,
            startValue=0.0,
            endValue=360.0,
            duration=1000,
        )
        self._animation.finished.connect(self._animation.start)
        self._animation.valueChanged.connect(self.on_valueChanged)
        
    def set_pixmap(self, pixmap):
        self._pixmap = pixmap
        self.setPixmap(self._pixmap)

    def start_animation(self):
        if self._animation.state() != QtCore.QAbstractAnimation.Running:
            self._animation.start()

    def on_valueChanged(self, value):
        t = QtGui.QTransform()
        t.rotate(value)
        self.setPixmap(self._pixmap.transformed(t))

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        label = RotateMe(alignment=QtCore.Qt.AlignCenter)
        style = QtWidgets.QApplication.style()
        icon = style.standardIcon(QtWidgets.QStyle.SP_BrowserReload)
        # img_path = os.path.join('path/to/image','image.svg')
        label.set_pixmap(icon.pixmap(32,32))
        button = QtWidgets.QPushButton('Rotate')

        button.clicked.connect(label.start_animation)
        
        label.setFixedSize(30,30)
        lay = QtWidgets.QVBoxLayout(self)
        lay2 = QtWidgets.QHBoxLayout(self)
        lay2.addWidget(label)
        lay2.addWidget(QtWidgets.QLabel("test"))
        lay2.addStretch()
        lay.addLayout(lay2)
        lay.addWidget(button)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())