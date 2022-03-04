# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-02-18 12:16:49'


import yaml
from collections import OrderedDict
from cerberus import Validator
from cerberus import schema_registry

def ordered_load(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

schema =ordered_load(
    """
tx:
  type: float
ty:
  type: float
tz:
  type: float
rx:
  type: float
ry:
  type: float
rz:
  type: float
sx:
  type: float
sy:
  type: float
sz:
  type: float
"""
)
print(schema)


# info = yaml.dump(schema)
# print(info)
# schema_registry.add("JntInfoSchema", schema)
# schema = yaml.safe_load(
#     """
# neutral_jnts_info:
#   type: dict
#   required: True
#   keysrules:
#     type: string
#   valuesrules:
#     type: dict
#     schema: JntInfoSchema
# """
# )


# print(schema)
# v = Validator(schema)
# document = {
#     "neutral_jnts_info": {
#         "spine_01": {
#             "tx": 0.0,
#             "ty": 0.0,
#             "tz": 0.0,
#             "rx": 0.0,
#             "ry": 0.0,
#             "rz": 0.0,
#             "sx": 1.0,
#             "sy": 1.0,
#             "sz": 1.0,
#         },
#         "spine_02": {
#             "tx": 0.0,
#             "ty": 0.0,
#             "rx": 0.0,
#             "ry": 0.0,
#             "rz": 0.0,
#             "sx": 1.0,
#             "sy": 1.0,
#             "sz": 1.0,
#         },
#     },
# }
# print(document)

# res = v.validate(document)
# print(res)
# print(v.errors)
