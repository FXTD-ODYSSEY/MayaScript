# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-04 08:38:11'

"""
camera shaking control
"""

import os
import sys
from itertools import product

from maya import mel
from maya import OpenMayaUI
import pymel.core as pm

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets
from Qt.QtCompat import loadUi
from Qt.QtCompat import wrapInstance

import QtLib
reload(QtLib)
import channelBoxPlus
reload(channelBoxPlus)
from channelBoxPlus import mayaToQT,SearchWidget
from QtLib import IMouseClickSignal,replaceWidget,ICompleterComboBox

DIR = os.path.dirname(__file__)

class CamShakerWidget(QtWidgets.QWidget):

    exclude_list = ['front','top','side','persp']
    def __init__(self,parent=None):
        super(CamShakerWidget, self).__init__(parent)
        loadUi(os.path.join(DIR,"cam.ui"),self)
        self.setMaximumSize(16777215,100)
        
        self.Cam_Combo = replaceWidget(self.Cam_Combo,ICompleterComboBox())

        # NOTE 添加更新
        self.updateCameraList()
        signal = IMouseClickSignal(self.Cam_Combo)
        signal.LClicked.connect(self.updateCameraList)

        if self.Cam_Combo.count():
            self.Cam_Combo.setCurrentIndex(0)


        self.Cam_BTN.clicked.connect(self.getSelectedCamera)
        
        self.Generate_BTN = QtWidgets.QPushButton(u"生成相机约束")
        self.layout().addWidget(self.Generate_BTN)
        self.Generate_BTN.clicked.connect(self.generateCamRig)

    def generateCamRig(self):
        idx = self.Cam_Combo.currentIndex()
        cam = self.Cam_Combo.itemText(idx)

        self.Cam_Combo.setCurrentText(cam)
        if not pm.objExists(cam):
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("生成确认")
            msgBox.setText("当前摄像机不存在\n你确定要生成抖动节点吗？")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)

            ret = msgBox.exec_()
            if ret == QtWidgets.QMessageBox.Cancel:
                return
            else:
                cam = None
        else:
            cam = pm.PyNode(cam)
            for attr,axis in product(('t','r'),('x','y','z')):
                attr = getattr(cam,attr+axis)
                if attr.isConnected() or attr.isLocked():
                    msg = u"摄像机属性存在锁定和被连接情况\n无法连接"
                    QtWidgets.QMessageBox.warning(self,u"警告",msg)
                    return
            
        try:
            self.createCamRig(cam)
        except:
            if self.CAM_CTRL:
                pm.delete(self.CAM_CTRL)
            import traceback
            QtWidgets.QMessageBox.critical(self,u"错误",traceback.format_exc())
            
    def createCamRig(self,cam=None):

        # NOTE 创建 Cam_Shaker_GRP 大组
        pm.select(cl=1)
        shaker_grp = "Cam_Shaker_GRP"
        if not pm.objExists(shaker_grp):
            shaker_grp = pm.group(n="Cam_Shaker_GRP",w=1) 

        # NOTE 创建 Rig locator ----------------------------------------------------------------
        CAM_LOC = pm.spaceLocator(n="CAM_LOC_#")
        ZROT_ROLL = pm.group(n="ZROT_ROLL_#")
        XROT_TILT = pm.group(n="XROT_TILT_#")
        YROT_PAN = pm.group(n="YROT_PAN_#")
        SHAKER = pm.group(n="SHAKER_#")
        XYX_TRANS = pm.group(n="XYX_TRANS_#")
        self.CAM_CTRL = pm.group(n="%s_CAM_CTRL" % cam)
        
        self.CAM_CTRL.setParent(shaker_grp)
        # SHAKER.setParent(CAM_CTRL)
        # XYX_TRANS.setParent(SHAKER)
        # YROT_PAN.setParent(XYX_TRANS)
        # XROT_TILT.setParent(YROT_PAN)
        # ZROT_ROLL.setParent(XROT_TILT)
        # CAM_LOC.setParent(ZROT_ROLL)

        # NOTE 添加相关的属性 ----------------------------------------------------------------

        self.CAM_CTRL.addAttr("locator_ScaleX",attributeType="double",defaultValue=3,keyable=1)
        self.CAM_CTRL.addAttr("locator_ScaleY",attributeType="double",defaultValue=3,keyable=1)
        self.CAM_CTRL.addAttr("locator_ScaleZ",attributeType="double",defaultValue=3,keyable=1)

        self.CAM_CTRL.addAttr("transform",attributeType="enum",en="menu")
        self.CAM_CTRL.transform.set(cb=1,l=1)

        self.CAM_CTRL.addAttr("trans_Cam_TransX",attributeType="double",defaultValue=0,keyable=1)
        self.CAM_CTRL.addAttr("trans_Cam_TransY",attributeType="double",defaultValue=0,keyable=1)
        self.CAM_CTRL.addAttr("trans_Cam_TransZ",attributeType="double",defaultValue=0,keyable=1)

        self.CAM_CTRL.addAttr("trans_XROT_TILT",attributeType="double",defaultValue=0,keyable=1)
        self.CAM_CTRL.addAttr("trans_YROT_PAN",attributeType="double",defaultValue=0,keyable=1)
        self.CAM_CTRL.addAttr("trans_ZROT_ROLL",attributeType="double",defaultValue=0,keyable=1)

        self.CAM_CTRL.addAttr("trans_scaleXYZ",attributeType="double",defaultValue=3,keyable=1)
        self.CAM_CTRL.addAttr("trans_Focal_Length",attributeType="double",defaultValue=35,min=2.5,keyable=1)

        self.CAM_CTRL.addAttr("weight",attributeType="enum",en="menu")
        self.CAM_CTRL.weight.set(cb=1,l=1)

        self.CAM_CTRL.addAttr("weight_shk_tx",attributeType="double",defaultValue=0,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("weight_shk_ty",attributeType="double",defaultValue=0,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("weight_shk_tz",attributeType="double",defaultValue=0,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("weight_shk_rx",attributeType="double",defaultValue=0,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("weight_shk_ry",attributeType="double",defaultValue=0,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("weight_shk_rz",attributeType="double",defaultValue=0,min=0,max=1,keyable=1)

        self.CAM_CTRL.addAttr("noise_weight",attributeType="enum",en="menu")
        self.CAM_CTRL.noise_weight.set(cb=1,l=1)

        self.CAM_CTRL.addAttr("noise_shk_tx",attributeType="double",defaultValue=1,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("noise_shk_ty",attributeType="double",defaultValue=1,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("noise_shk_tz",attributeType="double",defaultValue=1,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("noise_shk_rx",attributeType="double",defaultValue=1,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("noise_shk_ry",attributeType="double",defaultValue=1,min=0,max=1,keyable=1)
        self.CAM_CTRL.addAttr("noise_shk_rz",attributeType="double",defaultValue=1,min=0,max=1,keyable=1)

        self.CAM_CTRL.addAttr("shakingAttr",attributeType="enum",en="menu")
        self.CAM_CTRL.shakingAttr.set(cb=1,l=1)

        self.CAM_CTRL.addAttr("attr_tx_Frequency",attributeType="double",defaultValue=20,keyable=1)
        self.CAM_CTRL.addAttr("attr_tx_Seed",attributeType="double",defaultValue=1,keyable=1)
        self.CAM_CTRL.addAttr("attr_ty_Frequency",attributeType="double",defaultValue=20,keyable=1)
        self.CAM_CTRL.addAttr("attr_ty_Seed",attributeType="double",defaultValue=1,keyable=1)
        self.CAM_CTRL.addAttr("attr_tz_Frequency",attributeType="double",defaultValue=20,keyable=1)
        self.CAM_CTRL.addAttr("attr_tz_Seed",attributeType="double",defaultValue=1,keyable=1)

        self.CAM_CTRL.addAttr("attr_rx_Frequency",attributeType="double",defaultValue=20,keyable=1)
        self.CAM_CTRL.addAttr("attr_rx_Seed",attributeType="double",defaultValue=1,keyable=1)
        self.CAM_CTRL.addAttr("attr_ry_Frequency",attributeType="double",defaultValue=20,keyable=1)
        self.CAM_CTRL.addAttr("attr_ry_Seed",attributeType="double",defaultValue=1,keyable=1)
        self.CAM_CTRL.addAttr("attr_rz_Frequency",attributeType="double",defaultValue=20,keyable=1)
        self.CAM_CTRL.addAttr("attr_rz_Seed",attributeType="double",defaultValue=1,keyable=1)

        # NOTE 添加表达式 ----------------------------------------------------------------
        exp = ''
        for attr,axis in product(('t','r'),('x','y','z')):
            attr = "%s%s" % (attr,axis)
            # exp += "{SHAKER}.{attr} = {CAM_CTRL}.weight_shk_{attr} * (0.282*(1-{CAM_CTRL}.noise_shk_{attr}) + ({CAM_CTRL}.noise_shk_{attr} * noise((frame + {CAM_CTRL}.attr_{attr}_Seed)/{CAM_CTRL}.attr_{attr}_Frequency)));\n".format(SHAKER=SHAKER,attr=attr,CAM_CTRL=self.CAM_CTRL)
            exp += "{SHAKER}.{attr} = {CAM_CTRL}.weight_shk_{attr} * (({CAM_CTRL}.noise_shk_{attr} * noise((frame + {CAM_CTRL}.attr_{attr}_Seed)/{CAM_CTRL}.attr_{attr}_Frequency)));\n".format(SHAKER=SHAKER,attr=attr,CAM_CTRL=self.CAM_CTRL)
        
        pm.expression(n="%s_exp"%self.CAM_CTRL , s=exp,o=str(SHAKER),ae=1,uc="all")

        # NOTE 连接摄像机 ----------------------------------------------------------------
        if cam:
            # NOTE 匹配当前摄像机位置
            pm.delete(pm.parentConstraint(cam,CAM_LOC,mo=0))
            pm.parentConstraint(CAM_LOC,cam)
            cam_shape = cam.getShape()
            self.CAM_CTRL.trans_scaleXYZ.connect(cam_shape.locatorScale)
            self.CAM_CTRL.trans_Focal_Length.connect(cam_shape.focalLength)

        # NOTE 连接属性 ----------------------------------------------------------------
        
        loc_shape = CAM_LOC.getShape()
        self.CAM_CTRL.locator_ScaleX.connect(loc_shape.localScaleX)
        self.CAM_CTRL.locator_ScaleY.connect(loc_shape.localScaleY)
        self.CAM_CTRL.locator_ScaleZ.connect(loc_shape.localScaleZ)

        self.CAM_CTRL.trans_Cam_TransX.connect(XYX_TRANS.tx)
        self.CAM_CTRL.trans_Cam_TransY.connect(XYX_TRANS.ty)
        self.CAM_CTRL.trans_Cam_TransZ.connect(XYX_TRANS.tz)

        self.CAM_CTRL.trans_XROT_TILT.connect(XROT_TILT.rx)
        self.CAM_CTRL.trans_YROT_PAN.connect(YROT_PAN.rx)
        self.CAM_CTRL.trans_ZROT_ROLL.connect(ZROT_ROLL.rz)

        # NOTE 锁定隐藏属性 ----------------------------------------------------------------
        # self.CAM_CTRL.tx.set(l=1,k=0,cb=0)
        # self.CAM_CTRL.ty.set(l=1,k=0,cb=0)
        # self.CAM_CTRL.tz.set(l=1,k=0,cb=0)
        # self.CAM_CTRL.rx.set(l=1,k=0,cb=0)
        # self.CAM_CTRL.ry.set(l=1,k=0,cb=0)
        # self.CAM_CTRL.rz.set(l=1,k=0,cb=0)
        # self.CAM_CTRL.sx.set(l=1,k=0,cb=0)
        # self.CAM_CTRL.sy.set(l=1,k=0,cb=0)
        # self.CAM_CTRL.sz.set(l=1,k=0,cb=0)
        # self.CAM_CTRL.v.set(l=1,k=0,cb=0)

        XYX_TRANS.rx.set(l=1,k=0,cb=0)
        XYX_TRANS.ry.set(l=1,k=0,cb=0)
        XYX_TRANS.rz.set(l=1,k=0,cb=0)
        XYX_TRANS.sx.set(l=1,k=0,cb=0)
        XYX_TRANS.sy.set(l=1,k=0,cb=0)
        XYX_TRANS.sz.set(l=1,k=0,cb=0)

        YROT_PAN.tx.set(l=1,k=0,cb=0)
        YROT_PAN.ty.set(l=1,k=0,cb=0)
        YROT_PAN.tz.set(l=1,k=0,cb=0)
        YROT_PAN.rx.set(l=1,k=0,cb=0)
        YROT_PAN.rz.set(l=1,k=0,cb=0)
        YROT_PAN.sx.set(l=1,k=0,cb=0)
        YROT_PAN.sy.set(l=1,k=0,cb=0)
        YROT_PAN.sz.set(l=1,k=0,cb=0)

        XROT_TILT.tx.set(l=1,k=0,cb=0)
        XROT_TILT.ty.set(l=1,k=0,cb=0)
        XROT_TILT.tz.set(l=1,k=0,cb=0)
        XROT_TILT.ry.set(l=1,k=0,cb=0)
        XROT_TILT.rz.set(l=1,k=0,cb=0)
        XROT_TILT.sx.set(l=1,k=0,cb=0)
        XROT_TILT.sy.set(l=1,k=0,cb=0)
        XROT_TILT.sz.set(l=1,k=0,cb=0)

        ZROT_ROLL.tx.set(l=1,k=0,cb=0)
        ZROT_ROLL.ty.set(l=1,k=0,cb=0)
        ZROT_ROLL.tz.set(l=1,k=0,cb=0)
        ZROT_ROLL.ry.set(l=1,k=0,cb=0)
        ZROT_ROLL.rx.set(l=1,k=0,cb=0)
        ZROT_ROLL.sx.set(l=1,k=0,cb=0)
        ZROT_ROLL.sy.set(l=1,k=0,cb=0)
        ZROT_ROLL.sz.set(l=1,k=0,cb=0)

        self.CAM_CTRL = None

    def getSelectedCamera(self):
        sel = pm.ls(sl=1)
        
        # NOTE 当前的 modelEditor
        cur_mp = None
        for mp in pm.getPanel(type="modelPanel"):
            if pm.modelEditor(mp, q=1, av=1):
                cur_mp = mp
                break

        # NOTE 获取摄像机节点
        pm.pickWalk(d="down")
        cam_list = pm.ls(sl=1,ca=1)
        
        # NOTE 获取选择的摄像机 没有 则获取当前视窗的摄像机
        cam = cam_list[0].getParent() if cam_list else pm.modelEditor(cur_mp,q=1,cam=1)
        
        for i in range(self.Cam_Combo.count()):
            text = self.Cam_Combo.itemText(i)
            if text == str(cam):
                self.Cam_Combo.setCurrentIndex(i)
                break

        pm.select(sel)

    def updateCameraList(self):
        text = self.Cam_Combo.currentText()

        self.Cam_Combo.clear()
        for i,cam in enumerate(pm.ls(ca=1)):
            cam = cam.getParent()
            if str(cam) in self.exclude_list:continue
            self.Cam_Combo.addItem(str(cam))
            
        self.Cam_Combo.setCurrentText(text)


class ChannelBoxWidget(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(ChannelBoxWidget, self).__init__(parent)
        self.CamShakerWidget = parent
        temp_win = pm.window()
        pm.columnLayout()
        channelBox = pm.channelBox('CamShaker')
        self.display_label = QtWidgets.QLabel()

        search_layout = QtWidgets.QHBoxLayout()
        self.CHANNELBOX_PLUS = SearchWidget(channelBox,parent,self,threshold = 0.75)

        self.select_btn = QtWidgets.QPushButton(u"选择当前抖动节点")
        self.select_btn.clicked.connect(self.selectCameraRig)

        self.filter_label = QtWidgets.QLabel(u"快速过滤属性")
        self.filter = ICompleterComboBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.filter.setSizePolicy(sizePolicy)

        self.filter_list = ('weight','noise','attr','tx','ty','tz','rx','ry','rz','locator','trans')
        for filter_name in self.filter_list:
            self.filter.addItem(filter_name)
        
        self.filter.currentIndexChanged.connect(self.changeFilter)
        
        signal = IMouseClickSignal(self.filter_label)
        signal.LClicked.connect(lambda:self.changeFilter(self.filter.currentIndex()))

        search_layout.addWidget(self.select_btn)
        search_layout.addWidget(self.filter_label)
        search_layout.addWidget(self.filter)
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        layout.addLayout(search_layout)
        layout.addWidget(self.CHANNELBOX_PLUS)
        layout.addWidget(mayaToQT(channelBox))
        layout.addWidget(self.display_label)
        
        pm.deleteUI(temp_win)

        # NOTE 设置大小扩展
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)

    def changeFilter(self,index):
        text = self.filter.itemText(index)
        self.CHANNELBOX_PLUS.edit.setText(text)
    
    def selectCameraRig(self):
        idx = self.CamShakerWidget.Cam_Combo.currentIndex()
        cam = self.CamShakerWidget.Cam_Combo.itemText(idx)

        CAM_CTRL = "%s_CAM_CTRL" % cam
        if pm.objExists(CAM_CTRL):
            pm.select(CAM_CTRL)

class CamShakerWin(QtWidgets.QWidget):
    
    def __init__(self,parent=None):
        super(CamShakerWin, self).__init__(parent)
        self.setWindowTitle(u"镜头抖动生成工具")

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.cam_widget = CamShakerWidget()
        self.channelBox = ChannelBoxWidget(self.cam_widget)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitter.addWidget(self.cam_widget)
        self.splitter.addWidget(self.channelBox)

        layout.addWidget(self.splitter)

    def mayaShow(self,name="MF_CamShaker"):
        # NOTE 如果变量存在 就检查窗口多开
        if pm.versions.current() > pm.versions.v2016:
            if pm.window(name,q=1,ex=1):
                pm.deleteUI(name)
            window = pm.window(name,title=self.windowTitle())
        else:
            if pm.workspaceControl(name,q=1,ex=1):
                pm.deleteUI(name)
            window = pm.workspaceControl(name,label=self.windowTitle())
        
        pm.showWindow(window)

        # NOTE 将Maya窗口转换成 Qt 组件
        self.ptr = mayaToQT(window)
        self.ptr.setLayout(QtWidgets.QVBoxLayout())
        self.ptr.layout().setContentsMargins(0,0,0,0)
        self.ptr.layout().addWidget(self)
        self.ptr.resize(300,300)
        self.ptr.destroyed.connect(lambda:self.channelBox.CHANNELBOX_PLUS.removeCallback())
        # self.ptr.setMaximumHeight(300)
        return self.ptr
        
# import sys
# MODULE = r"F:\MayaTecent\MayaScript\anim\camShaker"
# if MODULE not in sys.path:
#     sys.path.append(MODULE)

# try:
#     import camShaker
#     reload (camShaker)
#     win = camShaker.CamShakerWin()
#     win.mayaShow()
# except:
#     import traceback
#     traceback.print_exc()