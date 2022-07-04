# -*- coding: utf-8 -*-
"""
打开 metahuman 项目执行脚本
需要启用 Sequencer Scripting 插件
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-06-24 18:07:09'

# Import built-in modules
from collections import defaultdict
import json
import os

# Import local modules
import unreal

DIR = os.path.dirname(os.path.abspath(__file__))


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
    sequence = unreal.load_asset('/Game/Sequencer/MetaHumanSample_Sequence.MetaHumanSample_Sequence')
    # NOTE: 收集 sequence 里面所有的 binding
    binding_dict = defaultdict(list)
    for binding in sequence.get_bindings():
        binding_dict[binding.get_name()].append(binding)

    # NOTE: 遍历命名为 Face 的 binding
    for binding in unreal_progress(binding_dict.get("Face", []), "导出 Face 数据"):
        # NOTE: 获取关键帧 channel 数据
        keys_dict = {}
        for track in binding.get_tracks():
            for section in track.get_sections():
                for channel in unreal_progress(section.get_channels(), "导出关键帧"):
                    if not channel.get_num_keys():
                        continue
                    keys = []
                    for key in channel.get_keys():
                        frame_time = key.get_time()
                        frame = frame_time.frame_number.value + frame_time.sub_frame
                        keys.append({"frame": frame, "value": key.get_value()})

                    keys_dict[channel.get_name()] = keys

        # NOTE: 导出 json
        name = binding.get_parent().get_name()
        export_path = os.path.join(DIR, "{0}.json".format(name))
        with open(export_path, "w") as wf:
            json.dump(keys_dict, wf, indent=4)


if __name__ == "__main__":
    main()
