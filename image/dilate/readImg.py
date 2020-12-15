# -*- coding: utf-8 -*-
"""
# https://www.imagemagick.org/Usage/convolve/#directional
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-12-09 11:24:11'

import os
from Qt import QtGui

DIR = os.path.dirname(__file__)

path = os.path.join(DIR, 'dilation2.png')
from Qt import QtGui
path = r"F:\MayaTecent\MayaScript\image\dilate\dilation2.png"

image = QtGui.QImage(path)

x,y = (0.20455388724803925, 0.4176434576511383)
pixel = image.pixelColor(x*1000,y*1000)
print(pixel.hue())



