import weakref
from addict import Dict
class Test():
    pass

a = Test()
test_list = weakref.WeakSet()
test_list.add(a)


del a 
print(len(test_list))


class PoseItemTypes(dict):
    group = "group"
    pose = "pose"
    psd = "psd"
    

print(PoseItemTypes())




