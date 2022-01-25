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

def main():
    sequence_list = [a for a in unreal.EditorUtilityLibrary.get_selected_assets() if isinstance(a,unreal.LevelSequence)]
    sequence = sequence_list[0]
    for binding in sequence.find_binding_by_name():
        print(binding.get_child_possessables())
        # print("binding: %s" % binding.get_name())
        # parent = binding.get_parent()
        # print("parent: %s" % parent.get_name())
        
        
    # binding = sequence.find_binding_by_name("CameraComponent")  # 拿到绑定
    # tracks = binding.find_tracks_by_type(unreal.MovieSceneFloatTrack)
    # track = tracks[0]
    # sections = track.get_sections()
    # section = sections[0]
    # section.set_range(101, 165)
    # channels = section.find_channels_by_type(unreal.MovieSceneScriptingFloatChannel)
    # tmp_channel = channels[0]
    # tmp_channel.add_key(unreal.FrameNumber(135), 0.5)

    return
    
    print(sequence_list)
    for sequence in sequence_list:
        
        for binding in sequence.get_bindings():
            print(binding.get_name())
            for track in binding.get_tracks():
                print("track_name",track.get_name())
                for section in track.get_sections():
                    print("section_name",section.get_name())
                    for channel in section.get_channels():
                        print("channel_name",channel.get_name())
                        if channel.get_name() == "MovieSceneScriptingFloatChannel_19":
                            print(channel)
                        # for key in channel.get_keys():                
                        #     print(key)
        

if __name__ == "__main__":
    main()


# @maxjzhang(张军)
