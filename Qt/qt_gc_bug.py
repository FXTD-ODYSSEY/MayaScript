# -*- coding: utf-8 -*-
"""
记录 Qt 的回收问题
因为 object 没有赋值会导致函数 gc 不起作用
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-03-21 20:58:35'


from Qt import QtWidgets
from Qt import QtCore
import attr
from dayu_widgets.qt import application

@attr.s(hash=False)
class TestCaller(object):
    view = attr.ib()

    def __call__(self):
        self.view.customContextMenuRequested.connect(self.test_print)
        return self
    
    def test_print(self):
        print(123)


class TestTreeView(QtWidgets.QTreeView):
    def __init__(self):
        super(TestTreeView, self).__init__()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        # # NOTES(timmyliang): 注册生效
        # self.caller = TestCaller(self)()

        # NOTES(timmyliang): 注册不生效
        TestCaller(self)()



with application():
        
    view = TestTreeView()
    view.show()
