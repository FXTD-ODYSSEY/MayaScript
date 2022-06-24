# -*- coding: utf-8 -*-
""""""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-06-10 13:48:04'


import attr
import threading
from addict import Dict


def on_setattr(attrib):
    def decorator(func):
        attrib.on_setattr = func
    return decorator

@attr.s
class Person(Dict):
    name = attr.ib(default="")
    age = attr.ib(default=0)
    @on_setattr(age)
    def _(self, attr,value):
        print("age",attr, value)
        threading.Timer(.1, lambda:print("later call",self.age)).start()
        return value
    sex = attr.ib(default="as")


# @attr.s
# class TestPersoon(Person):
#     work = attr.ib(default="student")

if __name__ == "__main__":
    person = Person("John", 18)
    person.age = 123
    print(person.age)
