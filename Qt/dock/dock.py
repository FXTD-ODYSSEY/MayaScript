# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/31915249
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-11-29 16:29:08"

from Qt import QtCore, QtWidgets
from Qt.QtWidgets import QMainWindow, QTextEdit, QDockWidget

_DOCK_OPTS = QtWidgets.QMainWindow.AllowNestedDocks
_DOCK_OPTS |= QtWidgets.QMainWindow.AllowTabbedDocks


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.centralContent = QtWidgets.QMainWindow()

        self.setCentralWidget(self.centralContent)

        self.centralContent.firstTabWidget = QtWidgets.QTextEdit()
        self.centralContent.firstTabDock = QtWidgets.QDockWidget("first")
        self.centralContent.firstTabDock.setWidget(self.centralContent.firstTabWidget)
        self.centralContent.addDockWidget(
            QtCore.Qt.LeftDockWidgetArea, self.centralContent.firstTabDock
        )
        self.centralContent.secondTabWidget = QtWidgets.QTextEdit()
        self.centralContent.secondTabDock = QtWidgets.QDockWidget("second")
        self.centralContent.secondTabDock.setWidget(self.centralContent.secondTabWidget)
        self.centralContent.addDockWidget(
            QtCore.Qt.RightDockWidgetArea, self.centralContent.secondTabDock
        )
        

        # self.centralContent.tabifyDockWidget(
        #     self.centralContent.firstTabDock, self.centralContent.secondTabDock
        # )

        layout = self.layout()
        layout.setContentsMargins(10, 10, 10, 10)
        print(layout)

        # secondQMainWindow = QMainWindow()
        # self.central = secondQMainWindow
        # self.setDockOptions(_DOCK_OPTS)
        # dw1 = QDockWidget("One")
        # textArea = QTextEdit()
        # textArea.setText("Text area 1")
        # dw1.setWidget(textArea)

        # dw2 = QDockWidget("Two")
        # textArea2 = QTextEdit()
        # textArea2.setText("Text area 2")
        # dw2.setWidget(textArea2)
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dw1)
        # self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dw2)
        # self.tabifyDockWidget(dw1, dw2)
        # dw3 = QDockWidget("Three")
        # textArea3 = QTextEdit()
        # textArea3.setText("Text area 3")
        # dw3.setWidget(textArea3)
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dw3)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
