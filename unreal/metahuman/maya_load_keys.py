# -*- coding: utf-8 -*-
"""

"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-06-24 16:01:05"

# Import built-in modules
import json
import os
import traceback

# Import third-party modules
import pymel.core as pm

DIR = os.path.dirname(os.path.abspath(__file__))


def progress(seq, status="", title=""):
    pm.progressWindow(status=status, title=title, progress=0.0, isInterruptable=True)
    total = len(seq)
    for i, item in enumerate(seq):
        try:
            if pm.progressWindow(query=True, isCancelled=True):
                break
            pm.progressWindow(e=True, progress=float(i) / total * 100)
            yield item  # with body executes here
        except:
            traceback.print_exc()
            pm.progressWindow(ep=1)
    pm.progressWindow(ep=1)


def main():

    # NOTE: 读取数据
    with open(os.path.join(DIR, "BP_metahuman_001.json"), "r") as rf:
        data = json.load(rf)

    attr_map = {"location": "t", "rotation": "r"}
    status = "Import Keyframe to metahuman controller"
    
    # NOTE: undo 支持
    pm.undoInfo(ock=1)
    for channel, frame_list in progress(data.items(), status=status):
        # NOTE: 解析 channel_name
        has_attr = channel.count(".")
        
        if not has_attr:
            # NOTE: 处理 `CTRL_C_eye_parallelLook_4311` 格式
            ctrl_name = channel.rsplit("_", 1)[0]
            attr = "ty"
        else:
            parts = iter(channel.split("."))
            ctrl_name = next(parts, "")
            param = next(parts, "")
            axis = next(parts, "")
            if not axis:
                # NOTE: 处理 `CTRL_C_teethD.Y_4330` 格式
                attr = "t"
                axis = param
            else:
                # NOTE: 处理 `CTRL_L_eyeAim.Rotation.Y_4387` 格式
                attr = attr_map.get(param.lower())
            attr += axis.split("_")[0].lower()

        # NOTE: 解析出控制器属性设置关键帧
        attribute = pm.PyNode(".".join([ctrl_name, attr]))
        for frame_data in frame_list:
            frame = frame_data.get("frame")
            value = frame_data.get("value")
            attribute.setKey(t=frame, v=value)

    pm.undoInfo(cck=1)


if __name__ == "__main__":
    main()
