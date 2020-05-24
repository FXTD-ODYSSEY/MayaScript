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

import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr
import ctypes
import struct

manager = omr.MRenderer.getTextureManager()
path_list = manager.imagePaths()

# NOTE ----------------------------------------------------------------
# NOTE 读取本地图片
# NOTE ----------------------------------------------------------------
texture = manager.acquireTexture(r"F:\personal\img\welcome\01.png")
pixel,rowPitch,total = texture.rawData()
ptr = ctypes.cast(pixel.__long__(), ctypes.POINTER(ctypes.c_char))
print(ptr)
pixels = ctypes.string_at(ptr, total)
height = int(total/rowPitch)
width = int(rowPitch/4)
print(height,total,width)

# manager.saveTexture(texture,r"F:\personal\img\01.tga")

# NOTE ----------------------------------------------------------------
# TODO 读取 file 节点 失败
# NOTE ----------------------------------------------------------------
# file_list = om.MGlobal.getSelectionListByName("file1")
# mObj = file_list.getDependNode(0)
# texture = manager.acquireTexture(mObj,allowBackgroundLoad = True)
# print (texture)



# NOTE ----------------------------------------------------------------
# NOTE 对比 MImage 和 MTexture 输出
# NOTE ----------------------------------------------------------------
# width = 1000
# height = 1000

# NOTE https://groups.google.com/forum/#!topic/python_inside_maya/Q9NuAd6Av20
pixels = bytearray([struct.pack("f", 125.1) for i in range(width*height*4)])
# for w in range(width):
#     for h in range(height):
#         pos = (w+h*width)*4
#         # NOTE 这里加数字代表当前像素下 RGBA 四个通道的值
#         pixels[pos+0] = 255
#         pixels[pos+1] = struct.pack("!f", 5.1)
#         pixels[pos+2] = 1
#         pixels[pos+3] = 255

# NOTE 返回裁剪的 Image
img = om.MImage()
img.setPixels(pixels, width, height)


# texture2 = manager.acquireDepthTexture("file1",[ord(char) for char in pixels],width,height)

# textureDesc = omr.MTextureDescription()
# textureDesc.setToDefault2DTexture()
# textureDesc.fHeight = height
# textureDesc.fWidth = width
# texture2 = manager.acquireDepthTexture("file6",textureDesc,pixels,False)

texture = manager.acquireDepthTexture("file3",bytearray(),width,height)
texture.update(pixels,False,rowPitch)
manager.saveTexture(texture,r"F:\personal\img\04.jpg")
img.writeToFile(r"F:\personal\img\02.jpg", 'jpg')

# NOTE ----------------------------------------------------------------
# NOTE Maya导入运行
# NOTE ----------------------------------------------------------------
# import sys
# MODULE = r"F:\MayaTecent\MayaScript\_OpenMayaDemo\texture&image"
# sys.path.insert(0,MODULE) if MODULE not in sys.path else None
# import MTextureWriteFile
# reload(MTextureWriteFile)