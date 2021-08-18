# -*- coding: utf-8 -*-
"""
C:\Program Files\Blender Foundation\Blender 2.91\2.91\scripts\addons\space_view3d_copy_attributes.py

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-08-17 14:16:41"


import bpy

# o = bpy.context.object

# # NOTE 复制模型
# duplicate_obj = bpy.ops.object.duplicate({"object": o}, linked=True)
# # NOTE 获取复制的模型
# o = bpy.context.object
# print(o)

# # NOTE 设置 parent
# bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)


print(bpy.context.selected_objects)

def copy_weight(ob, active):
    me_source = active.data
    me_target = ob.data
    # sanity check: do source and target have the same amount of verts?
    if len(me_source.vertices) != len(me_target.vertices):
        return ("ERROR", "objects have different vertex counts, doing nothing")
    vgroups_IndexName = {}
    for i in range(0, len(active.vertex_groups)):
        groups = active.vertex_groups[i]
        vgroups_IndexName[groups.index] = groups.name
    data = {}  # vert_indices, [(vgroup_index, weights)]
    for v in me_source.vertices:
        vg = v.groups
        vi = v.index
        if len(vg) > 0:
            vgroup_collect = []
            for i in range(0, len(vg)):
                vgroup_collect.append((vg[i].group, vg[i].weight))
            data[vi] = vgroup_collect
    # write data to target
    if ob != active:
        # add missing vertex groups
        for vgroup_name in vgroups_IndexName.values():
            # check if group already exists...
            already_present = 0
            for i in range(0, len(ob.vertex_groups)):
                if ob.vertex_groups[i].name == vgroup_name:
                    already_present = 1
            # ... if not, then add
            if already_present == 0:
                ob.vertex_groups.new(name=vgroup_name)
        # write weights
        for v in me_target.vertices:
            for vi_source, vgroupIndex_weight in data.items():
                if v.index == vi_source:

                    for i in range(0, len(vgroupIndex_weight)):
                        groupName = vgroups_IndexName[vgroupIndex_weight[i][0]]
                        groups = ob.vertex_groups
                        for vgs in range(0, len(groups)):
                            if groups[vgs].name == groupName:
                                groups[vgs].add(
                                    (v.index,), vgroupIndex_weight[i][1], "REPLACE"
                                )
    return ("INFO", "Weights copied")
