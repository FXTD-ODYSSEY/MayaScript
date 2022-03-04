# -*- coding: utf-8 -*-
"""

"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from pydoc import doc

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-03-03 10:50:07"


# Import built-in modules
import inspect

# Import third-party modules
from cerberus import Validator
import wrapt
from types import ModuleType


def validate_args(schema):
    @wrapt.decorator
    def decorator(func, instance, args, kwargs):
        document = inspect.getcallargs(func, *args, **kwargs)
        spec = inspect.getargspec(func)
        count = len(spec.defaults) if spec.defaults else 0
        start = 0
        if instance:
            start = 1
            document.pop(spec.args[0])
        _args = spec.args[start: -count] if count else spec.args
        varargs = document.pop(spec.varargs, ())
        keywords = document.pop(spec.keywords, {})
        document.update(keywords)
        validator = Validator(schema, allow_unknown=True)
        if not validator.validate(document):
            raise RuntimeError(validator.errors)
        document = validator.document.copy()
        arguments = tuple(document.pop(arg) for arg in _args) + varargs
        print(arguments, document)
        return func(*arguments, **document)

    return decorator


schema = {
    "flag": {
        "type": "boolean",
        "coerce": [str, lambda v: v.lower() in ("true", "1")],
    },
    "age": {"type": "integer", "min": 10},
}


@validate_args(schema)
def test_call(flag, age, b=1):
    print("test_call")
    print("flag", flag)


class TestClass(object):
    @validate_args(schema)
    @staticmethod
    def test_call_static(flag, age, b=1):
        print("test_call")
        print("flag", flag)

    @validate_args(schema)
    @classmethod
    def test_call_class(cls, flag, age, b=1):
        print("test_call")
        print("flag", flag)

    @validate_args(schema)
    def test_call(self, flag, age, b=1):
        print("test_call")
        print("flag", flag)


test_call("1", 11)
TestClass.test_call_static("1", 11)
TestClass.test_call_class("1", 11)

# inst = TestClass()
# inst.test_call(1, 11)


# @validate_args(
#     {
#         "module_name": {
#             "type": "string",
#             "coerce": (
#                 lambda module_name: module_name.__name__
#                 if isinstance(module_name, ModuleType)
#                 else module_name
#             ),
#         },
#     }
# )
# def module_test(module_name):
#     print(module_name)


# module_test(inspect)


# @validate_args(
#     {
#         "white_list": {
#             "type": "list",
#             "coerce": lambda value: value or [],
#         },
#     }
# )
# def test_list_args(white_list=None):
#     white_list.append(1)
#     return white_list


# @validate_args(
#     {
#         "white_list": {
#             "type": "list",
#             "coerce": lambda value: value or [],
#         },
#     }
# )
def test_asterisk_args(b, white_list, *args1, **kwargs2):
    print("args1", args1)
    print("kwargs2", kwargs2)
    return white_list


print(test_asterisk_args(1, [1], 32, a=1))
