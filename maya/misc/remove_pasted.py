# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-25 14:38:10'



from maya import cmds
prefix = "pasted__"
for sel in cmds.ls():
    if sel.startswith(prefix):
        print(sel)
        
