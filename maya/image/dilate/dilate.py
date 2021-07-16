# -*- coding: utf-8 -*-
"""
# 使用 maya 自带的 ImageMagick 膨胀图片
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-12-09 11:24:11'


import os
import sys
import subprocess
# creating a image object
DIR = os.path.dirname(__file__)
imconvert = r"C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe"
IMAGE = os.path.join(DIR, "dilation.png")
output = os.path.join(DIR, "dilation2.png")
dilate = 20

# bin = os.path.dirname(sys.executable)
# imconvert = os.path.join(bin,"imconvert.exe")
# IMAGE = r"C:\Users\timmyliang\Documents\maya\projects\default\images\outUV.png"
# output = r"C:\Users\timmyliang\Documents\maya\projects\default\images\outUV2.png"

subprocess.Popen(
    [
        imconvert,
        IMAGE,
        "-alpha",
        "extract",
        "-morphology",
        "Dilate:%s" % dilate,
        "Octagon",
        "-alpha",
        "copy",
        "-fill",
        "red",
        "+opaque",
        "transparent",
        output,
    ]
)

os.startfile(os.path.dirname(output))
