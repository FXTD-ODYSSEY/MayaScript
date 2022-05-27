from addict import Addict
import attr
from glom import glom
from glom import SKIP


@attr.s
class Person(Addict):
    name = attr.ib()
    age = attr.ib()


person_data = [("Tony", 35), ("Lisa", 32), ("Michael", 37), ("Gabe", 30)]
target = [Person(name=name, age=age) for name, age in person_data]
spec = [lambda obj: obj if obj.age > 33 else SKIP]
resp = glom(target, spec)
print(resp)
