# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-27 11:19:13'

"""
欧拉角 过滤 增强版
曲线编辑器的欧拉角过滤是对所有曲线操作
这里如果有选择的话，只会过滤选择部分的曲线
如果没有选择的话，就是默认的欧拉角过滤。
"""

import pymel.core as pm
from maya import mel


def eulerFilterEnhance():

    # NOTE 获取关键帧曲线 | 区分出驱动关键帧
    anim_dict = {}
    filter_flag = False
    anim_list = pm.keyframe(q=1,sl=1,n=1)
    
    if anim_list:
        for anim in anim_list:
            anim = pm.PyNode(anim)
            anim_dict[anim] = {}
            selected = pm.keyframe(anim,q=1,sl=1,iv=1)
            for idx in pm.keyframe(anim,q=1,iv=1):
                if idx not in selected:
                    anim_dict[anim][idx] = anim.getValue(idx)
                else:
                    filter_flag = True

    else:
        # NOTE 单帧曲线过滤
        # # NOTE 获取当前时间帧
        # cur = pm.currentTime(q=1)
        # for sel in pm.ls(sl=1):
        #     anim_list.extend(sel.listConnections(type="animCurveTA")) 

        # # NOTE 找出前后有关键帧 但是关键帧为小数中间的值进行删除
        # for anim in anim_list:
        #     anim_dict[anim] = {}
        #     for idx in pm.keyframe(anim,q=1,iv=1):
        #         time = anim.getTime(idx)
        #         if time != cur:
        #             anim_dict[anim][idx] = anim.getValue(idx)
        #         else:
        #             filter_flag = True
        mel.eval("performEulerFilter graphEditor1FromOutliner")
    
    if filter_flag:
        # NOTE 过滤曲线
        pm.filterCurve(anim_list)

        # NOTE 复原其他关键帧
        for anim,data in anim_dict.items():
            for idx,val in data.items():
                anim.setValue(idx,val)
        
if __name__ == "__main__":
    eulerFilterEnhance()