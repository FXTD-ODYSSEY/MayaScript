from cerberus import Validator
import attr
from addict import Dict


@attr.s
class Person(Dict):
    name = attr.ib(default="")
    age = attr.ib(default=0)
    sex = attr.ib(default="as")


class MyNormalizer(Validator):
    def __init__(self, *args, **kwargs):
        super(MyNormalizer, self).__init__(*args, **kwargs)

    def _normalize_coerce_person(self, value):
        return Person(**value)


schema = {"person": {"type": "dict", "coerce": "person"}}
v = MyNormalizer(schema)

document = {"person": {"name": "asd", "age": 12, "sex": "male"}}

res = v.validate(document)
print(res)
