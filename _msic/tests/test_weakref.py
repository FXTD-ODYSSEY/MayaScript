# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-01-19 14:15:23'


import weakref

item_list = weakref.WeakSet()
# item_list = set()

class Test(object):
    pass
a = Test()
item_list.add(a)

for item in item_list:
    print(item)
    
del a
del item

print("after")
for item in item_list:
    print(item)

