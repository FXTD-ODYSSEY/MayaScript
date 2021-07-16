# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-02 11:03:01'

"""
# NOTE https://stackoverflow.com/questions/45764093/
"""

from maya import cmds
from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui

def hierarchyTree(parent, tree):
    children = cmds.listRelatives(parent, c=True, type='transform')
    if children:
        tree[parent] = (children, {})
        for child in children:
            hierarchyTree(child, tree[parent][1])
    else:
        del tree

def retrive2Jnt(tree,jnt_list=[]):
    for parent, data in tree.items():

        # NOTE 首个 parent 节点的附加判断
        parent_jnt = "%s_jnt" % parent
        if not cmds.objExists(parent_jnt):
            cmds.select(cl=1)
            parent_jnt = cmds.joint(n=parent_jnt)
            jnt_list.append((parent_jnt,parent))
            cmds.parentConstraint(parent,parent_jnt)

        children, child_tree = data
        for child in children:
            # if not cmds.keyframe(child, q=True):
            #     continue
            cmds.select(cl=1)
            child_jnt = cmds.joint(n="%s_jnt" % child)
            jnt_list.append((child_jnt,child))
            cmds.parentConstraint(child,child_jnt)
            cmds.parent(child_jnt,parent_jnt)
            
        retrive2Jnt(child_tree,jnt_list)

def main():
    hierarchy_tree = {}
    sel_list = cmds.ls(sl=1)
    if not sel_list:
        msg = u"请选择一个带模型动画的组"
        QtWidgets.QMessageBox.warning(QtWidgets.QApplication.activeWindow(),u"警告",msg)
        return

    hierarchyTree(cmds.ls(sl=1)[0],hierarchy_tree)

    if hierarchy_tree:
        jnt_obj_list = []
        retrive2Jnt(hierarchy_tree,jnt_obj_list)

        # NOTE bake 关键帧
        start_time = cmds.playbackOptions(q=1,min=1)
        end_time = cmds.playbackOptions(q=1,max=1)
        jnt_list = [jnt for jnt,obj in jnt_obj_list]
        cmds.bakeResults(jnt_list,
            simulation=False, 
            t=(start_time,end_time)
        )

        # NOTE 删除约束
        top_jnt = jnt_list[0]
        con_list = cmds.ls(top_jnt,dag=1,ni=1,type="constraint")
        cmds.delete(con_list)
        
        # NOTE 绑定骨骼
        for jnt,obj in jnt_obj_list:
            try:
                # NOTE 清理物体本身的关键帧 | 否则物体会乱飞
                cmds.cutKey(obj,clear=1)
                # NOTE 添加蒙皮
                cmds.skinCluster( jnt, obj, 
                    dr=4,
                    bindMethod=0,
                    toSelectedBones=1,
                )   
            except:
                pass


# import sys
# MODULE = r"F:\MayaTecent\MayaScript\anim"
# if MODULE not in sys.path:
#     sys.path.append(MODULE)

# import convertMeshAnim2JntBind
# reload (convertMeshAnim2JntBind)
# convertMeshAnim2JntBind.main()