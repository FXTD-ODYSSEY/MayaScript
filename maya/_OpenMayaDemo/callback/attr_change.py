# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-11-18 15:13:14"


import pymel.core as pm
from maya import OpenMaya

root = pm.PyNode("callbackNode1")
attr_change_cb = OpenMaya.MNodeMessage.addAttributeChangedCallback


def change_call(msg, src, dst, data):
    # print("msg", msg)
    # print("src", src)
    # print("dst", dst)
    # print("data", data)
    
    flag = 0
    flags = [
        # "kConnectionMade",
        # "kConnectionBroken",
        # "kAttributeEval",
        "kAttributeSet",
    ]
    for f in flags:
        flag |= getattr(OpenMaya.MNodeMessage, f)

    
    print(msg)
    # if msg & flag:
    #     data = root.ikrefarray_proxy.get()
    #     root.ikrefarray.set(",".join({str(d) for d in data}))


cb_id = attr_change_cb(root.__apimobject__(), change_call, root)
# OpenMaya.MMessage.removeCallback(cb_id)

# print(OpenMaya.MNodeMessage.kConnectionBroken)
# print(OpenMaya.MNodeMessage.kConnectionMade)
# print(msg & OpenMaya.MNodeMessage.kConnectionMade|OpenMaya.MNodeMessage.kConnectionBroken)
