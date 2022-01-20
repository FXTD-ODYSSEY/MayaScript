# -*- coding: utf-8 -*-
"""
Import FBX.
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules
import logging

# Import third-party modules
import unreal


__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-12-25 12:48:01"

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

fbx_path = r'E:\_TEMP\2021-12-25\test.fbx'

def import_fbx(sequence, input_file):
    world = unreal.EditorLevelLibrary.get_editor_world()
    bindings = sequence.get_bindings()
    # Set Options
    import_options = unreal.MovieSceneUserImportFBXSettings()
    #import_options.set_editor_property("create_cameras",True)
    import_options.set_editor_property("reduce_keys",False)

    # Import
    unreal.SequencerTools.import_fbx(world, sequence, bindings, import_options, input_file)

    return sequence


def main():
    sequences = [
        sequence
        for sequence in unreal.EditorUtilityLibrary.get_selected_assets()
        if isinstance(sequence, unreal.LevelSequence)
    ]
    if not sequences:
        logging.warning("no sequence selected")
        return

    for sequence in sequences:
        import_fbx(sequence,fbx_path)


if __name__ == "__main__":
    main()
