# -*- coding: utf-8 -*-
"""
trim 可以将图片周围的空余给清理掉
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-08-13 11:09:19"


import os
import subprocess

DIR = os.path.dirname(__file__)
imconvert = r"C:\Program Files\Autodesk\Maya2018\bin\imconvert.exe"
# imconvert = r"C:\Program Files\Adobe\Adobe Photoshop 2021\convert.exe"

commands = [
    imconvert,
    os.path.join(DIR, "man.gif"),
    "-trim",
    os.path.join(DIR, "output.png"),
]

command = " ".join(commands)
subprocess.call(command)
