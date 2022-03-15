# -*- coding: utf-8 -*-
"""
测试 class 的修改是否影响到 inst
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-11 21:30:59'

class TestClass(object):
    pass

test = TestClass()

TestClass.__dict__["call"]=lambda self:print(123)
test2 = TestClass()
test2.call()
test.call()
