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
import sys
import subprocess
# creating a image object
DIR = os.path.dirname(__file__)
imconvert = '"%s"' % r"C:\Program Files\Autodesk\Maya2017\bin\imconvert.exe"
IMAGE = os.path.join(DIR, "dilation.jpg")
rainbow = os.path.join(DIR, "rainbow.jpg")
output = os.path.join(DIR, "dilation2.png")
dilate = 5

# bin = os.path.dirname(sys.executable)
# imconvert = os.path.join(bin,"imconvert.exe")
# IMAGE = r"C:\Users\timmyliang\Documents\maya\projects\default\images\outUV.png"
# output = r"C:\Users\timmyliang\Documents\maya\projects\default\images\outUV2.png"

# command = " ".join([
#     imconvert,
#     "-size 30x360 xc:red -colorspace HSB",
#     "gradient: -compose CopyRed -composite",
#     "-colorspace RGB -rotate 90",
#     rainbow
# ])

subprocess.call(command, stdout=subprocess.PIPE)

command = " ".join([imconvert,
        IMAGE,
        " -define convolve:scale=50%! -bias 50% ",
        " ( -clone 0 -morphology Convolve Sobel:0 )",
        " ( -clone 0 -morphology Convolve Sobel:90 )",
        # " ( -clone 0 -morphology Convolve Sobel:180 )",
        # " ( -clone 0 -morphology Convolve Sobel:270 )",
        "-delete 0 ",
        # ' ( -clone 0,1 -fx "0.5+atan2(v-0.5,0.5-u)/pi/2" "%s" -clut )' % rainbow,
        ' ( -clone 0,1 -fx "0.5+atan2(v-0.5,0.5-u)/pi/2" )',
        ' ( -clone 0,1 -fx "u>0.48&&u<0.52&&v>0.48&&v<0.52 ? 0.0 : 1.0" )',
        # " -morphology Dilate:10 Octagon",
        " -delete 0,1 -alpha off -compose CopyOpacity -composite",
        # "-alpha extract",
        # "-morphology EdgeOut  Octagon",
        output,])

# print(command)
subprocess.call(command, stdout=subprocess.PIPE)

# subprocess.Popen(command)

# os.startfile(os.path.dirname(output))
