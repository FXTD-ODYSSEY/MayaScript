# -*- coding: utf-8 -*-
"""
罗列 FBX IO 属性
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-06-02 19:48:31'

import fbx
import time

manager = fbx.FbxManager.Create()
ios = fbx.FbxIOSettings.Create(manager, fbx.IOSROOT)
prop = ios.RootProperty
prop_name = prop.GetHierarchicalName()

curr = time.time()
while str(prop_name):
    prop = ios.RootProperty.GetNextDescendent(prop)
    prop_name = prop.GetHierarchicalName()
    # TODO 获取类型
    prop_type = prop.GetPropertyDataType()
    print("%s = %s" % (prop_name,prop_type.GetName()))

