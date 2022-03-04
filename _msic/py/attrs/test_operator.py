import attr
import itertools
from addict import Dict
@attr.s
class TestClass(Dict):

    def __sub__(self, other):
        print("sub")
        return 1
        # return self.val - other.val

a = TestClass()
b = TestClass()
val = a-b
print(val)

for attribute,axis in itertools.product("trs","xyz"):
    print(attribute,axis)