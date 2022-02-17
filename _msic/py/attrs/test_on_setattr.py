import attr
from attr import validators
from addict import Dict
# from typing import data
from six.moves import builtins

@attr.s
class Person(Dict):
    name = attr.ib(default="")
    age = attr.ib(default=0,on_setattr=lambda:print('ad'))
    sex = attr.ib(default="as")

    def test(self):
        print("test call")
        
# @attr.s
# class TestPersoon(Person):
#     work = attr.ib(default="student")

if __name__ == "__main__":
    person = Person("John",18)
    person.age = 123
