# -*- coding: utf-8 -*-
"""
https://blog.csdn.net/qq_31175907/article/details/121417140
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-04-02 20:48:10"


# Import built-in modules
import json
import os
import tempfile

# Import local modules
import unreal

tmp_dir = tempfile.gettempdir()
rot_path = os.path.join(tmp_dir, "test_unreal_rot.json")


def main():
    with open(rot_path) as rf:
        quat_dict = json.load(rf)

    for _, v in quat_dict.items():
        quat = unreal.Quat(v[0], -v[1], v[2], -v[3])

    rotator = quat.rotator()
    for actor in unreal.EditorLevelLibrary.get_selected_level_actors():

        # NOTES(timmyliang): Maya DirectionalLight default rotation is point to the ground
        # NOTES(timmyliang): So we need to compensate this offset
        if isinstance(actor, unreal.DirectionalLight):
            rotator = rotator.delta(unreal.Rotator(0, 90, 0))

        actor.set_actor_rotation(rotator, False)


if __name__ == "__main__":
    main()
