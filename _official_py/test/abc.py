# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-12-14 16:05:59"

import inspect
from abc import abstractmethod
from abc import abstractproperty
from abc import ABCMeta
from types import FunctionType
import six


class TestBase(object):
    @property
    def WidgetDockMixin(self):
        return type("WidgetDockMixin", (), {})
    def abc_call(self):
        print("abc_call")

    def __getattr__(self, name):
        try:
            return super(TestBase, self).__getattr__(name)
        except AttributeError:
            # NOTES(timmyliang): accept any parameter
            kw = {"__init__": lambda *args, **kwargs: None}
            return type("%s_%s" % (self.__class__.__name__, name), (), kw)


class TestMeta(ABCMeta):
    def __new__(cls, name, bases, attrs):
        base = bases[0]
        if base is TestBase:
            for n, m in inspect.getmembers(base):
                if n.startswith("_"):
                    continue
                if inspect.ismethod(m):
                    attrs[n] = abstractmethod(m.im_func)
                elif isinstance(m, FunctionType):
                    attrs[n] = abstractmethod(m)
                elif isinstance(m, property):
                    attrs[n] = abstractproperty(m)
        else:
            cls.__check(list(bases))

        return super(TestMeta, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def __check(cls,base_list):
        index = base_list.index(TestAbstract)
        if index < 0:
            return 
        for n,m in inspect.getmembers(base_list.pop(index)):
            print(n,m)
        


class TestAbstract(six.with_metaclass(TestMeta, TestBase)):

    @abstractmethod
    def test2(self):
        print("test")


class Test(TestAbstract):
    WidgetDockMixin = 1
    def test2(self):
        print("test2")
        
    def abc_call(self):
        pass


a = Test()
# print(a.test2())
# a = tuple()
# itr = iter(a)
# print(next(itr,None))