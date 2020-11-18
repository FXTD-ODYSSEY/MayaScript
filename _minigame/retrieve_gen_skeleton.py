# -*- coding: utf-8 -*-
"""
遍历 locator 层级 生成骨骼
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-08 15:34:00'


from maya import cmds
import json

def hierarchyTree(parent, tree):
    children = cmds.listRelatives(parent, c=True, type='transform')
    if children:
        tree[parent] = (children, {})
        for child in children:
            hierarchyTree(child, tree[parent][1])
    else:
        del tree

def retrieve2Jnt(tree,jnt_list=[]):
    for parent, data in tree.items():

        parent_jnt = "%s_jnt" % parent
        if not cmds.objExists(parent_jnt):
            cmds.select(cl=1)
            parent_jnt = cmds.joint(n=parent_jnt)
            jnt_list.append((parent_jnt,parent))
            cmds.delete(cmds.parentConstraint(parent,parent_jnt))
            
        children, child_tree = data
        for child in children:
            cmds.select(cl=1)
            child_jnt = cmds.joint(n="%s_jnt" % child)
            jnt_list.append((child_jnt,child))
            cmds.delete(cmds.parentConstraint(child,child_jnt))
            cmds.parent(child_jnt,parent_jnt)
            
        retrieve2Jnt(child_tree,jnt_list)
  

def main():
        
    hierarchy_tree = {}
    hierarchyTree(cmds.ls(sl=1)[0],hierarchy_tree)

    if not hierarchy_tree:
        return

    jnt_obj_list = []
    retrieve2Jnt(hierarchy_tree,jnt_obj_list)
    # print(jnt_obj_list)

if __name__ == "__main__":
    main()

