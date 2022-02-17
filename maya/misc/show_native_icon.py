# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-02-14 17:22:59'

from Qt import QtGui,QtWidgets

label = QtWidgets.QLabel()
icon = QtGui.QIcon(":/arrowRight.png")
label.setPixmap(icon.pixmap(128, 128))
label.show()
