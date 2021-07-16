# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-18 11:25:25'

import os
from Qt import QtWidgets
from Qt import QtCore
from Qt.QtCompat import loadUi,wrapInstance
from maya.app.general import mayaMixin
import pymel.core as pm
import pymel.core.nodetypes as nt
from maya import OpenMayaUI as omui

class MyTestWidget(mayaMixin.MayaQWidgetBaseMixin,QtWidgets.QWidget):
    def __init__(self, parent=None):
        mainWindowPtr = omui.MQtUtil.mainWindow()
        parent = wrapInstance(long(mainWindowPtr), QtWidgets.QMainWindow)
        # parent = parent if parent else QtWidgets.QApplication.activeWindow()
        super(MyTestWidget, self).__init__(parent = parent)

        ui_file = "%s.ui" % os.path.splitext(__file__)[0]
        loadUi(ui_file, self)
        
        # window = QtWidgets.QApplication.activeWindow()
        # self.setParent(window)

        self.Edit = QtWidgets.QLineEdit(u"Python实现")
        self.layout().addWidget(self.Edit)
        
        self.TestButton.clicked.connect(self.print_test)
        self.Mesh_BTN.clicked.connect(self.get_mesh)
        
        self.setWindowFlags(QtCore.Qt.Window)
        
    # def show(self):
    #     # NOTE 避免窗口多开
    #     cls_name = self.__class__.__name__
    #     for win in QtWidgets.QApplication.topLevelWidgets():
    #         if cls_name == win.__class__.__name__:
    #             win.close()
    #     super(MyTestWidget, self).show()
        
    def get_mesh(self):
        sel_list = [
            m
            for m in pm.ls(sl=1, ni=1)
            if hasattr(m, "getShape") and isinstance(m.getShape(), nt.Mesh)
        ]
        sel = sel_list[0] if sel_list else ""
        self.Mesh_LE.setText(str(sel))

    def print_test(self):
        print(self.Edit)
        print(self.TestEdit)
        print(self.Edit.text())
        print(self.TestEdit.text())



def main():
    
    window = MyTestWidget()
    window.show()
    return window
    


# import sys
# MODULE = r"F:\MayaTecent\MayaScript\_maya_batch\test_load_ui"
# sys.path.insert(0,MODULE) if MODULE not in sys.path else None
# import test_load
# reload(test_load)
# from test_load import MyTestWidget
# window = MyTestWidget()
# window.show()
# print(window.Edit)
# print(window.TestEdit)
# print(window.Edit.text())
# print(window.TestEdit.text())
