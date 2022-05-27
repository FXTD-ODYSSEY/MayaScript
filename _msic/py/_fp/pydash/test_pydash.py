from pydash import py_
from fn import _ as X
from pydash import stub_true
from pydash import stub_false
from pydash import matches
from pydash import constant
from pydash import cond

# doubler = iterated(lambda x: x * 2)
# value = doubler(5, 5)
# print(value)
# print(8*32)
# print(4*2**5)
# [
#     [matches({"a": 1}), constant("matches A")],
#     [matches({"b": 2}), constant("matches B")],
#     [stub_true, lambda value: value],
# ]

# value = py_("test").is_instance_of(str).value()
# print(value)


class Test(object):
    def print(self):
        print("hello")
instance = Test()

func = py_().tap(lambda x: x.print())
print(func(instance))
print(py_())

