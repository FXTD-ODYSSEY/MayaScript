# -*- coding: utf-8 -*-
"""
测试
将 Maya 的 Outliner 和 NodeEditor 转换成 Qt Widgets 放到布局里
# TODO 时间过长会被 gc 回收

# NOTE 用 cmds 可以简单实现
import maya.cmds as cmds

cmds.window(title="Adam Node Editor",wh=(1200,800))
cmds.paneLayout( configuration='vertical2' )
outliner = cmds.outlinerPanel()
cmds.setParent("..")
editor = cmds.scriptedPanel(type="nodeEditorPanel")
cmds.showWindow()

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-11-16 14:54:30"

import os
import contextlib

import pymel.core as pm

from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore
from Qt.QtCompat import loadUi


DIR, BASE = os.path.split(__file__)


class MayaShowMixin(object):
    @staticmethod
    def maya_to_qt(name):
        from Qt.QtCompat import wrapInstance
        from maya import OpenMayaUI

        # Maya -> QWidget
        ptr = OpenMayaUI.MQtUtil.findControl(name)
        if ptr is None:
            ptr = OpenMayaUI.MQtUtil.findLayout(name)
        if ptr is None:
            ptr = OpenMayaUI.MQtUtil.findMenuItem(name)
        if ptr is not None:
            return wrapInstance(int(ptr), QtWidgets.QWidget)

    def maya_show(self, win_name=""):
        from Qt import QtWidgets

        win_name = win_name if win_name else self.__class__.__name__
        # NOTE 如果变量存在 就检查窗口多开
        if pm.window(win_name, q=1, ex=1):
            pm.deleteUI(win_name)

        window = pm.window(win_name, title=self.windowTitle())

        pm.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        self.__maya_window__ = self.maya_to_qt(window)
        layout = QtWidgets.QVBoxLayout()
        self.__maya_window__.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self)

        self.__maya_window__.setMaximumSize(self.maximumSize())
        self.__maya_window__.setMinimumSize(self.minimumSize())
        return self.__maya_window__


class NodeOutliner(QtWidgets.QWidget, MayaShowMixin):
    @classmethod
    @contextlib.contextmanager
    def get_widget(cls, widget_callback=None):
        pm.window()
        pm.formLayout()
        p = widget_callback()
        yield cls.maya_to_qt(p)

    def __init__(self):
        super(NodeOutliner, self).__init__()
        name = os.path.splitext(BASE)[0]
        ui_file = os.path.join(DIR, name + ".ui")
        loadUi(ui_file, self)

        with self.get_widget(lambda: pm.scriptedPanel(typ="nodeEditorPanel")) as editor:
            layout = self.Node_Editor.layout()
            layout.addWidget(editor)

        with self.get_widget(pm.outlinerPanel) as outliner:
            layout = self.Outliner.layout()
            layout.addWidget(outliner)

            window = outliner.window()
            view = window.findChild(QtWidgets.QListView)
            proxy_model = view.model()
            model = proxy_model.sourceModel()
            print(model)

            # window = outliner.window()
            # for w in window.children():
            #     if isinstance(w, QtWidgets.QWidget):
            #         layout.addWidget(w)


if __name__ == "__main__":
    window = NodeOutliner()
    window.maya_show()
