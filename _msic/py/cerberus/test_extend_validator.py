# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-03-04 22:33:06"

from cerberus import Validator
from cerberus.validator import InspectedValidator
from cerberus import TypeDefinition
import attr


@attr.s
class Person(object):
    name = attr.ib(default="")
    age = attr.ib(default=0)
    sex = attr.ib(default="as")
    
class AdamValidator(Validator):
    pass
    # def _validate_skip_except(self, constraint, field, value):
    #     """Validate skip field.

    #     Args:
    #         constraint (callable): validate function to skip.
    #         field (str): schema field.
    #         value (str): actual value.
    #     """
    #     if not isinstance(value, constraint):
    #         self.is_skip = True

    # def _validate_test(self,*args):
    #     print("validate test",args)

# AdamValidator._validate_test = lambda *args: print("validate lambda",args)
AdamValidator = type(AdamValidator.__name__,(AdamValidator,),{"_validate_test":lambda *args: print("validate lambda",args)})
schema = {"person": {"test": "123"}}
v = AdamValidator(schema)


document = {"person": Person(**{"name": "asd", "age": 12, "sex": "male"})}

# document = {"person": "as"}

res = v.validate(document)
print(res)
print(v.document)
print(v.errors)
