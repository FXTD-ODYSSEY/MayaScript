# -*- coding: utf-8 -*-
"""
修改 referneceEdit 属性进行匹配
结果匹配上了道具 但是轴向错误没有意义
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-12-08 16:55:55"

import pymel.core as pm
from maya.maya_to_py_itr import PyEditItr
from maya import OpenMaya
from Qt import QtWidgets


def main():
    # sel_list = pm.ls(pm.pickWalk(d="down"), ni=1, type="mesh")
    # if not sel_list:
    #     QtWidgets.QMessageBox.warning(None, u"警告", u"请选择一个模型")
    #     return
    # sel = sel_list[0]

    for ref in pm.listReferences():
        if ref != "X:/Characters/A_Usopp01/Rig/Low/Skel_Usopp01_L_rig.mb":
            continue
        ref = ref.refNode
        edits = PyEditItr(ar_mobj=ref.__apimobject__())
        
        for edit in edits:
            # NOTES(timmyliang) 获取出断开链接的关键帧
            if (
                edit.editType() is OpenMaya.MEdit.kConnectDisconnectEdit
                and edit.isFailed()
            ):
                attr = edit.dstPlugName()
                target_attr = attr.replace("Skel_90004_L_rig:","Skel_Usopp01_w01_L_rig:")
                if not pm.objExists(target_attr):
                    continue
                target_attr = pm.PyNode(target_attr)
                node = target_attr.node()
                name = node.getParent().longName()
                # print(name)
                pm.referenceEdit( ref, changeEditTarget=(attr,"%s.%s" % (name,target_attr.longName())))
        pm.referenceEdit( ref, applyFailedEdits=True )

if __name__ == "__main__":
    main()
