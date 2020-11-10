# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/55707726
替换为 内置 图标
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-10 11:43:20'

import os
from PySide2 import QtCore, QtGui,QtWidgets

root_path = os.path.dirname(os.path.realpath(__file__))
icons_path = file = os.path.join(root_path, "icons")


class MaterialCheckBox(QtWidgets.QWidget):
    clicked = QtCore.Signal()
    toggled = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(MaterialCheckBox, self).__init__(parent)
        self._is_checked = False
        style = QtWidgets.QApplication.style()
        icon = style.standardIcon(QtWidgets.QStyle.SP_DialogApplyButton)
        checkedIcon = MaterialIcon(
            self, 
            icon.pixmap(24,24)
        )
        icon = style.standardIcon(QtWidgets.QStyle.SP_DialogCancelButton)
        uncheckedIcon = MaterialIcon(
            self,
            icon.pixmap(24,24)
        )

        stateMachine = QtCore.QStateMachine(self)

        checkedState = QtCore.QState()
        checkedState.assignProperty(self, b"checked", True)
        checkedState.assignProperty(checkedIcon, b"opacity", 1.0)
        checkedState.assignProperty(uncheckedIcon, b"opacity", 0.0)

        uncheckedState = QtCore.QState()
        uncheckedState.assignProperty(self, b"checked", False)
        uncheckedState.assignProperty(checkedIcon, b"opacity", 0.0)
        uncheckedState.assignProperty(uncheckedIcon, b"opacity", 1.0)

        stateMachine.addState(checkedState)
        stateMachine.addState(uncheckedState)
        stateMachine.setInitialState(uncheckedState)

        duration = 2000

        transition1 = checkedState.addTransition(self.clicked, uncheckedState)
        animation1 = QtCore.QPropertyAnimation(
            checkedIcon, b"opacity", self, duration=duration
        )
        transition1.addAnimation(animation1)
        animation2 = QtCore.QPropertyAnimation(
            uncheckedIcon, b"opacity", self, duration=duration
        )
        transition1.addAnimation(animation2)

        transition2 = uncheckedState.addTransition(self.clicked, checkedState)
        animation3 = QtCore.QPropertyAnimation(
            checkedIcon, b"opacity", self, duration=duration
        )
        transition2.addAnimation(animation3)
        animation4 = QtCore.QPropertyAnimation(
            uncheckedIcon, b"opacity", self, duration=duration
        )
        transition2.addAnimation(animation4)

        stateMachine.start()

    def sizeHint(self):
        return QtCore.QSize(24, 24)

    def isChecked(self):
        return self._is_checked

    def setChecked(self, value):
        if self._is_checked != value:
            self._is_checked = value
            self.toggled.emit(self._is_checked)

    checked = QtCore.Property(
        bool, fget=isChecked, fset=setChecked, notify=toggled
    )

    def mousePressEvent(self, event):
        self.clicked.emit()
        self.update()
        super(MaterialCheckBox, self).mousePressEvent(event)


class MaterialIcon(QtWidgets.QWidget):
    opacityChanged = QtCore.Signal()

    def __init__(self, parent, address):
        super(MaterialIcon, self).__init__(parent)
        self.icon = QtGui.QPixmap(address)
        self._opacity = 0.0

    def opacity(self):
        return self._opacity

    def setOpacity(self, o):
        if o != self._opacity:
            self._opacity = o
            self.opacityChanged.emit()
            self.update()

    opacity = QtCore.Property(
        float, fget=opacity, fset=setOpacity, notify=opacityChanged
    )

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(self.opacity)
        mask = QtGui.QPainter(self.icon)
        mask.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        mask.fillRect(self.icon.rect(), QtGui.QColor(0, 158, 227))
        mask.end()
        painter.drawPixmap(0, 0, self.icon)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MaterialCheckBox()
    w.show()
    sys.exit(app.exec_())
