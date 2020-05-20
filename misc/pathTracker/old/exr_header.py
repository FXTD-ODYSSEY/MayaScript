# coding:utf-8
from __future__ import unicode_literals,division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-20 09:30:16'

"""

"""

import sys
import array
import OpenEXR
import Imath



# Open the input file
file = OpenEXR.InputFile(br"C:\Users\timmyliang\Desktop\FX\new\Male_rig_1__0002_head_ctrl_follow_plane.exr")

print(file.header())

file = OpenEXR.InputFile(br"C:\Users\timmyliang\Desktop\FX\red_eye001_UV1(1).EXR")

print(file.header())

# # Compute the size
# dw = file.header()['dataWindow']
# sz = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

# # Read the three color channels as 32-bit floats
# FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
# (R,G,B) = [array.array('f', file.channel(Chan, FLOAT)).tolist() for Chan in ("R", "G", "B") ]

# # Normalize so that brightest sample is 1
# brightest = max(R + G + B)
# R = [ i / brightest for i in R ]
# G = [ i / brightest for i in G ]
# B = [ i / brightest for i in B ]

# # Convert to strings
# (Rs, Gs, Bs) = [ array.array('f', Chan).tostring() for Chan in (R, G, B) ]

# # Write the three color channels to the output file
# out = OpenEXR.OutputFile(sys.argv[2], OpenEXR.Header(sz[0], sz[1]))
# out.writePixels({'R' : Rs, 'G' : Gs, 'B' : Gs })