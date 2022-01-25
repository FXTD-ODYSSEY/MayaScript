# -*- coding: utf-8 -*-
"""
https://pyqt.site/default/issignalconnected.html
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-12-25 23:50:40"

from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets


def isSignalConnected(obj, name):
    """判断信号是否连接
    :param obj:        对象
    :param name:       信号名，如 clicked()
    """
    meta = obj.metaObject()
    for i in range(meta.methodCount()):
        method = meta.method(i)
        print(method.name())
        print(method.typeName())
    index = meta.indexOfMethod(name)
    print(index)
    if index > -1:
        method = obj.metaObject().method(index)
        if method:
            return obj.isSignalConnected(method)
    return False


class Window(QtWidgets.QWidget):
    tested = QtCore.Signal(QtWidgets.QWidget, int)
    # tested = QtCore.Signal(int, int)

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout(self)
        self.button1 = QtWidgets.QPushButton("已连接", self, clicked=self.doTest)
        self.button2 = QtWidgets.QPushButton("未连接", self)
        self.retView = QtWidgets.QTextBrowser(self)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.retView)

        self.tested.connect(lambda *args: print("test"))
        is_connected = isSignalConnected(self, "tested")
        print(is_connected)

    def doTest(self):
        self.retView.append(
            """
        # button1 clicked 是否连接: %s, %s
        # button2 clicked 是否连接: %s, %s
        """
            % (
                self.isSignalConnected(self.button1, "clicked()"),
                self.button1.receivers("clicked") > 0,
                self.isSignalConnected(self.button2, "clicked()"),
                self.button2.receivers("clicked") > 0,
            )
        )


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())