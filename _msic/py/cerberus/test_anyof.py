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

import os
import yaml
from cerberus import Validator
from cerberus import schema_registry

DIR = os.path.dirname(__file__)
with open(os.path.join(DIR, "schema.yaml")) as f:
    schema = yaml.safe_load(f.read())

GroupItemSchema = yaml.safe_load(
    """
children:
  type: list
data:
  type: dict
item_type:
  type: string
name:
  type: string

"""
)
schema_registry.add("GroupItemSchema", GroupItemSchema)



schema = yaml.safe_load(
    """
pose_items:
  type: list
  required: true
  schema:
    type: dict
    schema:
      name:
        type: string
      data:
        type: dict
      relevant:
        type: list
        schema:
          type: string
      item_type:
        type: string
"""
)
print(schema)

v = Validator(schema)
document = {
    "pose_items": [
        {
            "name": "Ear",
            "data": {},
            "children": [
                {
                    "name": "earUp_R",
                    "data": {},
                    "relevant": [
                        "psd_item"
                    ],
                    "item_type": "pose"
                },
                {
                    "name": "earUp_L",
                    "data": {},
                    "relevant": [],
                    "item_type": "pose"
                },
                {
                    "name": "Ear2",
                    "data": {},
                    "children": [
                        {
                            "name": "earUp_L2",
                            "data": {},
                            "relevant": [],
                            "item_type": "pose"
                        },
                        {
                            "name": "earUp_R2",
                            "data": {},
                            "relevant": [],
                            "item_type": "pose"
                        },
                        {
                            "name": "Ear3",
                            "data": {},
                            "children": [
                                {
                                    "name": "earUp_L3",
                                    "data": {},
                                    "relevant": [],
                                    "item_type": "pose"
                                },
                                {
                                    "name": "earUp_R3",
                                    "data": {},
                                    "relevant": [],
                                    "item_type": "pose"
                                }
                            ],
                            "item_type": "group"
                        }
                    ],
                    "item_type": "group"
                }
            ],
            "item_type": "group"
        }
    ],
}
print(document)

res = v.validate(document)
print(res)
print(v.errors)
