from addict import Dict
import attr
import json
import weakref

weak_set = weakref.WeakSet()

@attr.s
class AttrBase(object):
    name = attr.ib(default="")
    

@attr.s
class Group(AttrBase,Dict):
    children = attr.ib(factory=list)

    def append_child(self, child):
        self.children.append(child)


@attr.s
class Child(AttrBase,Dict):
    pass

grp = Group("Group")
# weak_set.add(grp)
grp.append_child(Child("child1"))
grp.append_child(Child("child2"))

print(grp)
print(json.dumps(grp))


a = b = c = {}

a['b'] = b
a['c'] = c

print(a)
print(json.dumps(a))
