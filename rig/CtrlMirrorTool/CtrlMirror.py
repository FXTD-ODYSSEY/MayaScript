# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-13 19:46:02'

"""
控制器镜像工具
"""

import os
import re
import json
import time
import itertools
from functools import partial

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets
from Qt.QtCompat import loadUi
from Qt.QtCompat import wrapInstance


from maya import OpenMayaUI
from maya import mel
import pymel.core as pm
import pymel.core.datatypes as dt
import pymel.core.nodetypes as nt

from CtrlMirrorUtils import CollapsibleWidget
from CtrlMirrorUtils import SpliterWidget

MATCH_DICT = {
    r"^Rt"  : r"^Lf",
    r"_Rt_" : r"_Lf_",
    r"^R_"  : r"^L_",
    r"_R_"  : r"_L_",
}

class CtrlMirror(QtWidgets.QWidget):
    def __init__(self):
        super(CtrlMirror,self).__init__()
        DIR = os.path.dirname(__file__)
        ui_file = os.path.join(DIR,"ui","CtrlMirror.ui")
        loadUi(ui_file,self)

        self.R_list = {}
        self.L_list = {}
        self.R_matches = {}
        self.L_matches = {}
        self.C_matches = {}
        self.N_matches = {}
        self.thersold = 0.05
        self.axis = "z"

        self.Test_BTN.clicked.connect(self.TEST)
        CollapsibleWidget.install(self.Get_Match_Toggle,self.Get_Match_Layout)
        _,anim = CollapsibleWidget.install(self.Match_Toggle,self.Match_Layout)
        anim.finished.connect(self.TEST)

        CollapsibleWidget.install(self.Anim_Mirror_Toggle,self.Anim_Mirror_Layout)
        SpliterWidget.install(self.Match_Widget,self.Unmatch_Widget)

        self.Anim_Mirror_Layout.setEnabled(False)
        
        self.XY_RB.clicked.connect(partial(self.setAxis,"z"))
        self.XZ_RB.clicked.connect(partial(self.setAxis,"y"))
        self.YZ_RB.clicked.connect(partial(self.setAxis,"x"))

        self.Get_Matched_BTN.clicked.connect(self.getMatches)

        
        self.L_Match_List.itemDoubleClicked.connect(self.selectItem)
        self.R_Match_List.itemDoubleClicked.connect(self.selectItem)
        self.Unmatch_List.itemDoubleClicked.connect(self.selectItem)
        
        self.vs1 = self.L_Match_List.verticalScrollBar()
        self.vs2 = self.R_Match_List.verticalScrollBar()

        self.vs1.valueChanged.connect(self.syncScroll)
        self.vs2.valueChanged.connect(self.syncScroll)

        self.Mirror_Shape_BTN.clicked.connect(self.mirrorCrvShape)

        self.setStyleSheet('font-family: Microsoft YaHei UI;')

    def TEST(self):
        print self.Match_Layout.sizePolicy()
        print self.Match_Layout.sizeHint()
        print self.Match_Layout.height()
        print self.Match_Layout.maximumHeight()
        # if not self.Match_Toggle.toggleCollapse:
        #     self.Match_Layout.setMaximumHeight(16777215)

    def syncScroll(self,value):
        self.vs1.setValue(value)
        self.vs2.setValue(value)

    def setAxis(self,axis):
        self.axis = axis

    def selectItem(self,item):
        item = item.text()
        if pm.objExists(item):
            pm.select(item)
        else:
            pm.warning(u"物体不存在了")
            pm.headsUpMessage(u"物体不存在了")

    def negativeAxis(self,vec):
        return dt.Vector([-eval("vec.%s" % _axis) if self.axis == _axis else eval("vec.%s" % _axis) for _axis in ['x','y','z']])

    def findNameMatchCtrl(self,transform):
        for R,L in MATCH_DICT.items():
            Lm = re.search(L,transform.name())
            Rm = re.search(R,transform.name())
            if Lm:
                name = re.sub(L,R.replace("^",""),transform.name())
            elif Rm:
                name = re.sub(R,L.replace("^",""),transform.name())
            else:
                return
            
            if pm.objExists(name):
                return pm.PyNode(name)

    
    def getMatches(self):
        self.R_list = {}
        self.L_list = {}
        self.R_matches = {}
        self.L_matches = {}
        self.C_matches = {}
        self.N_matches = {}

        crv_list = pm.ls(ni=1,type="nurbsCurve")

        for crv in crv_list:
            transform = crv.getParent()

            if not transform.listAttr(k=1) or transform.listConnections(d=0,c=1,type="constraint"):
                continue

            pos = transform.getRotatePivot(space="world")
            attr = eval("pos.%s" % self.axis)
            if attr > self.thersold:
                self.R_list[transform] = pos
            elif attr < -self.thersold:
                self.L_list[transform] = pos
            else:
                self.C_matches[transform] = pos

        for R_ctrl,R_pos in self.R_list.items():

            L_ctrl = self.findNameMatchCtrl(R_ctrl)
            if L_ctrl:
                self.R_matches[R_ctrl] = L_ctrl
                self.L_matches[L_ctrl] = R_ctrl
                continue

            R_pos = self.negativeAxis(R_pos)
            R_end = R_ctrl.split("_")[-1]
            for L_ctrl,L_pos in self.L_list.items():
                if (R_pos - L_pos).length() < self.thersold:
                    if R_end == L_ctrl.split("_")[-1]:
                        self.R_matches[R_ctrl] = L_ctrl
                        self.L_matches[L_ctrl] = R_ctrl
                        break
            else:
                self.N_matches[R_ctrl] = R_pos

        # self.C_matches.update(no_matches)

        self.updateList()

    def updateList(self):
        self.L_Match_List.clear()
        self.R_Match_List.clear()
        self.C_Match_List.clear()
        self.Unmatch_List.clear()

        for ctrl in self.C_matches:
            self.C_Match_List.addItem(str(ctrl))

        for ctrl in self.N_matches:
            self.Unmatch_List.addItem(str(ctrl))

        for R,L in self.R_matches.items():
            self.L_Match_List.addItem(str(L))
            self.R_Match_List.addItem(str(R))

        self.Mirror_Shape_BTN.setEnabled(True)
        self.Anim_Mirror_Layout.setEnabled(True)

    def mirrorCrvShape(self):
        crv_shape_list = set()
        sel_list = pm.ls(sl=1,ni=1)
        for sel in sel_list:
            if type(sel) == nt.NurbsCurve:
                crv_shape_list.add(sel)
            elif hasattr(sel,"getShape") and type(sel.getShape()) == nt.NurbsCurve:
                crv_shape_list.add(sel.getShape())

        for sel in pm.ls(sl=1):
            if type(sel) == pm.general.NurbsCurveCV or type(sel) == pm.general.NurbsCurveEP:
                crv_shape_list.add(sel.node())

        pm.undoInfo(ock=1)
        for shape in crv_shape_list:
            crv = shape.getParent()
         
            if crv in self.L_matches:
                origin = self.L_matches[crv]
            elif crv in self.L_matches.values():
                origin = self.R_matches[crv]
            else:
                pm.warning(u"%s 曲线没有找到匹配"%crv)
                pm.headsUpMessage(u"%s 曲线没有找到匹配"%crv)
                continue
            
            mirror_crv = pm.duplicate(crv,rr=1,po=1)[0]
            mirror_crv_shape = pm.circle(ch=0)[0]

            for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
                attr = pm.Attribute("%s.%s"%(mirror_crv,attr))
                attr.setKeyable(True)
                attr.setLocked(False)

            pm.parent(mirror_crv_shape.getShape(),mirror_crv,r=1,s=1)
            pm.delete(mirror_crv_shape)

            crv.worldSpace[0].connect(mirror_crv.create,f=1)
            crv.worldSpace[0].disconnect(mirror_crv.create)

            pm.parent(mirror_crv,w=1)
            # NOTE 移动轴心到原点
            x,y,z = -crv.getTranslation(space="world")
            pm.move(x,y,z,mirror_crv.scalePivot,mirror_crv.rotatePivot,r=1)
            pm.makeIdentity(a=1,t=1,r=1,s=1,n=0,pn=1)
            # NOTE 镜像
            pm.xform(scale=[1,1,-1])
            pm.makeIdentity(a=1,t=1,r=1,s=1,n=0,pn=1)
            # NOTE 抵消组位移
            matrix = origin.worldMatrix.get().inverse()
            pm.xform(mirror_crv,m=matrix)
            pm.makeIdentity(a=1,t=1,r=1,s=1,n=0,pn=1)
            
            # NOTE 设置颜色
            shape = mirror_crv.getShape()
            origin_shape = origin.getShape()
            if origin_shape.overrideEnabled.get():
                shape.overrideEnabled.set(1)
                if origin_shape.overrideRGBColors.get():
                    color = origin_shape.overrideColorRGB.get()
                    shape.overrideColorRGB.set(color)
                else:
                    color = origin_shape.overrideColor.get()
                    shape.overrideColor.set(color)
                    
            pm.parent(shape,origin,r=1,s=1)
            pm.delete(mirror_crv)
            pm.delete(origin_shape)

        pm.select(sel_list)
        pm.undoInfo(cck=1)
                    
    def mayaShow(self,name="MF_CtrlMirrorTool"):
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
