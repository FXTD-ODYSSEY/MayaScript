# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-09-06 16:01:10"

import inspect


class Int2(int):
    def change(self):
        frame = inspect.currentframe()
        locals_dict = frame.f_back.f_locals
        for name, inst in locals_dict.items():
            if inst is self:
                locals_dict[name] = 4

    def __call__(self, value):
        return value


a = Int2(3)
b = c = a
a = 5
print(c)
# a.change()
# print(type(a))
# print(a)
# print(b)

