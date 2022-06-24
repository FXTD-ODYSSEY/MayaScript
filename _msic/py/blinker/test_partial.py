# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-05-30 15:36:36'


from blinker import signal
from blinker import Signal
from functools import partial

on_commit = Signal()

def run(num,sender):
    print('running',args)
    return 1

on_commit.connect(partial(run, 1), weak=False)
# on_commit.connect(run)

if "__main__" == __name__:

    res = on_commit.send()
    print(res)
    receivers = on_commit.receivers
    print(receivers)
