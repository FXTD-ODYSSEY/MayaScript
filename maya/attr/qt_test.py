# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-22 10:18:33'


from Qt import QtCore
import attr

@attr.s
class PoseController(QtCore.QObject):
    test = attr.ib(default="")

PoseController()
