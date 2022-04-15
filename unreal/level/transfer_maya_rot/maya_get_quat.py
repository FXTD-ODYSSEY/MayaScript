# -*- coding: utf-8 -*-
"""
get maya selected object quaternion

Maya need to set to Z axis ！
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-04-02 20:58:39"

# Import built-in modules
import json
import os
import tempfile

# Import third-party modules
import pymel.core as pm

def main():
    # NOTES(timmyliang): make sure current in Z axis
    pm.mel.setUpAxis("z")  
    tmp_dir = tempfile.gettempdir()
    rot_path = os.path.join(tmp_dir, 'test_unreal_rot.json')
    quat_list = {str(sel):tuple(sel.getTransform().getRotation().asQuaternion()) for sel in pm.ls(sl=1)}
    with open(rot_path, "w") as wf:
        json.dump(quat_list, wf)

if __name__ == "__main__":
    main()
