# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-24 10:35:32'

"""
MTexture 不支持 OpenMaya 1.0
MTexture 无法实例化

MTexture 比起 MImage 可以输出 exr 格式
"""

import os
import ctypes
import struct

import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr

manager = omr.MRenderer.getTextureManager()
print (dir(manager))
path_list = manager.imagePaths()

# NOTE ----------------------------------------------------------------
# NOTE 读取本地图片
# NOTE ----------------------------------------------------------------
DIR = os.path.dirname(__file__)
file_name = os.path.join(DIR,"test7.exr")

texture = manager.acquireTexture(file_name)
# print ("bytesPerPixel",texture.bytesPerPixel())

pixel,rowPitch,total = texture.rawData()
ptr = ctypes.cast(pixel.__long__(), ctypes.POINTER(ctypes.c_char))
pixels = ctypes.string_at(ptr, total)
height = int(total/rowPitch)
width = int(rowPitch/4)
# texture.freeRawData(pixel)
# print(height,total,width)

# NOTE ----------------------------------------------------------------
# NOTE 对比 MImage 和 MTexture 输出
# NOTE ----------------------------------------------------------------
# width = 1000
# height = 1000

# NOTE https://groups.google.com/forum/#!topic/python_inside_maya/Q9NuAd6Av20
# pixels_num = [ord(c) for c in pixels]
# with open(os.path.join(DIR,"test.txt"),'w') as f:
#     f.write(str(pixels_num))


pixels = range(width*height*4)
for w in range(width):
    for h in range(height):
        pos = (w+h*width)*4
        # NOTE 这里加数字代表当前像素下 RGBA 四个通道的值
        pixels[pos+0] = 25.5
        pixels[pos+1] = 213.8
        pixels[pos+2] = 0.5
        pixels[pos+3] = 255

img = om.MImage()
img.setPixels(pixels, width, height)
img.writeToFile(os.path.join(DIR,"MImage.png"), 'png')

# NOTE 无法执行 update 修改像素数据 _(:з」∠)_
# texture.update(pixels,False,rowPitch)
manager.saveTexture(texture,os.path.join(DIR,"MTexture.png"))

# NOTE ----------------------------------------------------------------
# NOTE Maya导入运行
# NOTE ----------------------------------------------------------------
# import sys
# MODULE = r"F:\MayaTecent\MayaScript\misc\python_exr"
# sys.path.insert(0,MODULE) if MODULE not in sys.path else None
# import MTextureWriteFile
# reload(MTextureWriteFile)