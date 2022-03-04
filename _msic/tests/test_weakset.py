import weakref
class Test():
    pass

a = Test()
test_list = weakref.WeakSet()
test_list.add(a)


del a 
print(len(test_list))
