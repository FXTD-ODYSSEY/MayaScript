# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/63642583
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-12-01 20:22:46'

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class DockWidget(QtWidgets.QDockWidget):
    def __init__(self, title: str):
        super().__init__(title)
        self.setTitleBarWidget(QtWidgets.QWidget())
        self.dockLocationChanged.connect(self.on_dockLocationChanged)

    def on_dockLocationChanged(self):
        main = self.parent()
        all_dock_widgets = main.findChildren(QtWidgets.QDockWidget)

        for dock_widget in all_dock_widgets:
            sibling_tabs = main.tabifiedDockWidgets(dock_widget)
            # If you pull a tab out of a group the other tabs still see it as a sibling while dragging...
            sibling_tabs = [s for s in sibling_tabs if not s.isFloating()]

            if len(sibling_tabs) != 0:
                # Hide title bar
                dock_widget.setTitleBarWidget(QtWidgets.QWidget())
            else:
                # Re-enable title bar
                dock_widget.setTitleBarWidget(None)

    def minimumSizeHint(self):
        return QtCore.QSize(100, 100)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main = QtWidgets.QMainWindow()

    dock1 = DockWidget("Blue")
    dock2 = DockWidget("Green")
    dock3 = DockWidget("Red")

    content1 = QtWidgets.QWidget()
    content1.setStyleSheet("background-color:blue;")
    content1.setMinimumSize(QtCore.QSize(50, 50))

    content2 = QtWidgets.QWidget()
    content2.setStyleSheet("background-color:green;")
    content2.setMinimumSize(QtCore.QSize(50, 50))

    content3 = QtWidgets.QWidget()
    content3.setStyleSheet("background-color:red;")
    content3.setMinimumSize(QtCore.QSize(50, 50))

    dock1.setWidget(content1)
    dock2.setWidget(content2)
    dock3.setWidget(content3)

    dock1.setAllowedAreas(Qt.AllDockWidgetAreas)
    dock2.setAllowedAreas(Qt.AllDockWidgetAreas)
    dock3.setAllowedAreas(Qt.AllDockWidgetAreas)

    main.addDockWidget(Qt.LeftDockWidgetArea, dock1)
    main.tabifyDockWidget(dock1, dock2)
    main.addDockWidget(Qt.RightDockWidgetArea, dock3)

    main.setDockOptions(main.GroupedDragging | main.AllowTabbedDocks | main.AllowNestedDocks)

    main.setTabPosition(Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)
    main.resize(400, 200)
    main.show()

    app.exec_()
