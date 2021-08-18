# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-18 14:00:19'

import time
import unreal
from unreal import SystemLibrary as sys_lib
from unreal import EditorLevelLibrary as level_lib
cur = time.time()

@unreal.uclass()
class TestObject(unreal.Object):
    world = level_lib.get_editor_world()
    # NOTE 蓝图库分类设置为 Python Blueprint
    @unreal.ufunction(static=True)
    def timer_call():
        print("timer_call")
        
    @unreal.ufunction(ret=unreal.World)
    def get_world(cls):
        return cls.world


obj = TestObject()
print(obj.get_world())    
        
# def callback(*args):
#     print(args)
#     elapsed = time.time() - cur
#     print("callback %s" % elapsed)

# delegate = unreal.TimerDynamicDelegate()
# delegate.bind_callable(callback)

# handle = sys_lib.set_timer_delegate(delegate,3,False)
handle = sys_lib.set_timer(obj,"timer_call",3,False)


