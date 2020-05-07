# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 14:52:04'

"""
https://stackoverflow.com/questions/10176226/how-do-i-pass-extra-arguments-to-a-python-decorator
"""

import time
from functools import partial, wraps

def myDecorator(func=None,logIt=None):
    print("func",func,logIt)
    if not func:
        return partial(myDecorator, logIt=logIt)
    @wraps(func)
    def f(*args, **kwargs):
        if logIt==1:
            print ('Logging level 1 for {}'.format(func.__name__))
        if logIt==2:
            print ('Logging level 2 for {}'.format(func.__name__))
        else:
            print ('Logging {}'.format(func.__name__))
        return func(*args, **kwargs)
    return f

def logTime(func=None, msg="elapsed time:"):
    if not func:
        return partial(logTime,msg=msg)
    @wraps(func)
    def wrapper(*args, **kwargs):
        curr = time.time()
        res = func(*args, **kwargs)
        print(msg,time.time() - curr)
        return res
    return wrapper


@logTime()
def pow2(i):
    return [j ** 2 for j in range(i**2)]

# @myDecorator
# def pow3(i):
#     return i**3

if __name__ == "__main__":
    pow2(1000)
    