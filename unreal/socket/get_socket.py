# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-06-03 16:04:17'


# NOTE 选择 skeletal mesh
skel_mesh , = unreal.EditorUtilityLibrary.get_selected_assets()
socket = "Lf_foot_drv_skinSocket"
socket = skel_mesh.find_socket(socket)
print(socket)
print(socket.relative_location)

