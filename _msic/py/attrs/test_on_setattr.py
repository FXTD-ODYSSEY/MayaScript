import attr
from attr import validators
from addict import Dict
# from typing import data
from six.moves import builtins

class Person(Dict):
    name = attr.ib(default="")
    age = attr.ib(default=0)
    sex = attr.ib(default="as")

    def test(self):
        print("test call")
        
    def __setattr__(self, name, value):
        super(Person, self).__setattr__(name, value)
        if name == "age":
            pass
Person = attr.s(Person)

# @attr.s
# class TestPersoon(Person):
#     work = attr.ib(default="student")

if __name__ == "__main__":
    person = Person("John",18)
    person.age = 123
    print(person.age)
    print(person.get("age"))
    print(person.sex)
    print(person.get("age"))
