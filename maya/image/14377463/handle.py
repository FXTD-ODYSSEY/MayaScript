# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-12-11 15:29:19"

import os
import subprocess

# imagemagick = '"%s"' % r"C:\Program Files\Autodesk\Maya2019\bin\imconvert.exe"
imagemagick = '"%s"' % r"G:\ImageMagick\magick.exe"
DIR = os.path.dirname(__file__)
input_img = os.path.join(DIR, "gradient.png")
input_img = os.path.join(DIR, "Bkw#me.png")
folder = os.path.join(DIR, "colors")
if not os.path.isdir(folder):
    os.mkdir(folder)
for f in os.listdir(folder):
    os.remove(os.path.join(folder, f))

command = " ".join([imagemagick, input_img, "+dither -colors 8 -unique-colors txt:"])
# command = " ".join([imagemagick, input, '+dither -colors 16 -define histogram:unique-colors=true -format "%c" histogram:info:'])

command = " ".join([imagemagick, input_img, "-depth 2 -format %c histogram:info:"])
command = " ".join([imagemagick, input_img, "-colors 256 -depth 8 -format %c histogram:info:"])
command = " ".join([imagemagick, input_img, '-format "%[colors]" info:'])

print(command)

color_string = subprocess.check_output(command)

# NOTES(timmyliang) 过滤出图片
for i, text in enumerate(color_string.split(b"\r\n")[1:-1], 1):
    print(text)
    color = "#%s" % str(text).split("#")[-1].split(" ")[0]
    output_image = os.path.join(folder, "%s.png" % color)
    
    continue
    
    # print(text)
    
    
    command = " ".join(
        [
            imagemagick,
            input_img,
            "-fill white +opaque %s" % color,
            "-transparent white -background transparent",
            output_image,
        ]
    )
    subprocess.call(command)

    command = " ".join(
        [
            imagemagick,
            output_image,
            ' -fill black +opaque %s' % color,
            ' -fill white -opaque %s' % color,
            '-format "%[fx:w*h*mean]" info:',
        ]
    )
    
    res = subprocess.check_output(command)
    print(output_image,res)
    # res= res.split(b"Alpha:")[-1].split(b"median: ")[0]
    # print(res)
    # if res.startswith(b'0'):
    #     os.remove(output_image)
