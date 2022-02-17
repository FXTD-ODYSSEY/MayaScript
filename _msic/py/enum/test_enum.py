from enum import Enum
from enum import auto
import inspect
from collections import namedtuple

class Shapes(Enum):
    rectangle = auto()
    square = auto()
    circle = auto()

print(str(Shapes.rectangle.name))

class ParentA(object):
    def test(self):
        print("ParentA")
class ParentB(object):
    def test(self):
        print("ParentB")

class Child(ParentA, ParentB):
    pass

a = Child()
print(a.test())

class MyEnum(str,Enum):
    state1 = 'state1'
    state2 = 'state2'

print(MyEnum.state1)

MyEnum = namedtuple(
    "MyEnum", ["state1", "state2"]
)

data = MyEnum().state1
print(data)
