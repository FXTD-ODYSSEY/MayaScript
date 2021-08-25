# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-08-19 16:03:23"


import bpy
from collections import defaultdict


def delete_hierarchy(obj):
    # https://blender.stackexchange.com/questions/44653
    obj.select_set(True)
    def get_child_names(obj):
        for child in obj.children:
            child.select_set(True)
            if child.children:
                get_child_names(child)

    get_child_names(obj)
    bpy.ops.object.delete()


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


def main():

    # NOTE  导入 FBX 文件
    fbx_path = r"G:\file_test\2021-08-17\Char_ouputTest_rig.fbx"
    bpy.ops.import_scene.fbx(filepath=fbx_path)

    obj_list = defaultdict(list)
    parent = None
    for obj in bpy.context.selected_objects:
        obj_list[obj.type].append(obj)
        if not obj.parent and len(obj.children):
            parent = obj

    assert obj_list["ARMATURE"], u"找不到骨架"
    bpy.ops.object.select_all(action="DESELECT")
    count = 0
    armature = None
    for a in obj_list["ARMATURE"]:
        if len(a.pose.bones) > count:
            armature = a

    armature.select_set(True)
    bpy.ops.object.parent_clear(type="CLEAR")
    for child in armature.children:
        if child in obj_list["MESH"]:
            obj_list["MESH"].remove(child)

    # NOTE 复制 mesh 并且 parent 到世界坐标
    for mesh in obj_list["MESH"]:
        bpy.ops.object.select_all(action="DESELECT")
        mesh.select_set(True)
        bpy.ops.object.duplicate(linked=True)
        src = bpy.context.selected_objects[0]
        armature.select_set(True)
        # NOTE 重新蒙皮
        bpy.ops.object.parent_set(type='ARMATURE')
        bpy.ops.object.select_all(action="DESELECT")
        # # NOTE 拷贝权重
        # copy_weight(mesh,src)
    
    delete_hierarchy(parent)

    # NOTE 导入动画文件
    fbx_path = r"G:\file_test\2021-08-17\Char_ouputTest_pose.FBX"
    bpy.ops.import_scene.fbx(filepath=fbx_path)
    anim = bpy.context.selected_objects[0]
    armature.select_set(True)
    anim.select_set(True)
    bpy.ops.object.make_links_data(type='ANIMATION')
    
    bpy.ops.object.select_all(action="DESELECT")
    anim.select_set(True)
    bpy.ops.object.delete()
    
bpy.ops.scene.new()
main()