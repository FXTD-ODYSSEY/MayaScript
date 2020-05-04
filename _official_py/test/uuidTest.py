# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 15:25:46'

"""
https://stackoverflow.com/questions/41186818/how-to-generate-a-random-uuid-which-is-reproducible-with-a-seed-in-python
"""
import uuid
import random

rd = random.Random()
rd.seed(1)
print (rd.getrandbits(128))
print (uuid.UUID(int=rd.getrandbits(128)))


import hashlib
import uuid

m = hashlib.md5()
seed = '2'
m.update(seed.encode('utf-8'))
new_uuid = uuid.UUID(m.hexdigest())

print(new_uuid)