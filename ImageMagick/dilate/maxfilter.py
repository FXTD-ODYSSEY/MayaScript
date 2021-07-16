# -*- coding: utf-8 -*-
"""
OpenCV 膨胀图片
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-12-09 11:24:55'


import os
import cv2 
import numpy as np 

    
# creating a image object
DIR = os.path.dirname(__file__)
IMAGE = os.path.join(DIR, "dilation.png")
output = os.path.join(DIR, "dilation2.png")

# Reading the input image 
img = cv2.imread(IMAGE, 0) 
  
size = 20
kernel = np.ones((size,size), np.uint8) 
  
img_dilation = cv2.dilate(img, kernel, iterations=1) 

cv2.imwrite(output, img_dilation)


