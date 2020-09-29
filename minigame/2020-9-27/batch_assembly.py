# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-27 22:20:18'

import os
from pymel import core as pm

path = pm.sceneName()
DIR = os.path.dirname(path)
for f in os.listdir(DIR):
    if not f.endswith(".ma") and not f.endswith(".mb"):
        continue
    elif f == os.path.basename(path):
        continue
    
    assembly = pm.ls(sl=1,type="assemblyDefinition")

    pm.assembly(assembly, edit=True, createRepresentation='Scene',
                input=f.replace('\\','/'))