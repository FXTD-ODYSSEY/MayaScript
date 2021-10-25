# -*- coding: utf-8 -*-
"""
Convert Soft-Selection to Cluster Tutorial
https://vimeo.com/200579734

drive OpenMaya 1.0
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-10-14 10:30:21"


from maya import OpenMaya
import pymel.core as pm


def main():

    soft_selection = OpenMaya.MRichSelection()
    OpenMaya.MGlobal.getRichSelection(soft_selection)

    selection_list = OpenMaya.MSelectionList()
    soft_selection.getSelection(selection_list)
    dag = OpenMaya.MDagPath()
    obj = OpenMaya.MObject()
    selection_list.getDagPath(0, dag, obj)

    comp_indices = OpenMaya.MFnSingleIndexedComponent(obj)
    index_list = OpenMaya.MIntArray()
    comp_indices.getElements(index_list)

    # NOTE https://forum.highend3d.com/t/how-to-get-along-with-mstringarray/48971/7
    # NOTE Maya API 没有 MStringArray 类型，直接传入 Python 数组即可
    vertex_array = []
    selection_list.getSelectionStrings(vertex_array)
    cluster = pm.cluster(vertex_array)[0]
    for i, index in enumerate(index_list):
        weight = comp_indices.weight(i).influence()
        cluster.weightList[0].w[index].set(weight)
    

if __name__ == "__main__":
    main()
