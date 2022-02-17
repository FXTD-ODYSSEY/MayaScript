from cerberus import Validator
import attr
from addict import Dict
from cerberus import schema_registry


@attr.s
class Person(Dict):
    name = attr.ib(default="")
    age = attr.ib(default=0)
    sex = attr.ib(default="as")
    children = attr.ib(default=[])


class MyNormalizer(Validator):
    def __init__(self, *args, **kwargs):
        super(MyNormalizer, self).__init__(*args, **kwargs)

    def _normalize_coerce_adam_pose_children(self, value):
        print(value)
        data = Person()
        data.name = 'asd'
        data.sex = 'female'
        return data
        # return [Person(**person) for person in value]


schema = {"children": {"type": "list", "coerce": "adam_pose_children"}}

schema = {
    "name": {"type": "string", "required": True, "minlength": 2},
    "sex": {"type": "string", "required": True},
    "age": {"type": "integer"},
    "children": {
        "type": "list",
        "schema": {
            "type": "dict",
            "coerce": "adam_pose_children",
            "schema": "adam_pose_children",
        },
    },
}


document = {
    "name": "tim",
    "age": 12,
    "sex": "male",
    "children": [
        {
            "name": "tim",
            "age": 22,
            "sex": "male",
        },
        {
            "name": "jimmy",
            "age": 23,
            "sex": "male",
        },
    ],
}

schema_registry.add(
    "adam_pose_children",
    schema,
)


v = MyNormalizer(schema)


res = v.validate(document)
print(v.errors)
res = v.normalized(document)
print(res)
