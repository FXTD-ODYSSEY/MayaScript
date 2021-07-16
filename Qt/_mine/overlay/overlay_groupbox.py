# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-04-04 17:19:43"

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

import os
from functools import partial
from collections import namedtuple

from Qt import QtCore, QtWidgets, QtGui
from Qt.QtCompat import load_ui


class OverlayBase(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OverlayBase, self).__init__(parent)
        DIR, file_name = os.path.split(__file__)
        file_name = os.path.splitext(file_name)[0]
        load_ui(os.path.join(DIR, "%s.ui" % file_name), self)
        
def main():
    UI = OverlayBase()
    UI.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main()
    app.exec_()

    # print(QtWidgets.QLayout.__base__)
    # print(dir(QtCore.QRect))