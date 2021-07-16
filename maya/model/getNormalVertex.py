# coding:utf-8
from __future__ import unicode_literals, division, print_function

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-05-22 12:29:35'

"""

"""

import sys
import pymel.core as pm
import pymel.core.datatypes as dt

from maya import OpenMaya
from maya import cmds


def getSimilarNormalVertex(thersold=0.95):

    for vtx in pm.ls(sl=1, fl=1):
        if type(vtx) is pm.MeshVertex:
            break
    else:
        pm.headsUpMessage(u"请选择一个顶点")
        return

    normal = OpenMaya.MVector(vtx.getNormal())

    node = vtx.node()
    itr = OpenMaya.MItMeshFaceVertex(node.__apimdagpath__())

    target_list = []
    while not itr.isDone():
        target_normal = OpenMaya.MVector()
        itr.getNormal(target_normal)
        vert_id = itr.vertId()
        face_id = itr.faceId()
        if normal * target_normal > thersold:
            target_list.append("%s.vtxFace[%s][%s]" % (
                node.fullPathName(), vert_id, face_id))
        itr.next()

    return target_list


def create_ui():
    ui_name = "SimilarNormalVertex_UI"
    if cmds.window(ui_name, exists=1):
        cmds.deleteUI(ui_name)

    window = cmds.window(ui_name, title="选择相似法线点", w=150,h=100)
    cmds.columnLayout(adj=1,columnAttach=["both",15])

    # NOTE 开发 slider 和 按钮 选择相似法线
    slider = cmds.floatSliderGrp(label='法线重合度', field=True, minValue=-1, maxValue=1, value=0.95, step=0.01 , columnWidth3=[30,100,20])
    cmds.button(label='选择相似顶点', 
                command=lambda *args: pm.select(getSimilarNormalVertex(cmds.floatSliderGrp(slider,q=1,v=1))))

    cmds.showWindow(window)


def main():
    create_ui()


if __name__ == "__main__":
    main()
