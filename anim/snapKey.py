# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-11-25 14:38:10'

"""
获取关键帧曲线并优化
"""

import pymel.core as pm

def snapKey():
    # NOTE 通过命令将 关键帧 吸附
    start = pm.playbackOptions( q=1 , min=1 )
    end = pm.playbackOptions( q=1 , max=1 )
    
    # NOTE 清空关键帧选择避免 snapKey 报错
    pm.selectKey(cl=1)
    pm.snapKey( t=(start,end), tm=1.0 )

    # NOTE 获取关键帧曲线 | 区分出驱动关键帧
    anim_list = []    
    for sel in pm.ls(sl=1):
        anim_list.extend(sel.listConnections(type="animCurveTA")) 
        anim_list.extend(sel.listConnections(type="animCurveTU")) 
        anim_list.extend(sel.listConnections(type="animCurveTL")) 

    # NOTE 找出前后有关键帧 但是关键帧为小数中间的值进行删除
    remove_dict = {}
    for anim in anim_list:
        for keyframe in range(anim.numKeys()):
            time = anim.getTime(keyframe)
            if not time.is_integer():
                if not remove_dict.has_key(anim):
                    remove_dict[anim] = []
                remove_dict[anim].append(time)

    for anim,times in remove_dict.items():
        for time in times:
            pm.cutKey(anim,clear=1,time=time)


if __name__ == "__main__":
    snapKey()
