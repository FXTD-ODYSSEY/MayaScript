# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-04-04 17:19:43"

from Qt import QtCore, QtWidgets, QtGui
from dayu_widgets.qt import application
from floating_spinbox_ui import Ui_Form


class FloatingSpinbox(QtWidgets.QWidget):
    __instance = None

    def __init__(self, parent=None):
        super(FloatingSpinbox, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.spin_box = QtWidgets.QSpinBox()
        layout.addWidget(self.spin_box)

        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Esc"), self)
        self.shortcut.activated.connect(self.hide)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance

    @classmethod
    def popup(cls):
        """Position window to mouse cursor"""
        active_window = QtWidgets.QApplication.activeWindow()
        launcher = cls.instance(active_window)
        launcher.move(QtGui.QCursor.pos())
        launcher.show()


class EventFilter(QtCore.QObject):
    def eventFilter(self, receiver, event):

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.MidButton:
                FloatingSpinbox.popup()

        return super(EventFilter, self).eventFilter(receiver, event)


class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        filter = EventFilter(self)
        scene = QtWidgets.QGraphicsScene()
        self.Graphic_View.setScene(scene)
        self.Graphic_View.installEventFilter(filter)


if __name__ == "__main__":
    with application():
        window = MainWindow()
        window.show()
