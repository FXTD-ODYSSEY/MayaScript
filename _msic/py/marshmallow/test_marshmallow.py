# -*- coding: utf-8 -*-
"""Test marshmallow."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import datetime as dt
import weakref

# Import third-party modules
from addict import Dict
import attr
from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load
from marshmallow import pprint

# from six.moves.builtins import _


@attr.s
class PoseItemBase(Dict):
    name = attr.ib()
    parent = attr.ib(default=None)
    children = attr.ib(default=[])
    data = attr.ib(default={})
    
    _instances = weakref.WeakSet()
    
    def __attrs_post_init__(self):
        print("init")
        # self._instances.add(self)
    
    def __hash__(self):
        return id(self)

    # self.parent = None
    # self.children = []
    # self.name = self.get_unique_name(name)
    # self.data = {}


class PoseItem(PoseItemBase):
    def __init__(self, *args, **kwargs):
        super(PoseItem, self).__init__(*args, **kwargs)
        print("__init__")


class PoseItemSchema(Schema):
    # parent = fields()
    name = fields.Str()
    data = fields.Dict()
    # children = fields.Nested(PoseItemSchema())


user = PoseItem(name="Monty")
print(user)
schema = PoseItemSchema()
result = schema.dump(user).data
result = schema.load(result).data
pprint(result)

a = PoseItem("a")
b = PoseItem("b")
a.data = {'a':1}
print(a)
