# -*- coding: utf-8 -*-
"""
测试 Python 的导入方法
1. 如何让 from module_test import abc 不报错 (在没有具体文件的情况下)
q1_solution1
q1_solution2
q1_solution3 (不支持 py2)

2. 导入 module 的时候，属性不存在返回默认值
q2_solution1 (不支持 py2)

参考:
https://stackoverflow.com/a/7668273

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-12-05 20:05:26"

import os
import sys
import pkgutil
from functools import partial
from types import ModuleType
from pkgutil import walk_packages

MODULE = os.path.dirname(os.path.abspath(__file__))
MODULE not in sys.path and sys.path.insert(0, MODULE)

import module_test


def q1_solution1():
    # NOTE __path__ 添加多个路径会类似 sys.path 一样自动搜索
    module_test.__path__.append(MODULE)
    from module_test import abc

    print("abc", abc)


def q1_solution2():
    module_test.__dict__.update({"abc": 1})
    from module_test import abc

    print("abc", abc)


def q1_solution3():
    """
    这个方法不兼容 py2
    """
    sys.modules["module_test.abc"] = 1
    from module_test import abc

    print("abc", abc)


def q2_solution1():
    """
    (不支持 py2)
    """
    import module_test

    def get_attr(module, name):
        print(name)
        try:
            return __import__(module.__name__ + "." + name)
        except ImportError:
            return None

    module_test.__dict__.update({"__getattr__": partial(get_attr, module_test)})

    import module_test.abc

    # from module_test import abc
    from module_test import view

    print("abc", abc)
    print("view", view)

    from module_test import model

    model.__dict__.update({"__getattr__": partial(get_attr, model)})
    print(model.a)


def q2_solution2():
    def deco(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            print(args, res)
            return res

        return wrapper

    class ProxyModule(object):
        abc = 1

        def __init__(self, module):
            self.abc = 2
            self.module = module
            list(walk_packages(module.__path__, module.__name__ + "."))
            self.__dict__.update(module.__dict__)
            
            for name in sys.modules:
                if name.startswith("module_test"):
                    print(name)

        # @deco
        def __getattribute__(self, name):
            print("__getattribute__", name)
            return super(ProxyModule, self).__getattribute__(name)

        def __getattr__(self, name):
            try:
                return super(ProxyModule, self).__getattr__(name)
            except AttributeError:
                return "1"

    sys.modules["module_test"] = ProxyModule(sys.modules["module_test"])
    # import module_test.abc as abc

    # print(abc)
    from module_test import abc

    print("abc", abc)
    from module_test import view

    print("view", view)

    import module_test

    print(module_test)


def test_multi_api():
    from multi_api import utils

    print(utils.display_info)


if __name__ == "__main__":
    test_multi_api()
