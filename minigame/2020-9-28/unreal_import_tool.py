# -*- coding: utf-8 -*-
"""
测试 C++ 获取 thumbnail 
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-09-28 16:52:47'


import unreal
from Qt import QtCore, QtWidgets, QtGui
from Qt.QtCompat import load_ui, QFileDialog

py_lib = unreal.PyToolkitBPLibrary()

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyWidget,self).__init__()
        self.vertical = QtWidgets.QVBoxLayout()
        self.scroll = QtWidgets.QScrollArea()
        self.content = QtWidgets.QWidget()
        self.scroll.setWidget(self.content)
        self.scroll.setWidgetResizable(True)
        self.layout = QtWidgets.QVBoxLayout()

        for asset in unreal.EditorUtilityLibrary.get_selected_assets():
            label = QtWidgets.QLabel()
            data = "".join([chr(v) for v in py_lib.get_thumbnial(asset)])
            image = QtGui.QImage(data, 256, 256, QtGui.QImage.Format_RGB32)
            label.setPixmap(QtGui.QPixmap.fromImage(image).scaled(256, 256))
            self.layout.addWidget(label)
            
        self.content.setLayout(self.layout)
        self.vertical.addWidget(self.scroll)
        self.setLayout(self.vertical)

widget = MyWidget()
widget.resize(800, 600)
widget.show()