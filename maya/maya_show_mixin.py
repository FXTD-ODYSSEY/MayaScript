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
        from pymel import core as pm

        win_name = win_name if win_name else self.__class__.__name__
        # NOTE 如果变量存在 就检查窗口多开
        if pm.window(win_name, q=1, ex=1):
            pm.deleteUI(win_name)

        window = pm.window(win_name, title=self.windowTitle())

        pm.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        self.__maya_window__ = pm.toQtObject(window)
        layout = QtWidgets.QVBoxLayout()
        self.__maya_window__.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self)

        self.__maya_window__.setMaximumSize(self.maximumSize())
        self.__maya_window__.setMinimumSize(self.minimumSize())
        return self.__maya_window__


if __name__ == "__main__":
    from Qt import QtWidgets

    class TestWidget(QtWidgets.QPushButton, MayaShowMixin):
        pass

    widget = TestWidget()
    widget.maya_show()
