# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-08-11 23:16:13'


import os
import json
import unreal
red_lib = unreal.RedArtToolkitBPLibrary

objects = red_lib.get_all_objects()
# objects = red_lib.get_all_properties()
# print(len(objects))
path_list = []
for obj in objects:
    try:
        path_list.append(obj.get_path_name())
    except:
        print("error -> %s" % obj)

path_list = [func.get_path_name() for func in red_lib.get_all_functions()]
path = r"G:\RedApp\Plugins\RedArtToolkit\tmp\object_list.json"
with open(path,'w',encoding="utf-8") as f:
    json.dump(path_list,f,ensure_ascii=False,indent=4)   

os.startfile(path)
