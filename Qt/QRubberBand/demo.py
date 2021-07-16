# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/13840289/

marque selection
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-16 10:41:41'


from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QVBoxLayout(self)
        layout.setMargin(15)
        layout.setSpacing(10)
        for text in 'One Two Three Four Five'.split():
            layout.addWidget(QtGui.QPushButton(text, self))
        self.rubberband = QtGui.QRubberBand(
            QtGui.QRubberBand.Rectangle, self)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(
            QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberband.show()
        QtGui.QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(
                QtCore.QRect(self.origin, event.pos()).normalized())
        QtGui.QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.hide()
            selected = []
            rect = self.rubberband.geometry()
            for child in self.findChildren(QtGui.QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)
            print ('Selection Contains:\n '),
            if selected:
                print('  '.join(
                    'Button: %s\n' % child.text() for child in selected))
            else:
                print(' Nothing\n')
        QtGui.QWidget.mouseReleaseEvent(self, event)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())