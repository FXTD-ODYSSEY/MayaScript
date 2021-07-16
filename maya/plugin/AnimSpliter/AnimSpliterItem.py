# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-12 08:49:49'

u"""
批量切分FBX动画
"""

import os
from functools import partial
import pymel.core as pm

from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui
from Qt.QtCompat import loadUi


class AnimSpliterItem(QtWidgets.QWidget):
    """
    AnimSpliterItem 摄像机设置界面的摄像机Item
    """
    def __init__(self,paernt=None,index=0,start=0,end=0):
        super(AnimSpliterItem,self).__init__()
        DIR = os.path.dirname(__file__)
        ui_file = os.path.join(DIR,"ui","item.ui")
        loadUi(ui_file,self)

        self.Widget = paernt
        self.Start_SP.setValue(int(start))
        self.End_SP.setValue(int(end))
        self.Index_Label.setText(str(index))
        
        self.preview_state = False

        self.Delete_BTN.clicked.connect(self.deleteItem)
        self.Preview_BTN.clicked.connect(self.previewItem)

        self.Start_SP.valueChanged.connect(self.startChange)
        self.End_SP.valueChanged.connect(self.endChange)
    
    def startChange(self,value):
        index = self.Index_Label.text()
        self.Widget.setting[index]["start"] = value
        config_path = self.Widget.getCurrentConfigPath()
        self.Widget.exportJsonSetting(config_path)

    def endChange(self,value):
        index = self.Index_Label.text()
        self.Widget.setting[index]["end"] = value
        config_path = self.Widget.getCurrentConfigPath()
        self.Widget.exportJsonSetting(config_path)

    def deleteItem(self):
        layout = self.parent().layout()
        self.setParent(None)
        # NOTE 调整序号
        count = layout.count()
        self.Widget.setting = {}
        for i in range(count-1):
            item = layout.itemAt(i).widget()
            item.Index_Label.setText(str(i+1))
            self.Widget.setting[str(i+1)] = {
                "start":item.Start_SP.value(),
                "end":item.End_SP.value()
            }
            
        config_path = self.Widget.getCurrentConfigPath()
        self.Widget.exportJsonSetting(config_path)

    def previewItem(self):
        if not self.previewCheck():
            QtWidgets.QMessageBox.warning(self,u"警告",u"起始时间和结束时间相等，无法预览！！")
            return

        self.preview_state = not self.preview_state

        layout = self.parent().layout()
        count = layout.count()
        for i in range(count-1):
            item = layout.itemAt(i).widget()
            item.Index_Label.setText(str(i+1))
            if item.Preview_BTN.styleSheet():
                item.previewStop()
                break

        if self.preview_state:
            self.previewPlay()
        else:
            self.previewStop()
    
    def previewPlay(self):
        self.curr = pm.currentTime(q=1)
        self.start = pm.playbackOptions( q=1,min=1 )
        self.end = pm.playbackOptions( q=1,max=1 )
        start = self.Start_SP.value()
        end = self.End_SP.value()
        pm.playbackOptions( min=start, max=end )
        pm.play( state=1 )
        self.Preview_BTN.setStyleSheet("background:red")

    def previewStop(self):
        pm.playbackOptions( min=self.start, max=self.end )
        pm.play( state=0 )
        pm.currentTime(self.curr)
        self.Preview_BTN.setStyleSheet("")

    def previewCheck(self):
        start = self.Start_SP.value()
        end = self.End_SP.value()

        if start > end:
            self.Start_SP.setValue(end)
            self.End_SP.setValue(start)
        elif start == end:
            return False

        return True