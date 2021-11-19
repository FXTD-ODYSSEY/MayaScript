# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from dayu_widgets.push_button import MPushButton
from dayu_widgets.combo_box import MComboBox
from dayu_widgets.line_edit import MLineEdit
from dayu_widgets.check_box import MCheckBox
from dayu_widgets.radio_button import MRadioButton
from dayu_widgets.item_view import MTableView
from dayu_widgets.spin_box import MSpinBox
from dayu_widgets.tab_widget import MTabWidget


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(835, 966)
        self.actionopen = QAction(Form)
        self.actionopen.setObjectName(u"actionopen")
        self.actionopen.setText(u"open")
        self.actionsave = QAction(Form)
        self.actionsave.setObjectName(u"actionsave")
        self.menubar = QMenuBar(Form)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 9999, 23))
        self.menufile = QMenu(self.menubar)
        self.menufile.setObjectName(u"menufile")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 25, -1, -1)
        self.horizontalWidget_2 = QWidget(Form)
        self.horizontalWidget_2.setObjectName(u"horizontalWidget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget_2.sizePolicy().hasHeightForWidth())
        self.horizontalWidget_2.setSizePolicy(sizePolicy)
        self.horizontalWidget_2.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setFamily(u"Microsoft YaHei")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.horizontalWidget_2.setFont(font)
        self.horizontalWidget_2.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.horizontalWidget_2)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setFamily(u"Microsoft YaHei")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setWeight(75)
        self.label_4.setFont(font1)
        self.label_4.setStyleSheet(u"font: bold 12pt \"Microsoft YaHei\";\n"
"")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.Controller_Combo = MComboBox(self.horizontalWidget_2)
        self.Controller_Combo.setObjectName(u"Controller_Combo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Controller_Combo.sizePolicy().hasHeightForWidth())
        self.Controller_Combo.setSizePolicy(sizePolicy1)
        self.Controller_Combo.setFont(font)

        self.horizontalLayout_2.addWidget(self.Controller_Combo)


        self.verticalLayout.addWidget(self.horizontalWidget_2)

        self.Splitter = QSplitter(Form)
        self.Splitter.setObjectName(u"Splitter")
        self.Splitter.setStyleSheet(u"font: bold 12pt \"Microsoft YaHei\";")
        self.Splitter.setOrientation(Qt.Horizontal)
        self.Splitter.setOpaqueResize(True)
        self.Splitter.setHandleWidth(10)
        self.Splitter.setChildrenCollapsible(True)
        self.tabWidget = MTabWidget(self.Splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"font-weight:bold")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidgetPage1 = QWidget()
        self.tabWidgetPage1.setObjectName(u"tabWidgetPage1")
        self.verticalLayout_2 = QVBoxLayout(self.tabWidgetPage1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, -1, 9, -1)
        self.groupBox = QGroupBox(self.tabWidgetPage1)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font1)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.Ignore_Case_CB = MCheckBox(self.groupBox)
        self.Ignore_Case_CB.setObjectName(u"Ignore_Case_CB")

        self.gridLayout.addWidget(self.Ignore_Case_CB, 4, 0, 1, 1)

        self.RE_CB = MCheckBox(self.groupBox)
        self.RE_CB.setObjectName(u"RE_CB")

        self.gridLayout.addWidget(self.RE_CB, 3, 0, 1, 1)

        self.Convention_CB = MCheckBox(self.groupBox)
        self.Convention_CB.setObjectName(u"Convention_CB")

        self.gridLayout.addWidget(self.Convention_CB, 1, 0, 1, 1)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 2, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(self.tabWidgetPage1)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setFont(font1)
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.Prefix_CB = MCheckBox(self.groupBox_4)
        self.Prefix_CB.setObjectName(u"Prefix_CB")

        self.horizontalLayout_9.addWidget(self.Prefix_CB)

        self.Prefix_LE = MLineEdit(self.groupBox_4)
        self.Prefix_LE.setObjectName(u"Prefix_LE")
        self.Prefix_LE.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.Prefix_LE)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.Suffix_CB = MCheckBox(self.groupBox_4)
        self.Suffix_CB.setObjectName(u"Suffix_CB")

        self.horizontalLayout_10.addWidget(self.Suffix_CB)

        self.Suffix_LE = MLineEdit(self.groupBox_4)
        self.Suffix_LE.setObjectName(u"Suffix_LE")
        self.Suffix_LE.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.Suffix_LE)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)


        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.tabWidgetPage1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy2)
        self.groupBox_3.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_3.setFont(font1)
        self.groupBox_3.setAutoFillBackground(False)
        self.groupBox_3.setStyleSheet(u"")
        self.groupBox_3.setTitle(u"\u6587\u4ef6\u5e8f\u53f7{INDEX}")
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setCheckable(False)
        self.groupBox_3.setChecked(False)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_5.addWidget(self.label)

        self.Index_Combo = MComboBox(self.groupBox_3)
        self.Index_Combo.addItem("")
        self.Index_Combo.addItem("")
        self.Index_Combo.setObjectName(u"Index_Combo")
        sizePolicy1.setHeightForWidth(self.Index_Combo.sizePolicy().hasHeightForWidth())
        self.Index_Combo.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.Index_Combo)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.stackedWidget = QStackedWidget(self.groupBox_3)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy3)
        self.stackedWidget.setMaximumSize(QSize(16777215, 16777215))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        sizePolicy3.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy3)
        self.horizontalLayout_6 = QHBoxLayout(self.page)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_6.addWidget(self.label_2)

        self.Padding_SP = MSpinBox(self.page)
        self.Padding_SP.setObjectName(u"Padding_SP")
        sizePolicy1.setHeightForWidth(self.Padding_SP.sizePolicy().hasHeightForWidth())
        self.Padding_SP.setSizePolicy(sizePolicy1)
        self.Padding_SP.setMinimum(1)

        self.horizontalLayout_6.addWidget(self.Padding_SP)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        sizePolicy3.setHeightForWidth(self.page_2.sizePolicy().hasHeightForWidth())
        self.page_2.setSizePolicy(sizePolicy3)
        self.horizontalLayout_7 = QHBoxLayout(self.page_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.page_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.groupBox_2.setStyleSheet(u"border:none")
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.horizontalLayout_8 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.Lower_CB = MRadioButton(self.groupBox_2)
        self.Lower_CB.setObjectName(u"Lower_CB")
        self.Lower_CB.setChecked(True)

        self.horizontalLayout_8.addWidget(self.Lower_CB)

        self.Upper_CB = MRadioButton(self.groupBox_2)
        self.Upper_CB.setObjectName(u"Upper_CB")

        self.horizontalLayout_8.addWidget(self.Upper_CB)


        self.horizontalLayout_7.addWidget(self.groupBox_2)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_5.addWidget(self.stackedWidget)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.Variable_Group = QGroupBox(self.tabWidgetPage1)
        self.Variable_Group.setObjectName(u"Variable_Group")
        self.verticalLayout_11 = QVBoxLayout(self.Variable_Group)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.INDEX_CB = MCheckBox(self.Variable_Group)
        self.INDEX_CB.setObjectName(u"INDEX_CB")
        self.INDEX_CB.setChecked(True)

        self.verticalLayout_11.addWidget(self.INDEX_CB)

        self.ORIGIN_NAME_CB = MCheckBox(self.Variable_Group)
        self.ORIGIN_NAME_CB.setObjectName(u"ORIGIN_NAME_CB")
        self.ORIGIN_NAME_CB.setChecked(True)

        self.verticalLayout_11.addWidget(self.ORIGIN_NAME_CB)

        self.MATCH_CB = MCheckBox(self.Variable_Group)
        self.MATCH_CB.setObjectName(u"MATCH_CB")
        self.MATCH_CB.setChecked(True)

        self.verticalLayout_11.addWidget(self.MATCH_CB)

        self.ASSET_PATH_CB = MCheckBox(self.Variable_Group)
        self.ASSET_PATH_CB.setObjectName(u"ASSET_PATH_CB")
        self.ASSET_PATH_CB.setChecked(True)

        self.verticalLayout_11.addWidget(self.ASSET_PATH_CB)

        self.FOLDER_PATH_CB = MCheckBox(self.Variable_Group)
        self.FOLDER_PATH_CB.setObjectName(u"FOLDER_PATH_CB")
        self.FOLDER_PATH_CB.setChecked(True)

        self.verticalLayout_11.addWidget(self.FOLDER_PATH_CB)

        self.ASSET_FILE_PATH_CB = MCheckBox(self.Variable_Group)
        self.ASSET_FILE_PATH_CB.setObjectName(u"ASSET_FILE_PATH_CB")
        self.ASSET_FILE_PATH_CB.setChecked(True)

        self.verticalLayout_11.addWidget(self.ASSET_FILE_PATH_CB)

        self.ASSET_CLASS_CB = MCheckBox(self.Variable_Group)
        self.ASSET_CLASS_CB.setObjectName(u"ASSET_CLASS_CB")
        self.ASSET_CLASS_CB.setChecked(True)

        self.verticalLayout_11.addWidget(self.ASSET_CLASS_CB)

        self.ASSET_CLASS_LONG_CB = MCheckBox(self.Variable_Group)
        self.ASSET_CLASS_LONG_CB.setObjectName(u"ASSET_CLASS_LONG_CB")
        self.ASSET_CLASS_LONG_CB.setChecked(True)

        self.verticalLayout_11.addWidget(self.ASSET_CLASS_LONG_CB)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setSizeConstraint(QLayout.SetFixedSize)
        self.Select_All_BTN = MPushButton(self.Variable_Group)
        self.Select_All_BTN.setObjectName(u"Select_All_BTN")

        self.horizontalLayout_24.addWidget(self.Select_All_BTN)

        self.Toggle_Select_BTN = MPushButton(self.Variable_Group)
        self.Toggle_Select_BTN.setObjectName(u"Toggle_Select_BTN")

        self.horizontalLayout_24.addWidget(self.Toggle_Select_BTN)

        self.Non_Select_BTN = MPushButton(self.Variable_Group)
        self.Non_Select_BTN.setObjectName(u"Non_Select_BTN")

        self.horizontalLayout_24.addWidget(self.Non_Select_BTN)


        self.verticalLayout_11.addLayout(self.horizontalLayout_24)


        self.verticalLayout_2.addWidget(self.Variable_Group)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.Splitter.addWidget(self.tabWidget)
        self.layoutWidget = QWidget(self.Splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_6 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Selector_Label_3 = QLabel(self.layoutWidget)
        self.Selector_Label_3.setObjectName(u"Selector_Label_3")

        self.horizontalLayout_3.addWidget(self.Selector_Label_3)

        self.Search_LE = MLineEdit(self.layoutWidget)
        self.Search_LE.setObjectName(u"Search_LE")
        sizePolicy1.setHeightForWidth(self.Search_LE.sizePolicy().hasHeightForWidth())
        self.Search_LE.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.Search_LE)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.Selector_Label_2 = QLabel(self.layoutWidget)
        self.Selector_Label_2.setObjectName(u"Selector_Label_2")

        self.horizontalLayout_4.addWidget(self.Selector_Label_2)

        self.Replace_LE = MLineEdit(self.layoutWidget)
        self.Replace_LE.setObjectName(u"Replace_LE")
        sizePolicy1.setHeightForWidth(self.Replace_LE.sizePolicy().hasHeightForWidth())
        self.Replace_LE.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.Replace_LE)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalWidget = QWidget(self.layoutWidget)
        self.horizontalWidget.setObjectName(u"horizontalWidget")
        self.horizontalWidget.setMinimumSize(QSize(0, 0))
        self.horizontalWidget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_11 = QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.Table_View = MTableView(self.horizontalWidget)
        self.Table_View.setObjectName(u"Table_View")
        sizePolicy.setHeightForWidth(self.Table_View.sizePolicy().hasHeightForWidth())
        self.Table_View.setSizePolicy(sizePolicy)
        self.Table_View.setMinimumSize(QSize(0, 0))
        self.Table_View.setMaximumSize(QSize(16777215, 16777215))
        self.Table_View.setSizeIncrement(QSize(0, 0))
        self.Table_View.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Table_View.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.Table_View.setDragEnabled(True)
        self.Table_View.setDragDropMode(QAbstractItemView.InternalMove)
        self.Table_View.setDefaultDropAction(Qt.MoveAction)
        self.Table_View.setAlternatingRowColors(True)
        self.Table_View.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.Table_View.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.Table_View.setShowGrid(True)
        self.Table_View.setCornerButtonEnabled(True)
        self.Table_View.horizontalHeader().setCascadingSectionResizes(False)
        self.Table_View.horizontalHeader().setStretchLastSection(False)
        self.Table_View.verticalHeader().setCascadingSectionResizes(False)
        self.Table_View.verticalHeader().setStretchLastSection(False)

        self.horizontalLayout_11.addWidget(self.Table_View)

        self.Arrow_Container = QFrame(self.horizontalWidget)
        self.Arrow_Container.setObjectName(u"Arrow_Container")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.Arrow_Container.sizePolicy().hasHeightForWidth())
        self.Arrow_Container.setSizePolicy(sizePolicy4)
        self.Arrow_Container.setMinimumSize(QSize(0, 0))
        self.Arrow_Container.setMaximumSize(QSize(16777215, 16777215))
        self.Arrow_Container.setFrameShape(QFrame.NoFrame)
        self.Arrow_Container.setFrameShadow(QFrame.Raised)
        self.Arrow_Container.setLineWidth(2)
        self.verticalLayout_3 = QVBoxLayout(self.Arrow_Container)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.Update_BTN = MPushButton(self.Arrow_Container)
        self.Update_BTN.setObjectName(u"Update_BTN")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.Update_BTN.sizePolicy().hasHeightForWidth())
        self.Update_BTN.setSizePolicy(sizePolicy5)
        self.Update_BTN.setMaximumSize(QSize(25, 25))
        self.Update_BTN.setBaseSize(QSize(0, 0))

        self.verticalLayout_3.addWidget(self.Update_BTN)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)

        self.Get_Actor_BTN = MPushButton(self.Arrow_Container)
        self.Get_Actor_BTN.setObjectName(u"Get_Actor_BTN")
        sizePolicy5.setHeightForWidth(self.Get_Actor_BTN.sizePolicy().hasHeightForWidth())
        self.Get_Actor_BTN.setSizePolicy(sizePolicy5)
        self.Get_Actor_BTN.setMaximumSize(QSize(25, 25))
        self.Get_Actor_BTN.setBaseSize(QSize(0, 0))

        self.verticalLayout_3.addWidget(self.Get_Actor_BTN)

        self.Get_Asset_BTN = MPushButton(self.Arrow_Container)
        self.Get_Asset_BTN.setObjectName(u"Get_Asset_BTN")
        sizePolicy5.setHeightForWidth(self.Get_Asset_BTN.sizePolicy().hasHeightForWidth())
        self.Get_Asset_BTN.setSizePolicy(sizePolicy5)
        self.Get_Asset_BTN.setMaximumSize(QSize(25, 25))
        self.Get_Asset_BTN.setBaseSize(QSize(0, 0))

        self.verticalLayout_3.addWidget(self.Get_Asset_BTN)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.Find_BTN = MPushButton(self.Arrow_Container)
        self.Find_BTN.setObjectName(u"Find_BTN")
        sizePolicy5.setHeightForWidth(self.Find_BTN.sizePolicy().hasHeightForWidth())
        self.Find_BTN.setSizePolicy(sizePolicy5)
        self.Find_BTN.setMaximumSize(QSize(25, 25))
        self.Find_BTN.setBaseSize(QSize(0, 0))

        self.verticalLayout_3.addWidget(self.Find_BTN)

        self.Drive_BTN = MPushButton(self.Arrow_Container)
        self.Drive_BTN.setObjectName(u"Drive_BTN")
        sizePolicy5.setHeightForWidth(self.Drive_BTN.sizePolicy().hasHeightForWidth())
        self.Drive_BTN.setSizePolicy(sizePolicy5)
        self.Drive_BTN.setMaximumSize(QSize(25, 25))
        self.Drive_BTN.setBaseSize(QSize(0, 0))

        self.verticalLayout_3.addWidget(self.Drive_BTN)

        self.Del_BTN = MPushButton(self.Arrow_Container)
        self.Del_BTN.setObjectName(u"Del_BTN")
        sizePolicy5.setHeightForWidth(self.Del_BTN.sizePolicy().hasHeightForWidth())
        self.Del_BTN.setSizePolicy(sizePolicy5)
        self.Del_BTN.setMaximumSize(QSize(25, 25))
        self.Del_BTN.setBaseSize(QSize(0, 0))

        self.verticalLayout_3.addWidget(self.Del_BTN)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.Up_BTN = MPushButton(self.Arrow_Container)
        self.Up_BTN.setObjectName(u"Up_BTN")
        sizePolicy5.setHeightForWidth(self.Up_BTN.sizePolicy().hasHeightForWidth())
        self.Up_BTN.setSizePolicy(sizePolicy5)
        self.Up_BTN.setMaximumSize(QSize(25, 25))
        self.Up_BTN.setBaseSize(QSize(0, 0))

        self.verticalLayout_3.addWidget(self.Up_BTN)

        self.Dn_BTN = MPushButton(self.Arrow_Container)
        self.Dn_BTN.setObjectName(u"Dn_BTN")
        sizePolicy5.setHeightForWidth(self.Dn_BTN.sizePolicy().hasHeightForWidth())
        self.Dn_BTN.setSizePolicy(sizePolicy5)
        self.Dn_BTN.setMinimumSize(QSize(0, 0))
        self.Dn_BTN.setMaximumSize(QSize(25, 25))

        self.verticalLayout_3.addWidget(self.Dn_BTN)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_6)


        self.horizontalLayout_11.addWidget(self.Arrow_Container)


        self.verticalLayout_6.addWidget(self.horizontalWidget)

        self.Rename_BTN = MPushButton(self.layoutWidget)
        self.Rename_BTN.setObjectName(u"Rename_BTN")
        font2 = QFont()
        font2.setFamily(u"Microsoft YaHei")
        font2.setBold(True)
        font2.setItalic(False)
        font2.setWeight(75)
        self.Rename_BTN.setFont(font2)
        self.Rename_BTN.setStyleSheet(u"font-weight:bold;\n"
"font-size:18px;")

        self.verticalLayout_6.addWidget(self.Rename_BTN)

        self.Splitter.addWidget(self.layoutWidget)

        self.verticalLayout.addWidget(self.Splitter)


        self.menubar.addAction(self.menufile.menuAction())
        self.menufile.addAction(self.actionopen)
        self.menufile.addAction(self.actionsave)

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.actionsave.setText(QCoreApplication.translate("Form", u"save", None))
        self.menufile.setTitle(QCoreApplication.translate("Form", u"file", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u8bed\u8a00\u9009\u62e9", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u9009\u9879", None))
        self.Ignore_Case_CB.setText(QCoreApplication.translate("Form", u"\u4e0d\u533a\u5206\u5927\u5c0f\u5199", None))
        self.RE_CB.setText(QCoreApplication.translate("Form", u"\u6b63\u5219\u8868\u8fbe\u5f0f", None))
        self.Convention_CB.setText(QCoreApplication.translate("Form", u"\u547d\u540d\u89c4\u8303 - \u81ea\u52a8\u5339\u914d", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"\u524d\u540e\u7f00", None))
        self.Prefix_CB.setText(QCoreApplication.translate("Form", u"\u524d\u7f00", None))
        self.Suffix_CB.setText(QCoreApplication.translate("Form", u"\u540e\u7f00", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u5e8f\u53f7\u65b9\u5f0f", None))
        self.Index_Combo.setItemText(0, QCoreApplication.translate("Form", u"\u6570\u5b57(0-9)", None))
        self.Index_Combo.setItemText(1, QCoreApplication.translate("Form", u"\u5b57\u6bcd(a-z)", None))

        self.label_2.setText(QCoreApplication.translate("Form", u"\u7f16\u53f7\u589e\u91cf", None))
        self.groupBox_2.setTitle("")
        self.Lower_CB.setText(QCoreApplication.translate("Form", u"\u5c0f\u5199", None))
        self.Upper_CB.setText(QCoreApplication.translate("Form", u"\u5927\u5199", None))
        self.Variable_Group.setTitle(QCoreApplication.translate("Form", u"\u53d8\u91cf\u914d\u7f6e", None))
        self.INDEX_CB.setText(QCoreApplication.translate("Form", u"\u8d44\u6e90\u5e8f\u53f7       ${INDEX} ", None))
        self.ORIGIN_NAME_CB.setText(QCoreApplication.translate("Form", u"\u8d44\u6e90\u539f\u540d\u79f0     ${ORIGIN_NAME} ", None))
        self.MATCH_CB.setText(QCoreApplication.translate("Form", u"\u5339\u914d\u7684\u5173\u952e\u5b57   ${MATCH} ", None))
        self.ASSET_PATH_CB.setText(QCoreApplication.translate("Form", u"\u8d44\u6e90\u5f15\u64ce\u8def\u5f84   ${ASSET_PATH} ", None))
        self.FOLDER_PATH_CB.setText(QCoreApplication.translate("Form", u"\u8d44\u6e90\u6587\u4ef6\u5939\u8def\u5f84 ${FOLDER_PATH} ", None))
        self.ASSET_FILE_PATH_CB.setText(QCoreApplication.translate("Form", u"\u8d44\u6e90\u672c\u5730\u8def\u5f84   ${ASSET_FILE_PATH} ", None))
        self.ASSET_CLASS_CB.setText(QCoreApplication.translate("Form", u"\u8d44\u6e90\u7c7b\u540d\u7b80\u5199   ${ASSET_CLASS} ", None))
        self.ASSET_CLASS_LONG_CB.setText(QCoreApplication.translate("Form", u"\u8d44\u6e90\u7c7b\u540d\u5168\u7a0b   ${ASSET_CLASS_LONG} ", None))
        self.Select_All_BTN.setText(QCoreApplication.translate("Form", u"\u5168\u9009", None))
        self.Toggle_Select_BTN.setText(QCoreApplication.translate("Form", u"\u53cd\u9009", None))
        self.Non_Select_BTN.setText(QCoreApplication.translate("Form", u"\u5168\u4e0d\u9009", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), QCoreApplication.translate("Form", u"\u914d\u7f6e", None))
        self.Selector_Label_3.setText(QCoreApplication.translate("Form", u"\u67e5\u627e:", None))
        self.Search_LE.setPlaceholderText(QCoreApplication.translate("Form", u"asd", None))
        self.Selector_Label_2.setText(QCoreApplication.translate("Form", u"\u66ff\u6362:", None))
#if QT_CONFIG(tooltip)
        self.Update_BTN.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u5237\u65b0</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Update_BTN.setText("")
#if QT_CONFIG(tooltip)
        self.Get_Actor_BTN.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">\u83b7\u53d6\u6587\u4ef6</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Get_Actor_BTN.setText("")
#if QT_CONFIG(tooltip)
        self.Get_Asset_BTN.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">\u83b7\u53d6\u6587\u4ef6</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Get_Asset_BTN.setText("")
#if QT_CONFIG(tooltip)
        self.Find_BTN.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">\u5b9a\u4f4d\u6587\u4ef6</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Find_BTN.setText("")
#if QT_CONFIG(tooltip)
        self.Drive_BTN.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">\u6253\u5f00\u7cfb\u7edf\u76ee\u5f55\u8def\u5f84</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Drive_BTN.setText("")
#if QT_CONFIG(tooltip)
        self.Del_BTN.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">\u5220\u9664\u6587\u4ef6</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Del_BTN.setText("")
#if QT_CONFIG(tooltip)
        self.Up_BTN.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">\u4e0a\u79fb</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Up_BTN.setText("")
#if QT_CONFIG(tooltip)
        self.Dn_BTN.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">\u4e0b\u79fb</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Dn_BTN.setText("")
        self.Rename_BTN.setText(QCoreApplication.translate("Form", u"\u6279\u91cf\u6539\u540d", None))
    # retranslateUi

