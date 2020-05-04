# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 14:52:04'

"""
https://stackoverflow.com/questions/10176226/how-do-i-pass-extra-arguments-to-a-python-decorator
"""

import functools

def myDecorator(func=None,logIt=None):
    if not func:
        return functools.partial(myDecorator, logIt=logIt)
    @functools.wraps(func)
    def f(*args, **kwargs):
        if logIt==1:
            print ('Logging level 1 for {}'.format(func.__name__))
        if logIt==2:
            print ('Logging level 2 for {}'.format(func.__name__))
        else:
            print ('Logging {}'.format(func.__name__))
        return func(*args, **kwargs)
    return f


@myDecorator(logIt=2)
def pow2(i):
    return i**2

@myDecorator
def pow3(i):
    return i**3