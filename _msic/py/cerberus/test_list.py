# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/56415704/13452951
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-02-18 12:15:54"

import yaml
from cerberus import Validator
from cerberus import schema_registry
from collections import OrderedDict

PostItemSchema = yaml.safe_load(
    """
data:
  type: dict
  required: true
  keysrules:
    type: string
  valuesrules:
    type: dict
item_type:
  type: string
  required: true
name:
  type: string
  required: true
relevant:
  type: list
  required: true
  schema:
    type: string


"""
)
schema_registry.add("PostItemSchema", PostItemSchema)


v = Validator(PostItemSchema)
document = OrderedDict(
    [("name", "b"), ("data", {}), ("relevant", []), ("item_type", "pose")]
)
print(document)

res = v.validate(document)
print(res)
print(v.errors)
