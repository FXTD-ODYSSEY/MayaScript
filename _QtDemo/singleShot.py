# -*- coding: utf-8 -*-
"""
递归出发 singleShot
fn  - function 出发的函数
t   - time     延时的时间
d   - depth    记录递归的深度
m   - max      跳出条件
end - end      完成触发的函数
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-07-12 13:18:09'

from Qt import QtCore

delay = QtCore.QTimer.singleShot
call = lambda fn, t=0, d=0, m=5, end=None: (
    delay(t, lambda: (fn(), call(fn, t, d + 1, m, end)))
    if d < m
    else callable(end) and end()
)
