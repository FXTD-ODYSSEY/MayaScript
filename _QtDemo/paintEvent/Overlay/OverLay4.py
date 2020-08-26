# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/59648791/overlay-qwidget-with-layout
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-08-18 20:48:27'


import sys

from PySide2 import QtWidgets as Qw
from PySide2 import QtCore as Qc
from PySide2 import QtGui as Qg


class MenuWidgetSignals(Qc.QObject):
    # SIGNALS
    CLOSE = Qc.Signal()

class MenuWidget(Qw.QWidget):
    def __init__(self, parent=None):
        super(MenuWidget, self).__init__(parent)

        self.menu_ui()

    def menu_ui(self):

        # make the window frameless
        self.setWindowFlags(Qc.Qt.FramelessWindowHint)
        self.setAttribute(Qc.Qt.WA_TranslucentBackground)

        s = self.size()
        self.setMinimumSize(500, s.height()-71)

        self.close_btn = self.menu_button()

        self.close_btn.clicked.connect(self.close_menu)

        self.save_btn = self.save_button()
        self.save_btn.clicked.connect(self.save_menu)

        # Layout
        # init GroupBox to limit the width and the height
        menu_grp_box = Qw.QGroupBox(self)
        menu_grp_box.setGeometry(Qc.QRect(0, 70, 500, s.height()-71))

        # init VBoxLayout
        menu_v_box = Qw.QVBoxLayout(menu_grp_box)
        menu_v_box.addStretch(1)
        menu_v_box.setContentsMargins(0, 0, 0, 0)

        # init spacer
        spacer01 = Qw.QSpacerItem(20, 40, Qw.QSizePolicy.Expanding, Qw.QSizePolicy.Minimum)

        # add widgets and items
        menu_v_box.addItem(spacer01)
        menu_v_box.addWidget(self.save_btn)
        menu_v_box.addItem(spacer01)

        menu_grp_box.setLayout(menu_v_box)

        self.SIGNALS = MenuWidgetSignals()

    def menu_button(self):
        """

        Returns:
            QtWidgets.QPushButton: button

        """
        btn = Qw.QPushButton(self, text="To Main")
        btn.setMinimumSize(Qc.QSize(83, 65))

        btn.setToolTip("Close Menu")

        MenuWidget.saving = False

        return btn

    def save_button(self):
        """

        Returns:
            QtWidgets.QPushButton: button

        """
        btn = Qw.QPushButton(self, text="Save")
        btn.setMinimumSize(Qc.QSize(80, 35))
        btn.setToolTip("Saving files and folder settings and close menu")

        return btn

    def close_menu(self):
        self.SIGNALS.CLOSE.emit()

    def save_menu(self):
        MenuWidget.saving = True
        self.close_menu()


class MainWindow(Qw.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.set_ui()

    def set_ui(self):

        self.setFixedSize(1000, 700)

        # init menu button
        menu_btn = self.menu_button()
        menu_btn.setFixedSize(Qc.QSize(83, 65))
        menu_btn.move(0, 0)
        menu_btn.clicked.connect(self.active_menu)

        self.show()

    def menu_button(self):

        btn = Qw.QPushButton(self, text="To Menu")

        btn.setToolTip("Open Menu")

        return btn

    def active_menu(self):
        self._menu_frame = MenuWidget(self)
        self._menu_frame.move(0, 0)
        self._menu_frame.resize(self.width(), self.height())
        self._menu_frame.SIGNALS.CLOSE.connect(self.close_menu)
        self._menu_frame.show()

    def close_menu(self):
        self._menu_frame.close()

if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    hyg_window = MainWindow()
    sys.exit(app.exec_())