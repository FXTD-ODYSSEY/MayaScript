# -*- coding: utf-8 -*-
"""
Numpy RBF retarget.
add this script into Python Script Node.
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-09-21 16:25:37"

# Import third-party modules
import hou
import numpy as np

import time

# start = time.time()

node = hou.pwd()
geo = node.geometry()
src_geo = node.inputGeometry(1)
dst_geo = node.inputGeometry(2)

src_matrix = np.array([point.position() for point in src_geo.iterPoints()])
dst_matrix = np.array([point.position() for point in dst_geo.iterPoints()])

distance_matrix = np.array(
    [point.attribValue("distance_matrix") for point in src_geo.iterPoints()]
)

# NOTES(timmyliang): calculate weight matrix
weight_matrix = np.linalg.solve(distance_matrix, dst_matrix)


input_distance_matrix = np.array(
    [point.attribValue("distance_matrix") for point in geo.iterPoints()]
)

output = np.matmul(input_distance_matrix, weight_matrix)

# NOTES(timmyliang): add color to source input mesh
for index, point in enumerate(geo.iterPoints()):
    point.setAttribValue("P", output[index])

# print('elapsed time: %s' % (time.time() - start))
