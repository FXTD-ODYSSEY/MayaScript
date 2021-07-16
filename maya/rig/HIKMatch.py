# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-11 16:21:11'

"""
HumanIK 骨架 匹配 快速绑定骨架 的工具
"""

from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets
from Qt import QtCompat

import pymel.core as pm
import maya.OpenMayaUI as omui


class MayaGetUI(QtWidgets.QWidget):
    def __init__(self,text="",btn_text=""):
        super(MayaGetUI,self).__init__()

        self.Label = QtWidgets.QLabel(text)
        self.LE = QtWidgets.QLineEdit()
        self.BTN = QtWidgets.QPushButton(btn_text)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.Label)
        layout.addWidget(self.LE)
        layout.addWidget(self.BTN)

        self.setLayout(layout)

class HumanIKMatchUI(QtWidgets.QWidget):
    def __init__(self):
        super(HumanIKMatchUI, self).__init__()

        self.QuickRigGet = MayaGetUI(u"快速绑定骨架",u"获取")
        self.QuickRigGet.BTN.clicked.connect(lambda:self.QuickRigGet.LE.setText(self.getHumanIK()))

        self.HumanRigGet = MayaGetUI(u"目标匹配骨架",u"获取")
        self.HumanRigGet.BTN.clicked.connect(lambda:self.HumanRigGet.LE.setText(self.getHumanIK()))

        self.Match_BTN = QtWidgets.QPushButton(u"一键匹配")
        self.Match_BTN.clicked.connect(self.matchRig)
        
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.QuickRigGet)
        layout.addWidget(self.HumanRigGet)
        layout.addWidget(self.Match_BTN)
        layout.addItem(spacerItem)

        self.setLayout(layout)
        self.setWindowTitle(u"匹配 HumanIK 骨架")
    
    def getHumanIK(self):
        sel = pm.ls(sl=1,ni=1)[0]

        mode = ""
        if sel.type() == "hikFKJoint" or sel.type() == "hikIKEffector" :
            mode = "ctrl"
        elif sel.type() == "joint":
            mode = "joint"
        else:
            QtWidgets.QMessageBox.information(self,u"警告",u"请选择 HumanIK 相关的物体")
            return

        prefix = sel.split("_")[0]

        if not pm.optionMenuGrp("hikCharacterList",q=1,ex=1):
            QtWidgets.QMessageBox.information(self,u"警告",u"请创建HumanIK骨骼")
            return

        for item in pm.optionMenuGrp("hikCharacterList",q=1,itemListLong=1):
            if pm.menuItem(item,q=1,label=1) == prefix and prefix != "None":
                break
        else:
            QtWidgets.QMessageBox.information(self,u"警告",u"当前选择没有找到 HumanIK 所属")
            return

        top_parent = sel.fullPath().split("|")[1]
        if mode == "ctrl":
            top_parent = top_parent.replace("_Ctrl_","_")

        return top_parent

    def matchRig(self):
        QuickRig = self.QuickRigGet.LE.text()
        HumanRig = self.HumanRigGet.LE.text()
        prefix = HumanRig.split("_")[0]
        _prefix = QuickRig.split("_")[0]
        pm.undoInfo(ock=1)
        for quick in pm.ls(QuickRig,dag=1,type="joint"):
            human = quick.replace(_prefix,prefix)
            human = pm.PyNode(human)
            quick_pos = quick.getTranslation(space="world")
            human.setTranslation(quick_pos,space="world")
        pm.undoInfo(cck=1)

    def mayaShow(self, win_name="HumanIK_Match"):
        def mayaToQT(name):
            # Maya -> QWidget
            ptr = omui.MQtUtil.findControl(name)
            if ptr is None:
                ptr = omui.MQtUtil.findLayout(name)
            if ptr is None:
                ptr = omui.MQtUtil.findMenuItem(name)
            if ptr is not None:
                return QtCompat.wrapInstance(long(ptr), QtWidgets.QWidget)

        # NOTE 如果变量存在 就检查窗口多开
        if pm.window(win_name, q=1, ex=1):
            pm.deleteUI(win_name)

        window = pm.window(win_name, title=self.windowTitle())

        pm.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        ptr = mayaToQT(window)
        ptr.setLayout(QtWidgets.QVBoxLayout())
        ptr.layout().setContentsMargins(0, 0, 0, 0)
        ptr.layout().addWidget(self)

        return ptr


if __name__ == "__main__":
    window = HumanIKMatchUI()
    window.mayaShow()