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
