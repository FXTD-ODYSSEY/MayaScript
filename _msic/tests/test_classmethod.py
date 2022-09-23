# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-09-20 10:18:05"

from collections import defaultdict
import json
import inspect


class A(object):
    @classmethod
    def cls_run(cls, inst):
        print(cls, inst)
        
    def inst_run(self):
        print(self)

a = A()
a.cls_run(a)

print(A.cls_run.__self__)
print(inspect.ismethod(A.cls_run))
print(a.inst_run.__self__)
print(inspect.ismethod(A.inst_run))

class NestedDict(object):
    nested_dict = classmethod(lambda cls: defaultdict(cls.nested_dict))

    def __new__(cls):
        return cls.nested_dict()


b = NestedDict()
print(b)
b[1][2] = 3
print(json.dumps(b))
