# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-10 12:00:04'

"""
选择一个物体，获取物体之下的子物体 转为json存储
"""

import pymel.core as pm
import pymel.core.nodetypes as nt
import json

def hierarchy2json(parents,tree=None,init=True):
    parents = parents if isinstance(parents,list) else [parents]
    _tree = {str(p):{} if isinstance(p,nt.Transform) else p.type() for p in parents} if not isinstance(tree,dict) else tree

    for parent in parents:
        tree = _tree[str(parent)] if init else _tree
        for child in parent.getChildren(ni=1):
            tree[str(child)] = {} if isinstance(child,nt.Transform) else child.type()
            hierarchy2json(child,tree[str(child)],False)

    if init:
        return json.dumps(_tree)

# for sel in pm.selected():
#     print(json.dumps(hierarchy2json(sel)))

print((hierarchy2json(pm.selected())))
