# -*- coding: utf-8 -*-
"""
# 使用 maya 自带的 ImageMagick 计算边缘方向
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-12-09 11:24:11'


import os
import posixpath
import subprocess
# creating a image object
DIR = os.path.dirname(__file__)
imconvert = r"C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe"
output =  posixpath.join(DIR,"rainbow.jpg")
command = ''' "%s" -size 30x600 xc:'#0F0' -colorspace HSB gradient: -compose CopyRed -composite -colorspace RGB -rotate 90  %s''' % (imconvert,output)

print(command)
# subprocess.Popen(command)

# os.startfile(os.path.dirname(output))
