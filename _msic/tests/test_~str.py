# -*- coding: utf-8 -*-
"""
try to patch `~` operator for string
not work
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-02-17 15:49:23'


from __future__ import print_function
import gc
import ctypes

def patchable_builtin(klass):
    refs = gc.get_referents(klass.__dict__)
    assert len(refs) == 1
    return refs[0]

dikt = patchable_builtin(str)

dikt["__getattr__"] = lambda self,attr:print(attr)



