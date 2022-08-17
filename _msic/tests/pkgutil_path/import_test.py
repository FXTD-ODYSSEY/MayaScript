import os
import sys

DIR = os.path.dirname(__file__)
for folder in ["a","b"]:
    path = os.path.join(DIR, folder)
    path not in sys.path and sys.path.insert(0,path)

from gg.maya import real
from gg.maya import test_maya

print(real)
print(test_maya)

import pkgutil
import gg
for finder,name,ispkg in pkgutil.walk_packages(gg.__path__,gg.__name__+'.'):
    print(finder,name,ispkg)

print('----------------------------------------')

from setuptools import find_packages

print(gg.__file__)
print(find_packages(os.path.dirname(gg.__file__)))

