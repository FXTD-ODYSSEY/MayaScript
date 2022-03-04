# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-01-20 16:17:10"


from addict import Dict
import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))

extra = Dict()
extra.a = 1
extra.b = "asd"


class DB(Dict):
    def __init__(self):
        self.test2 = 1
        self.abc = "abc"

    def test(self):
        print("test call")

    def __setattr__(self, name, value):
        print(name, value)


data = DB()
data.extra = extra

with open(os.path.join(DIR, "abc.json"), "w") as f:
    json.dump(data, f)
