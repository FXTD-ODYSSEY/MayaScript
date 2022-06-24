# -*- coding: utf-8 -*-
"""
same name object return long name in Maya
long name contain `|` splitter
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-06-16 16:26:03'


from maya import cmds

for sel in cmds.ls():
    if '|' in sel:
        print(sel)

