# -*- coding: utf-8 -*-
"""
Numpy RBF calculate.
add this script into Python Script Node.
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-09-21 16:25:37"

# Import built-in modules
from collections import defaultdict

# Import third-party modules
import hou
import numpy as np

node = hou.pwd()
geo = node.geometry()
input_geo = node.inputGeometry(1)

center = geo.boundingBox().center()
input_points = input_geo.poients()

cd_list = []
pos_list = []
dist_list = []
for point in input_points:
    pos = point.position()
    pos_list.append(pos)
    cd_list.append(point.attribValue("Cd"))
    dist_list.append((center - pos).length())

# NOTES(timmyliang): Construct Distance Matrix
input_points_count = len(input_points)
dis_matrix = np.zeros(shape=(input_points_count, input_points_count))
for row, row_pos in enumerate(pos_list):
    for col, col_pos in enumerate(pos_list):
        dis_matrix[row][col] = (row_pos - col_pos).length()

# NOTES(timmyliang): calculate weight matrix
weight_matrix = np.linalg.inv(dis_matrix).dot(np.array(cd_list))

output_cd = tuple(np.array(dist_list).dot(weight_matrix))

# NOTES(timmyliang): get cd attrib (create it if not exists)
cd_attrib = geo.findPointAttrib("Cd")
if not cd_attrib:
    cd_attrib = geo.addAttrib(hou.attribType.Point, "Cd", (1.0, 1.0, 1.0))

# NOTES(timmyliang): add color to source input mesh
for point in geo.points():
    point.setAttribValue(cd_attrib, output_cd)
