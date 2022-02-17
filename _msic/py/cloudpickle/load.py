# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-02-09 15:36:59'

import io
import os
import cloudpickle

import cloudpickle
squared = lambda x: x ** 2
pickled_lambda = cloudpickle.dumps(squared)

import pickle
new_squared = pickle.loads(pickled_lambda)
value = new_squared(2)
print(value)


path = r"F:\repo\MayaScript\_msic\py\cloudpickle\data"
with io.open(path, 'r',encoding='utf8') as f:
    data = cloudpickle.load(f)
    print(data)



