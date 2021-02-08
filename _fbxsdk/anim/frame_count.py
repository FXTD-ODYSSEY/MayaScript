# -*- coding: utf-8 -*-
"""
FBX API 读取动画帧数
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-06-01 23:11:30'

import os
import fbx
import FbxCommon
import time
from functools import wraps

DIR = os.path.dirname(__file__)


def logTime(func=None, msg="elapsed time:"):
    """logTime 
    log function running time

    :param func: function get from decorators, defaults to None
    :type func: function, optional
    :param msg: default print message, defaults to "elapsed time:"
    :type msg: str, optional
    :return: decorator function return
    :rtype: dynamic type
    """            
    if not func:
        return partial(logTime,msg=msg)
    @wraps(func)
    def wrapper(*args, **kwargs):
        curr = time.time()
        res = func(*args, **kwargs)
        print(msg,time.time() - curr)
        return res
    return wrapper

    

@logTime
def main():
    FBX_file = os.path.join(DIR, "anim.FBX")
    manager, scene = FbxCommon.InitializeSdkObjects()
    result = FbxCommon.LoadScene(manager, scene, FBX_file)
    if not result:
        return
    
    setting = scene.GetGlobalSettings()
    time_span = setting.GetTimelineDefaultTimeSpan()
    time_mode = setting.GetTimeMode()
    frame_rate = fbx.FbxTime.GetFrameRate(time_mode)
    duration = time_span.GetDuration()
    second = duration.GetMilliSeconds()
    print("frame",round(second/1000*frame_rate))


    # anim = scene.GetCurrentAnimationStack()
    # # print("anim",type(anim),dir(anim))
    # time_span = anim.GetLocalTimeSpan()
    # # print("time_span",type(time_span),dir(time_span))
    # duration = time_span.GetDuration()
    # # print("duration",type(duration),dir(duration))
    # frame_count = duration.GetFrameCount()
    # # frame_rate = duration.GetFrameRate()
    # frame = duration.GetTimeString()
    # print(frame_count,frame)

    # pNode = scene.GetRootNode()

    # for i in range(scene.GetSrcObjectCount(fbx.FbxCriteria.ObjectType(fbx.FbxAnimStack.ClassId))):
    #     lAnimStack = scene.GetSrcObject(fbx.FbxCriteria.ObjectType(fbx.FbxAnimStack.ClassId), i)

    #     for j in range(lAnimStack.GetSrcObjectCount(fbx.FbxCriteria.ObjectType(fbx.FbxAnimLayer.ClassId))):
    #         lAnimLayer = lAnimStack.GetSrcObject(fbx.FbxCriteria.ObjectType(fbx.FbxAnimLayer.ClassId), j)
    #         lAnimCurve = pNode.LclTranslation.GetCurve(lAnimLayer,"X")
    #         lKeyCount = lAnimCurve.KeyGetCount()
    #         print("lkeyCount",lkeyCount)
    #         break
    #     break

    # print(dir(duration))
    # print("anim", anim)
    # print("time_span", time_span)
    # print("duration", duration)
    # print("frame_count", frame_count)


if __name__ == "__main__":
    main()
