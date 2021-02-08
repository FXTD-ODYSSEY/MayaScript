# -*- coding: utf-8 -*-
"""
快速编译 uv 生成兼容 Qt.py 的 ui 文件
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-12-04 10:50:02'


import os
import subprocess

Qt_path = r"C:\Magician\python\2.7\Qt.py"
maya_directory = r"C:\Program Files\Autodesk\Maya2019\bin"
mayapy = os.path.join(maya_directory,"mayapy.exe")
uic = os.path.join(maya_directory,"pyside2-uic")

folder = os.path.dirname(__file__)
for ui in os.listdir(folder):
    if not ui.endswith(".ui"):
        continue
    name = os.path.splitext(ui)[0] 
    ui_py = os.path.join(folder, "%s_ui.py" % name)
    subprocess.call(
        [
            mayapy,
            uic,
            "-o",
            ui_py,
            os.path.join(folder, ui),
        ]
    )
    subprocess.call(
        [
            mayapy,
            Qt_path,
            "--convert",
            ui_py,
        ]
    )

