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


from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui

class Window(QtWidgets.QWidget):
    def __init__(self,*args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setMargin(15)
        layout.setSpacing(10)
        for text in 'One Two Three Four Five'.split():
            layout.addWidget(QtWidgets.QPushButton(text, self))
        self.rubberband = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(
            QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberband.show()
        return super(Window, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.setGeometry(
                QtCore.QRect(self.origin, event.pos()).normalized())
        return super(Window, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.hide()
            selected = []
            rect = self.rubberband.geometry()
            for child in self.findChildren(QtWidgets.QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)
            print ('Selection Contains:\n '),
            if selected:
                print('  '.join(
                    'Button: %s\n' % child.text() for child in selected))
            else:
                print(' Nothing\n')
        return super(Window, self).mouseReleaseEvent(event)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())