# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/3749678

UV shell 膨胀
存在膨胀的瑕疵 遂 改用 图片处理的方案
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-12-04 09:52:53"

import os
import sys
import posixpath
import threading
from collections import defaultdict

from Qt import QtGui, QtCore, QtWidgets

import pymel.core as pm
import pymel.core.datatypes as dt


def error_log(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except:
            import traceback

            QtWidgets.QMessageBox.warning(
                None, u"警告", u"错误 \n%s" % traceback.format_exc()
            )

    return wrapper


def vecRot90CW(v):
    return dt.Vector(v.y, -v.x)


def vecRot90CCW(v):
    return dt.Vector(-v.y, v.x)


def polyIsCw(v1, v2):
    return vecRot90CW(v1) * v2 >= 0


def set_option(func):

    if not pm.objExists("TurtleDefaultBakeLayer"):
        pm.evalDeferred(lambda: set_option(func), lp=1)
        return
    TurtleRenderOptions = pm.PyNode("TurtleRenderOptions")
    TurtleRenderOptions.renderer.set(1)
    TurtleDefaultBakeLayer = pm.PyNode("TurtleDefaultBakeLayer")
    TurtleDefaultBakeLayer.tbResX.set(1000)
    TurtleDefaultBakeLayer.tbResY.set(1000)
    TurtleDefaultBakeLayer.tbDirectory.set("turtle/bakedTextures/")
    TurtleDefaultBakeLayer.tbFileName.set("dilation.png")
    TurtleDefaultBakeLayer.renderType.set(1)
    TurtleDefaultBakeLayer.renderSelection.set(1)
    TurtleDefaultBakeLayer.fullShading.set(0)
    TurtleDefaultBakeLayer.tbBilinearFilter.set(0)
    TurtleDefaultBakeLayer.tbEdgeDilation.set(0)
    TurtleDefaultBakeLayer.normals.set(1)
    TurtleDefaultBakeLayer.tbImageFormat.set(9)
    func()


@error_log
def turtle_initialize(func):
    def wrapper(*args, **kwargs):
        # NOTE 加载 turtle 插件
        if not pm.pluginInfo("Turtle", q=1, loaded=1):
            pm.loadPlugin("Turtle")
        # pm.mel.unifiedRenderGlobalsWindow()
        defaultRenderGlobals = pm.PyNode("defaultRenderGlobals")
        defaultRenderGlobals.currentRenderer.set("turtle")
        defaultRenderGlobals.imageFormat.set(32)

        pm.evalDeferred(lambda: set_option(func), lp=1)

    return wrapper


@error_log
# @turtle_initialize
def main():
    sel_list = pm.ls(pm.pickWalk(d="down"), ni=1, type="mesh")
    if not sel_list:
        QtWidgets.QMessageBox.warning(None, u"警告", u"请选择一个模型")
        return
    sel = sel_list[0]

    # # NOTE(timmyliang) 获取法线贴图过滤出里外
    # pm.mel.renderWindowRender("redoPreviousRender", "renderView")
    # texture_path = posixpath.join(
    #     pm.workspace(q=1, rd=1), "turtle", "bakedTextures", "dilation.png"
    # )
    # img = QtGui.QImage(texture_path)

    pm.undoInfo(ock=1)
    
    # TODO check overlap first 
    

    num_list, total = sel.getUvShellsIds()
    shell_dict = {num: i for i, num in enumerate(num_list)}
    border_dict = defaultdict(dict)
    uv_dict = {}

    pm.progressWindow(title=u"获取 uv border", status=u"获取模型 uv border...", progress=0.0)
    for i, uv in shell_dict.items():
        pm.progressWindow(e=1, progress=i / total * 100)
        # NOTES(timmyliang) 如果 uv 不在 0,1 象限则跳过
        x,y = sel.getUV(uv)
        
        if not 0 < x < 1 or not 0 < y < 1:
            continue

        pm.select(sel.map[uv])
        pm.polySelectConstraint(uv=1, bo=0, m=2)
        uv_list = pm.polySelectConstraint(t=0x0010, uv= 0, bo=1, m=2, rs=1)
        uv_list = [_uv.currentItemIndex() for _uv in pm.ls(uv_list, fl=1)]
        pos_list = {uv: sel.getUV(uv) for uv in uv_list}
        x = sum([pos[0] for pos in pos_list.values()]) / len(pos_list)
        y = sum([pos[1] for pos in pos_list.values()]) / len(pos_list)
        uv_dict.update(pos_list)
        borders = pm.polyListComponentConversion(fuv=1, te=1, bo=1)
        borders = pm.ls(borders, fl=1)
        for uv in uv_list:
            edges = pm.polyListComponentConversion(sel.map[uv], fuv=1, te=1)
            edges = [e for e in pm.ls(edges, fl=1) if e in borders]
            uvs = pm.polyListComponentConversion(edges, fe=1, tuv=1)
            uvs = [_uv.currentItemIndex() for _uv in pm.ls(uvs, fl=1)]
            uvs = [_uv for _uv in uvs if _uv != uv and _uv in uv_list]
            border_dict[uv] = {"uvs": uvs, "center": (x, y)}

    pm.progressWindow(ep=1)
    pm.polySelectConstraint(uv=0,bo=0, rs=1)

    distant = 0.01
    
    for uv, data in border_dict.items():
        uvs = data.get("uvs",[])
        if len(uvs) <= 1:
            continue
        uv1, uv2 = uvs
        x, y = data.get("center")
        center = dt.Vector(x, y)
        
        pos = dt.Vector(*uv_dict[uv])
        pos1 = dt.Vector(*uv_dict[uv1])
        pos2 = dt.Vector(*uv_dict[uv2])
        vec1 = pos - pos1
        vec2 = pos2 - pos
        
        x,y  = get_pt(pos,pos1,pos2,vec1,vec2,distant)
        pt = dt.Vector(x,y)
        vec = pos - pt
        line = pos - center
        # NOTE reverse
        if vec.dot(line) > 0:
            x,y  = get_pt(pos,pos1,pos2,vec1,vec2,distant,True)
        sel.setUV(uv, x, y)
    
    face_list = pm.polyUVOverlap( sel.faces,oc=True )    
    pm.undoInfo(cck=1)
    
    # pm.undo()
    # pm.selectType(facet=1,ocm=1)
    # pm.hilite()
    # pm.select(face_list)


def get_pt(pos,pos1,pos2,vec1,vec2,distant,reverse=False):
    rot = vecRot90CCW if polyIsCw(vec1, vec2) else vecRot90CW
    vec1 = rot(vec1)
    vec1.normalize()
    d = vec1 * distant
    if reverse:
        d = -d
    line1_0 = pos + d
    line1_1 = pos1 + d

    vec2 = rot(vec2)
    vec2.normalize()
    d = vec2 * distant
    if reverse:
        d = -d
    line2_0 = pos + d
    line2_1 = pos2 + d

    a1 = line1_1.x - line1_0.x
    b1 = line2_0.x - line2_1.x
    c1 = line2_0.x - line1_0.x
    a2 = line1_1.y - line1_0.y
    b2 = line2_0.y - line2_1.y
    c2 = line2_0.y - line1_0.y

    val = a2 * b1 - a1 * b2
    if val == 0:
        x = line1_0.x
        y = line1_0.y
    else:
        t = (b1 * c2 - b2 * c1) / val
        x = line1_0.x + t * (line1_1.x - line1_0.x)
        y = line1_0.y + t * (line1_1.y - line1_0.y)

    return x,y

if __name__ == "__main__":
    main()
