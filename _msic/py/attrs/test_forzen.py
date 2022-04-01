# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-18 21:21:40'

import attr

@attr.s(frozen=True)
class ItemAttr(object):
    name = property(lambda self: "{0}_0".format(self.item_type))
    
    # name = attr.ib(type=str)
    item_type = attr.ib(type=str, default="asd")
    # data = attr.ib(type=dict, factory=dict)
    # parent = attr.ib(default=None)
    # parser = attr.ib(default=None)

print(ItemAttr().__init__.__self__)
# for field in attr.fields(ItemAttr):
#     print(field)

# (Attribute(name='name', default=NOTHING, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=<type 'str'>, converter=None, kw_only=False), Attribute(name='item_type', default='asd', validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=<type 'str'>, converter=None, kw_only=False), Attribute(name='data', default=Factory(factory=<type 'dict'>, takes_self=False), validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=<type 'dict'>, converter=None, kw_only=False), Attribute(name='parent', default=None, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False), Attribute(name='parser', default=None, validator=None, repr=True, eq=True, order=True, hash=None, init=True, metadata=mappingproxy({}), type=None, converter=None, kw_only=False))
