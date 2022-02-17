from dependencies import operation
from dependencies import Injector



class Container(Injector):

    foo = 1
    bar = 2

    @operation
    def process(foo, bar, baz=3):
        return foo + bar + baz

    @operation
    def test(process):
        return process()

a = Container.test()
print(a)
