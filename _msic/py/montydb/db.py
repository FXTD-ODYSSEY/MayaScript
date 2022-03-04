# -*- coding: utf-8 -*-
"""

"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-01-20 16:51:18"

# Import third-party modules
from montydb import MontyClient
from addict import Dict
import json
import os

# DIR = os.path.dirname(os.path.abspath(__file__))

client = MontyClient(":memory:")
db = client["runoobdb"]

# db.drop_collection("data")

data_collection = db["data"]

extra = Dict()
extra.a = 1
extra.b = "asd"


class DB(Dict):
    def __init__(self):
        self.test2 = 1
        self.abc = "abc"
        self["asd a"] = 1

    def test(self):
        print("test call")


data = DB()
print(data.asd_assemblyDefinitiond)
data.extra = extra

x = data_collection.insert_one(data)
myquery = {"abc": "abc"}
newvalues = {"$set": {"alexa": "12345"}}
data_collection.update_one(myquery, newvalues)
mydoc = data_collection.find(myquery)
for x in mydoc:
    print(x)
    print(data)
    # print(x["alexa"])
    # print(data.test())
