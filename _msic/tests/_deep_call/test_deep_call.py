# -*- coding: utf-8 -*-
"""
how to fix call stack hell
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-04 14:54:04'

import time
from dependencies import Injector
# from conf import threshold


def baz(threshold):
    time.sleep(threshold)

def bar():
    baz()

def foo():
    bar()

def main():
    foo()
    
if __name__ == '__main__':
    main()
    