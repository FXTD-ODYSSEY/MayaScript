# -*- coding: utf-8 -*-
"""
图片数据压缩转换为 base64 数据进行存储
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-10-16 15:12:14'

import base64
import zlib

path = r"D:\3dsMax2017\3ds Max 2017\Icons\icon_main.ico"
with open(path, "rb") as f:
    output = f.read()

output = zlib.compress(output)
output = base64.b64encode(output)

with open('./test.txt','wb') as f:
    f.write(output)

path = r"G:\tencent_git\AppManager\test.txt"
with open(path,'rb') as f:
    data =f.read()

data = base64.b64decode(data)
data = zlib.decompress(data)

with open('./test.png','wb') as f:
    f.write(data)