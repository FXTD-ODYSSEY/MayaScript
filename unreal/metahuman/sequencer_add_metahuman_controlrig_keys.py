# -*- coding: utf-8 -*-
"""
打开 metahuman 项目执行脚本
需要启用 Sequencer Scripting 插件
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-06-24 18:07:09"

# Import built-in modules
from collections import defaultdict
import json
import os
import math

# Import local modules
import unreal

DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = r"F:\repo\MayaScript\unreal\metahuman\BP_Ada.json"


def unreal_progress(tasks, label="进度", total=None):
    total = total if total else len(tasks)
    with unreal.ScopedSlowTask(total, label) as task:
        task.make_dialog(True)
        for i, item in enumerate(tasks):
            if task.should_cancel():
                break
            task.enter_progress_frame(1, "%s %s/%s" % (label, i, total))
            yield item


def main():
    # NOTE: 读取 sequence
    sequence = unreal.load_asset(
        "/Game/Digital_Idol/Characters/Lucky22/Sequence/NewLevelSequence.NewLevelSequence"
    )
    # NOTE: 收集 sequence 里面所有的 binding
    binding_dict = defaultdict(list)
    for binding in sequence.get_bindings():
        binding_dict[binding.get_name()].append(binding)

    with open(DATA_PATH, "r") as rf:
        key_data = json.load(rf)

    # NOTE: 遍历命名为 Face 的 binding
    for binding in unreal_progress(binding_dict.get("ABP_headmesh", []), "导入 Face 数据"):
        # NOTE: 获取关键帧 channel 数据
        keys_dict = {}
        for track in binding.get_tracks():
            for section in track.get_sections():
                for channel in unreal_progress(section.get_channels(), "导入关键帧"):
                    channel_name = channel.get_name()
                    if not channel_name.startswith("CTRL_"):
                        continue

                    channel_name = channel_name.rsplit("_", 1)[0]
                    key_list = key_data.get(channel_name)
                    if not key_list:
                        continue

                    for frame_data in key_list:
                        frame = frame_data.get("frame")
                        value = frame_data.get("value")
                        sub_frame, frame = math.modf(frame_data.get("frame"))
                        channel.add_key(unreal.FrameNumber(frame), value, sub_frame)


if __name__ == "__main__":
    main()
