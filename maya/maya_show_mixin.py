# -*- coding: utf-8 -*-
"""
解决 Maya 加载 ui 文件问题
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-07-19 22:29:57"


class MayaShowMixin(object):
    def maya_show(self, win_name=""):
        from Qt import QtWidgets
        from Qt.QtCompat import wrapInstance
        from maya import cmds, OpenMayaUI

        def maya_to_qt(name):
            # Maya -> QWidget
            ptr = OpenMayaUI.MQtUtil.findControl(name)
            if ptr is None:
                ptr = OpenMayaUI.MQtUtil.findLayout(name)
            if ptr is None:
                ptr = OpenMayaUI.MQtUtil.findMenuItem(name)
            if ptr is not None:
                return wrapInstance(int(ptr), QtWidgets.QWidget)

        win_name = win_name if win_name else self.__class__.__name__
        # NOTE 如果变量存在 就检查窗口多开
        if cmds.window(win_name, q=1, ex=1):
            cmds.deleteUI(win_name)

        window = cmds.window(win_name, title=self.windowTitle())

        cmds.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        self.__maya_window__ = maya_to_qt(window)
        layout = QtWidgets.QVBoxLayout()
        self.__maya_window__.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self)

        self.__maya_window__.setMaximumSize(self.maximumSize())
        self.__maya_window__.setMinimumSize(self.minimumSize())
        return self.__maya_window__
