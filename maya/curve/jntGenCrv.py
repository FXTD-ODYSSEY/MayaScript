# coding:utf 8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-20 09:30:27'

""" 
选择骨骼生成闭合曲线（生成的曲线可能无法按顺序_(:з」∠)_）
"""

import pymel.core as pm
import heapq

def getAdjacentJointOrder(jnt_list):
    # NOTE https://stackoverflow.com/questions/6880899/sort-a-set-of-3-d-points-in-clockwise-counter-clockwise-order
    # NOTE 获取位置数据
    jnt_dict = {jnt:jnt.getTranslation(space="world") for jnt in jnt_list}
    
    # NOTE 找到骨骼的中心点
    # NOTE 从离中心点最远的骨骼开始生成曲线
    center = sum(jnt_dict.values())/len(jnt_dict)
    dist_list = [{"joint":jnt,"distance":(center - jnt_dict[jnt]).length()} for jnt in jnt_dict]
    joint_list = heapq.nlargest(1,dist_list,key=lambda x:x["distance"])
    joint = joint_list[0]["joint"]
    order_jnt_list = [joint]

    while len(jnt_dict) > 1:
        
        # NOTE 获取上次的骨骼位置
        first = jnt_dict[joint]
        del jnt_dict[joint]
        
        # NOTE 获取当前骨骼之下距离最近的骨骼点
        dist_list = [{"joint":jnt,"distance":(first - jnt_dict[jnt]).length()} for jnt in jnt_dict if jnt not in order_jnt_list]
        joint_list = heapq.nsmallest(1,dist_list,key=lambda x:x["distance"])
        joint = joint_list[0]["joint"]

        order_jnt_list.append(joint)
        
    return order_jnt_list

def generateCrv():
    
    jnt_list = pm.ls(sl=1,type="joint")

    if len(jnt_list) < 3:
        pm.headsUpMessage(u"选取的骨骼数量必须大于或等于三个")
        pm.warning(u"选取的骨骼数量必须大于或等于三个")
        return

    # # NOTE 获取曲线名称
    # crv_name, ok = QInputDialog.getText(self, u'曲线名称', u'输入曲线名称')
    # if not ok or crv_name == '': return
    # elif pm.objExists(crv_name):
    #     return

    # NOTE 获取生成曲线的骨骼顺序
    adjacent_jnts = getAdjacentJointOrder(jnt_list)
    # NOTE 生成曲线
    curve = pm.curve(d=1,p=[jnt.getTranslation(space="world") for jnt in adjacent_jnts])
    # NOTE 闭合曲线
    pm.closeCurve(curve,ch=0,rpo=1)

if __name__ == "__main__":
    generateCrv()