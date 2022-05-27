from pydash import py_
import toolz

@toolz.curry
class Test(object):
    def __init__(self, a, b):
        print(a, b)

# test = Test(1, 2)

@toolz.curry
def test_call(a,b):
    print(a,b)


test_call(1)(2)
res = Test(1,2)
print(res)
