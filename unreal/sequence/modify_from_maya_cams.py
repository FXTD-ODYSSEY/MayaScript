# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-11-16 21:07:20'


import unreal

maya_cams = ['MayaCamera','MayaCamera2']

def main():
    sequence_list = [a for a in unreal.EditorUtilityLibrary.get_selected_assets() if isinstance(a,unreal.LevelSequence)]
    sequence = sequence_list[0]
    
    for binding in sequence.get_bindings():
        if binding.get_name() not in maya_cams:
            continue
        for cam_binding in binding.get_child_possessables():
            if cam_binding.get_name() != "CameraComponent":
                continue
            
            # NOTES(timmyliang): 业务逻辑
            tracks = cam_binding.find_tracks_by_type(unreal.MovieSceneFloatTrack)
            track = tracks[0]
            sections = track.get_sections()
            section = sections[0]
            section.set_range(101, 165)
            channels = section.find_channels_by_type(unreal.MovieSceneScriptingFloatChannel)
            tmp_channel = channels[0]
            tmp_channel.add_key(unreal.FrameNumber(135), 0.5)


if __name__ == "__main__":
    main()


# @maxjzhang(张军)
