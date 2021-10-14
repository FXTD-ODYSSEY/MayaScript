# -*- coding: utf-8 -*-
"""
ls files
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-10-08 14:50:48'


import os

IS_DIR = True

DIR  = os.path.dirname(os.path.abspath(__file__))
equal = os.path.isdir if IS_DIR else os.path.isfile

for f in os.listdir(DIR):
    if equal(os.path.join(DIR, f)):
        print(f)

