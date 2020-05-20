# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-19 21:35:54'

"""

"""

import sys
import json
import array
import Imath
import OpenEXR


if len(sys.argv) != 3:
    print ("usage: json-data exr-output-file")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    img_data = json.load(f,encoding='utf-8')

R = [color[0] for h,width in img_data.items() for w,color in width.items()]
G = [color[1] for h,width in img_data.items() for w,color in width.items()]
B = [color[2] for h,width in img_data.items() for w,color in width.items()]
Rs = array.array('f', R).tostring()
Gs = array.array('f', G).tostring()
Bs = array.array('f', B).tostring()

width = len(img_data.values()[0])
height = len(img_data)
out = OpenEXR.OutputFile(sys.argv[2], OpenEXR.Header(width, height))
out.writePixels({'R' : Rs, 'G' : Gs, 'B' : Gs })
