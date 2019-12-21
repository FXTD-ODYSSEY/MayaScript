# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-20 16:52:15'

"""
挤出轮廓边
"""


from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from Qt.QtCompat import wrapInstance
from Qt.QtCompat import loadUi

import os
from maya import OpenMayaUI
import pymel.core as pm

# class outlineExtrude_UI(object):
#     def setupUi(self, Form):
#         Form.setObjectName("Form")
#         Form.resize(410, 176)
#         self.verticalLayout = QtWidgets.QVBoxLayout(Form)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.Extrude_BTN = QtWidgets.QPushButton(Form)
#         self.Extrude_BTN.setObjectName("Extrude_BTN")
#         self.verticalLayout.addWidget(self.Extrude_BTN)
#         self.horizontalLayout = QtWidgets.QHBoxLayout()
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         self.label = QtWidgets.QLabel(Form)
#         self.label.setObjectName("label")
#         self.horizontalLayout.addWidget(self.label)
#         self.Extrude_LE = QtWidgets.QLineEdit(Form)
#         self.Extrude_LE.setObjectName("Extrude_LE")
#         self.horizontalLayout.addWidget(self.Extrude_LE)
#         self.Extrude_Get = QtWidgets.QPushButton(Form)
#         self.Extrude_Get.setObjectName("Extrude_Get")
#         self.horizontalLayout.addWidget(self.Extrude_Get)
#         self.verticalLayout.addLayout(self.horizontalLayout)
#         self.verticalWidget = QtWidgets.QWidget(Form)
#         self.verticalWidget.setObjectName("verticalWidget")
#         self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget)
#         self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
#         self.verticalLayout_2.setObjectName("verticalLayout_2")
#         self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
#         self.horizontalLayout_3.setObjectName("horizontalLayout_3")
#         self.label_3 = QtWidgets.QLabel(self.verticalWidget)
#         self.label_3.setObjectName("label_3")
#         self.horizontalLayout_3.addWidget(self.label_3)
#         self.Thickness_sp = QtWidgets.QDoubleSpinBox(self.verticalWidget)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.Thickness_sp.sizePolicy().hasHeightForWidth())
#         self.Thickness_sp.setSizePolicy(sizePolicy)
#         self.Thickness_sp.setObjectName("Thickness_sp")
#         self.horizontalLayout_3.addWidget(self.Thickness_sp)
#         self.verticalLayout_2.addLayout(self.horizontalLayout_3)
#         self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
#         self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#         self.label_2 = QtWidgets.QLabel(self.verticalWidget)
#         self.label_2.setObjectName("label_2")
#         self.horizontalLayout_2.addWidget(self.label_2)
#         self.Angle_SP = QtWidgets.QDoubleSpinBox(self.verticalWidget)
#         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.Angle_SP.sizePolicy().hasHeightForWidth())
#         self.Angle_SP.setSizePolicy(sizePolicy)
#         self.Angle_SP.setObjectName("Angle_SP")
#         self.horizontalLayout_2.addWidget(self.Angle_SP)
#         self.verticalLayout_2.addLayout(self.horizontalLayout_2)
#         self.verticalLayout.addWidget(self.verticalWidget)
#         spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
#         self.verticalLayout.addItem(spacerItem)

#         self.retranslateUi(Form)
#         QtCore.QMetaObject.connectSlotsByName(Form)

#     def retranslateUi(self, Form):
#         Form.setWindowTitle(u"挤出轮廓")
#         self.Extrude_BTN.setText(u"挤出边")
#         self.label.setText(u"挤出节点")
#         self.Extrude_Get.setText(u"获取")
#         self.label_3.setText(u"厚度调整")
#         self.label_2.setText(u"角度调整")


class outlineExtrude(QtWidgets.QWidget):

    def __init__(self):
        super(outlineExtrude,self).__init__()
        DIR = os.path.dirname(__file__)
        ui_file = os.path.join(DIR,"outline.ui")
        loadUi(ui_file,self)

        self.Adjust_Layout.setEnabled(False)

        self.extrude_node = None
        self.origin_edge_list = None

        self.Extrude_BTN.clicked.connect(self.extrudeFn)
        self.Thickness_sp.valueChanged.connect(self.thicknessAdjust)
        self.Angle_SP.valueChanged.connect(self.angleAdjust)

    def extrudeFn(self):
        self.origin_edge_list = [sel for sel in pm.ls(sl=1) if type(sel) == pm.general.MeshEdge]

        if not self.origin_edge_list:
            QtWidgets.QMessageBox(self,u"警告",u"请选择边")
            return

        for edge in self.origin_edge_list:
                
            self.extrude_node = pm.polyExtrudeEdge(edge,ch=1,thickness=0.1)[0]
            self.Extrude_LE.setText(self.extrude_node.name())
            self.Thickness_sp.setValue(0.1)
            self.Adjust_Layout.setEnabled(True)

            self.extrude_edge_list = [sel for sel in pm.ls(sl=1) if type(sel) == pm.general.MeshEdge]

    def thicknessAdjust(self,value):
        self.extrude_node.thickness.set(value)

    def angleAdjust(self,value):
        self.extrude_node.localTranslateY.set(value)

    def mayaShow(self,name="outlineExtrude"):
        # NOTE 如果变量存在 就检查窗口多开
        if pm.window(name,q=1,ex=1):
            pm.deleteUI(name)
        window = pm.window(name,title=self.windowTitle())
        pm.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        ptr = self.mayaToQT(window)
        ptr.setLayout(QtWidgets.QVBoxLayout())
        ptr.layout().setContentsMargins(0,0,0,0)
        ptr.layout().addWidget(self)
        ptr.destroyed.connect(self._close)

        return ptr
        
    def _close(self):
        # NOTE 脱离要删除的窗口
        window = OpenMayaUI.MQtUtil.mainWindow()
        window = wrapInstance(long(window), QtWidgets.QMainWindow)
        self.setParent(window)
    
    def mayaToQT( self,name ):
        # Maya -> QWidget
        ptr = OpenMayaUI.MQtUtil.findControl( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findLayout( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
        if ptr is not None: return wrapInstance( long( ptr ), QtWidgets.QWidget )


if __name__ == "__main__":
    pass
    # win = outlineExtrude()
    # win.show()

# import sys
# MODULE = r"F:\MayaTecent\MayaScript\model\outline"
# if MODULE not in sys.path:
#     sys.path.append(MODULE)

# import outlineExtrude
# reload(outlineExtrude)
# from outlineExtrude import outlineExtrude
# win = outlineExtrude()
# win.mayaShow()