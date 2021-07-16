# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-02 11:03:01'

"""
# NOTE https://stackoverflow.com/questions/45764093/
"""
import math
import pymel.core as pm
import pymel.core.datatypes as dt

def generateCubeFromVector(start_pt, end_pt, distant=3, angle=45):
    x_vec = start_pt - end_pt

    y_vec = start_pt.cross(end_pt)
    if angle:
        # NOTE 角度转弧度
        angle = angle*math.pi/180
        y_vec = y_vec.rotateBy(x_vec, angle)
    y_vec.normalize()

    z_vec = x_vec.cross(y_vec)
    z_vec.normalize()

    # NOTE 计算8个顶点坐标位置
    start_corner_1 = start_pt+y_vec*distant
    start_corner_2 = start_pt-y_vec*distant
    start_corner_3 = start_pt+z_vec*distant
    start_corner_4 = start_pt-z_vec*distant

    end_corner_1 = end_pt+y_vec*distant
    end_corner_2 = end_pt-y_vec*distant
    end_corner_3 = end_pt+z_vec*distant
    end_corner_4 = end_pt-z_vec*distant

    # NOTE 生成方块曲线
    return pm.curve(d=1,p=[
        start_corner_1,
        start_corner_3,
        start_corner_2,
        start_corner_4,
        start_corner_1,
        end_corner_1,
        end_corner_3,
        end_corner_2,
        end_corner_4,
        end_corner_1,
        end_corner_4,
        start_corner_4,
        start_corner_2,
        end_corner_2,
        end_corner_3,
        start_corner_3,
    ])
    
def hierarchyTree(parent, tree):
    children = pm.listRelatives(parent, c=True, type='joint')
    if children:
        tree[parent] = (children, {})
        for child in children:
            hierarchyTree(child, tree[parent][1])
    else:
        del tree

def retrive2Jnt(tree,ctrl_list=[]):
    for parent, data in tree.items():

        # NOTE 首个 parent 节点的附加判断
        parent_ctrl = "%s_ctrl" % parent
        if not pm.objExists(parent_ctrl):
            parent_ctrl = pm.curve(ch=0,n=parent_ctrl)[0]
            pm.group(parent_ctrl,n=parent_ctrl+"_grp")
            ctrl_list.append((parent_ctrl,parent))
            pm.parentConstraint(parent,parent_ctrl)

        children, child_tree = data
        for child in children:
            child_ctrl = pm.circle(ch=0,n="%s_ctrl" % child)[0]
            pm.group(child_ctrl,n=child_ctrl+"_grp")
            ctrl_list.append((child_ctrl,child))
            pm.parentConstraint(child,child_ctrl)
            pm.parent(child_ctrl,parent_ctrl)
            
        retrive2Jnt(child_tree,ctrl_list)

def main():
    hierarchy_tree = {}
    sel_list = pm.ls(sl=1)
    if not sel_list:
        msg = u"请选择一个骨骼"
        pm.headsUpMessage(msg)
        return

    hierarchyTree(pm.ls(sl=1)[0],hierarchy_tree)
    retrive2Jnt(hierarchy_tree)

if __name__ == "__main__":

    try:
        main()
    except:
        import traceback
        traceback.print_exc()
    # if hierarchy_tree:
    #     jnt_obj_list = []
    #     retrive2Jnt(hierarchy_tree,jnt_obj_list)

    #     # NOTE bake 关键帧
    #     start_time = pm.playbackOptions(q=1,min=1)
    #     end_time = pm.playbackOptions(q=1,max=1)
    #     ctrl_list = [jnt for jnt,obj in jnt_obj_list]
    #     pm.bakeResults(ctrl_list,
    #         simulation=False, 
    #         t=(start_time,end_time)
    #     )

    #     # NOTE 删除约束
    #     top_jnt = ctrl_list[0]
    #     con_list = pm.ls(top_jnt,dag=1,ni=1,type="constraint")
    #     pm.delete(con_list)
        
    #     # NOTE 绑定骨骼
    #     for jnt,obj in jnt_obj_list:
    #         try:
    #             # NOTE 清理物体本身的关键帧 | 否则物体会乱飞
    #             pm.cutKey(obj,clear=1)
    #             # NOTE 添加蒙皮
    #             pm.skinCluster( jnt, obj, 
    #                 dr=4,
    #                 bindMethod=0,
    #                 toSelectedBones=1,
    #             )   
    #         except::
    import traceback
    traceback.print_exc()
    #             pass


# import sys
# MODULE = r"F:\MayaTecent\MayaScript\anim"
# if MODULE not in sys.path:
#     sys.path.append(MODULE)

# import convertMeshAnim2JntBind
# reload (convertMeshAnim2JntBind)
# convertMeshAnim2JntBind.main()