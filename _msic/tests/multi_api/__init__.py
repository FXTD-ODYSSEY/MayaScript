import os
from .py import *
from .constants import IS_MAYA
if IS_MAYA:
    from .maya import *
