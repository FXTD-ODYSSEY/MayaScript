# coding:utf-8
from __future__ import division, print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-05-10 12:00:04"

"""
选择一个物体，获取物体之下的子物体 转为json存储
"""

from collections import defaultdict

import pymel.core as pm
import pymel.core.nodetypes as nt
import json


def is_iterable(obj):
    if isinstance(obj, str):
        return False
    try:
        return iter(obj)
    except TypeError:
        return False


def to_hierarchy_tree(objects, is_json=False, callback=None, depth=0):
    tree = defaultdict(dict)
    objects = objects if isinstance(objects, list) else [objects]
    for obj in objects:
        obj = pm.PyNode(obj)
        _obj = str(obj)
        for child in obj.getChildren(type="transform"):
            callable(callback) and callback(child, depth)
            if child.getChildren(type="transform"):
                tree[_obj].setdefault("groups", {})
                tree[_obj]["groups"][str(child)] = to_hierarchy_tree(
                    child, callback=callback,depth=depth + 1
                )
            else:
                tree[_obj].setdefault("children", [])
                tree[_obj]["children"].append(str(child))

    return json.dumps(tree) if is_json else tree


def hierarchy2json(parents, dump2json=True, tree=None, init=True):
    parents = parents if isinstance(parents, list) else [parents]
    _tree = (
        {str(p): {} if isinstance(p, nt.Transform) else p.type() for p in parents}
        if not isinstance(tree, dict)
        else tree
    )

    for parent in parents:
        tree = _tree[str(parent)] if init else _tree
        for child in parent.getChildren():
            tree[str(child)] = {} if isinstance(child, nt.Transform) else child.type()
            hierarchy2json(child, tree=tree[str(child)], init=False)

    if init:
        return json.dumps(_tree) if dump2json else _tree


# for sel in pm.selected():
#     print(json.dumps(hierarchy2json(sel)))

# print((hierarchy2json(pm.selected())))
print(to_hierarchy_tree(pm.selected(), True, callback=lambda c, i: print(i)))
