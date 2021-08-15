# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-11 23:17:48'

import unreal

# path = '/Script/CoreUObject.Object:ExecuteUbergraph'
path = '/Game/ArtResources/Characters/T1ani/A040419/A070/NewEditorUtilityBlueprint.SKEL_NewEditorUtilityBlueprint_C:MyCall'

obj = unreal.load_object(None,path)
print(obj)
print(unreal.EditorLevelLibrary.get_selected_level_actors)
# print(obj.call_method('GetReturnProperty'))
# print(dir(obj))
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_post_init', '_wrapper_meta_data', 'call_method', 'cast', 'get_class', 'get_default_object', 'get_editor_property', 'get_fname', 'get_full_name', 'get_name', 'get_outer', 'get_outermost', 'get_path_name', 'get_typed_outer', 'get_world', 'modify', 'rename', 'set_editor_properties', 'set_editor_property', 'static_class']