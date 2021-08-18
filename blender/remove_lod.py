# -*- coding: utf-8 -*-
"""
清理 后缀为 LOD1 等的 mesh
# ! 不需要了，因为 Unreal 可以不导出 LOD
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-17 14:08:01'

import re
import bpy


objs = bpy.data.objects
for obj in bpy.context.selectable_objects:
    if obj.type == "MESH" and re.search(r"LOD[1-9]$",obj.name):
        objs.remove(obj, do_unlink=True)
        
        