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
from cerberus import TypeDefinition
import attr


@attr.s
class Person(object):
    name = attr.ib(default="")
    age = attr.ib(default=0)
    sex = attr.ib(default="as")
    
@attr.s
class AdamValidator(Validator):
    
    def _validate_type_skip(self, value):
        self.is_skip = False
        return True

    def _validate_skip_except(self, constraint, field, value):
        """Validate skip field.

        Args:
            constraint (callable): validate function to skip.
            field (str): schema field.
            value (str): actual value.
        """
        if not isinstance(value, constraint):
            self.is_skip = True


schema = {"person": {"type": "skip", "skip_except": (Person)}}
v = AdamValidator(schema)


document = {"person": Person(**{"name": "asd", "age": 12, "sex": "male"})}

# document = {"person": "as"}

res = v.validate(document)
print(res)
print(v.document)
print(v.errors)
print(v.is_skip)
