# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, unicode_literals
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-11 22:48:59'

import unreal

@unreal.uclass()
class PyBPFunctionLibrary(unreal.BlueprintFunctionLibrary):
    # NOTE 蓝图库分类设置为 Python Blueprint
    @unreal.ufunction(static=True,meta=dict(Category="Python Blueprint"))
    def TestFunction():
        unreal.SystemLibrary.print_string(None,'Python Test Function Run',text_color=[255,255,255,255])

    @unreal.ufunction(params=[str],ret=str,static=True,meta=dict(Category="Python Blueprint"))
    def TestReadFile(filepath):
        if not os.path.exists(filepath):
            return ''
        with open(filepath,'r') as f:
            data = f.read()
        return data
    
# obj = PyBPFunctionLibrary()
# path = '/Game/ArtResources/Characters/Roles/Actor/Sanji01/BluePrints/Biz/Sanji01_St_Biz.Sanji01_St_Biz'
# obj = unreal.load_object(None,path)
# print(obj)
# print(unreal.get_blueprint_generated_types(path))

@unreal.uclass()
class Test(unreal.Object):
    pass

cls = unreal.generate_class(Test)
print(cls)
print(Test)

# print(obj.TestReadFile)
# print(type(obj.TestReadFile))
# print(dir(obj.TestReadFile))
# print(isinstance(obj.TestReadFile,unreal.Function))
# print(obj.TestReadFile.__signature__)
    
    