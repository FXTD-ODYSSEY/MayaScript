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


logger = logging.getLogger(__name__)


def export_fbx(sequence):
    pass


def main():
    pass
    sequences = [
        sequence
        for sequence in unreal.EditorUtilityLibrary.get_selected_assets()
        if isinstance(sequence, unreal.LevelSequence)
    ]
    if not sequences:
        logger.warning("no sequence selected")
        return

    for sequence in sequences:
        export_fbx(sequence)


if __name__ == '__main__':
    main()
