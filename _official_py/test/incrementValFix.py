# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 14:29:38'

"""
https://www.liaoxuefeng.com/wiki/897692888725344/989705420143968
"""

from functools import partial

def count():
    fs = []
    for i in range(1, 4):
        fs.append(partial(lambda i:i*i,i))
    return fs

f1, f2, f3 = count()

print (f1())
print (f2())
print (f3())
