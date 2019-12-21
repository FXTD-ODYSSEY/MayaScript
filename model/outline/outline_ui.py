# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\MayaTecent\MayaScript\model\outline\outline.ui'
#
# Created: Fri Dec 20 16:56:06 2019
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(410, 176)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Extrude_BTN = QtWidgets.QPushButton(Form)
        self.Extrude_BTN.setObjectName("Extrude_BTN")
        self.verticalLayout.addWidget(self.Extrude_BTN)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Extrude_LE = QtWidgets.QLineEdit(Form)
        self.Extrude_LE.setObjectName("Extrude_LE")
        self.horizontalLayout.addWidget(self.Extrude_LE)
        self.Extrude_Get = QtWidgets.QPushButton(Form)
        self.Extrude_Get.setObjectName("Extrude_Get")
        self.horizontalLayout.addWidget(self.Extrude_Get)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalWidget = QtWidgets.QWidget(Form)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.verticalWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.Thickness_sp = QtWidgets.QDoubleSpinBox(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Thickness_sp.sizePolicy().hasHeightForWidth())
        self.Thickness_sp.setSizePolicy(sizePolicy)
        self.Thickness_sp.setObjectName("Thickness_sp")
        self.horizontalLayout_3.addWidget(self.Thickness_sp)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.Angle_SP = QtWidgets.QDoubleSpinBox(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Angle_SP.sizePolicy().hasHeightForWidth())
        self.Angle_SP.setSizePolicy(sizePolicy)
        self.Angle_SP.setObjectName("Angle_SP")
        self.horizontalLayout_2.addWidget(self.Angle_SP)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.verticalWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "挤出轮廓", None, -1))
        self.Extrude_BTN.setText(QtWidgets.QApplication.translate("Form", "挤出边", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "挤出节点", None, -1))
        self.Extrude_Get.setText(QtWidgets.QApplication.translate("Form", "获取", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "厚度调整", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "角度调整", None, -1))

