# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-07-21 14:27:14"

import re
import unreal
import inspect
import builtins

(bp,) = unreal.EditorUtilityLibrary.get_selected_assets()
bp_gc = unreal.load_object(None, "%s_C" % bp.get_path_name())
bp_cdo = unreal.get_default_object(bp_gc)

@unreal.uclass()
class TempObj(unreal.Object):
    pass

map = {
    "IntProperty":int,
    "StrProperty":str,
    "ArrayProperty":list,
    "Object":TempObj
}
def guess_call(obj, name, num=999):
    # obj.call_method(name, (unreal.World(),''))
    # return
    regx = r"takes at most (\d+) argument"
    try:
        obj.call_method(name, tuple([i for i in range(num)]))
    except Exception as e:
        error = str(e)
        print(error)
        match = re.search(regx, error)
        assert match,u"找不到函数"
        count = int(match.group(1))
    
    print("count",count)
    regx = re.compile(r"allowed Class type: '(\D+?)'")
    regx2 = re.compile(r"NativizeProperty: Cannot nativize '(\D+)' as '(\D+)' \((\D+)\)")
    args = tuple()
    for i in reversed(range(count)):
        try:
            print(args)
            obj.call_method(name, args + tuple([None for j in range(i + 1)]))
            args += (1,)
        except Exception as e:
            error = str(e)
            # print(error)
            match = regx.search(error)
            typ_string = match.group(1) if match else regx2.search(error).group(3)
            typ = getattr(unreal,typ_string,None)
            # print(typ_string)
            # print(map.get(typ_string))
            typ = map.get(typ_string,getattr(builtins,typ_string,getattr(unreal,typ_string,lambda:[])))
            args += (typ(),)
            
    print('call',args)
    obj.call_method(name, args=tuple(reversed(args)))

guess_call(bp_cdo, "MyCall")
# guess_call(bp_cdo, "生成死亡渐隐材质")


# # NOTE 获取 component
# face = bp_cdo.get_editor_property("FaceRender")
# print(face.get_name())
