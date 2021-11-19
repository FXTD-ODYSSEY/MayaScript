# -*- coding: utf-8 -*-
"""
修改 cameraComponent 属性
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-11-16 21:00:45'

import unreal

def main():
    sequence = unreal.load_asset("/Game/NewLevelSequence", unreal.LevelSequence)
    binding = sequence.find_binding_by_name("CameraComponent")  # 修改为 component
    tracks = binding.find_tracks_by_type(unreal.MovieSceneFloatTrack) # 修改为 float track
    track = tracks[0]
    sections = track.get_sections()
    section = sections[0]
    section.set_range(101, 165)
    channels = section.find_channels_by_type(unreal.MovieSceneScriptingFloatChannel)
    tmp_channel = channels[0]
    tmp_channel.add_key(unreal.FrameNumber(135), 0.5)


if __name__ == "__main__":
    main()
