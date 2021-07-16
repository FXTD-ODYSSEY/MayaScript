# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-20 16:52:15'

"""
挤出轮廓边
"""

import os
from functools import wraps

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from Qt.QtCompat import wrapInstance
from Qt.QtCompat import loadUi

import maya.api.OpenMaya as om
from maya import OpenMayaUI
import pymel.core as pm
from maya import mel


class outlineExtrude_UI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(442, 234)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Gen_Profile_BTN = QtWidgets.QPushButton(Form)
        self.Gen_Profile_BTN.setObjectName("Gen_Profile_BTN")
        self.verticalLayout.addWidget(self.Gen_Profile_BTN)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Profile_LE = QtWidgets.QLineEdit(Form)
        self.Profile_LE.setObjectName("Profile_LE")
        self.horizontalLayout.addWidget(self.Profile_LE)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Adjust_Layout = QtWidgets.QWidget(Form)
        self.Adjust_Layout.setObjectName("Adjust_Layout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Adjust_Layout)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.Adjust_Layout)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.U_SP = QtWidgets.QSpinBox(self.Adjust_Layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.U_SP.sizePolicy().hasHeightForWidth())
        self.U_SP.setSizePolicy(sizePolicy)
        self.U_SP.setMinimum(1)
        self.U_SP.setObjectName("U_SP")
        self.horizontalLayout_5.addWidget(self.U_SP)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.Adjust_Layout)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.V_SP = QtWidgets.QSpinBox(self.Adjust_Layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.V_SP.sizePolicy().hasHeightForWidth())
        self.V_SP.setSizePolicy(sizePolicy)
        self.V_SP.setMinimum(1)
        self.V_SP.setObjectName("V_SP")
        self.horizontalLayout_4.addWidget(self.V_SP)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.Adjust_Layout)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.Thickness_SP = QtWidgets.QDoubleSpinBox(self.Adjust_Layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Thickness_SP.sizePolicy().hasHeightForWidth())
        self.Thickness_SP.setSizePolicy(sizePolicy)
        self.Thickness_SP.setMinimum(-999.0)
        self.Thickness_SP.setMaximum(999.0)
        self.Thickness_SP.setSingleStep(0.01)
        self.Thickness_SP.setProperty("value", 1.0)
        self.Thickness_SP.setObjectName("Thickness_SP")
        self.horizontalLayout_3.addWidget(self.Thickness_SP)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.Complete_BTN = QtWidgets.QPushButton(self.Adjust_Layout)
        self.Complete_BTN.setObjectName("Complete_BTN")
        self.verticalLayout_2.addWidget(self.Complete_BTN)
        self.verticalLayout.addWidget(self.Adjust_Layout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(u"挤出轮廓")
        self.Gen_Profile_BTN.setText(u"选择模型 - 生成轮廓")
        self.label.setText(u"轮廓组")
        self.label_5.setText(u"U向分段")
        self.label_4.setText(u"V向分段")
        self.label_3.setText(u"厚度调整")
        self.Complete_BTN.setText(u"完成调整")

def errorHandler(func):
    @wraps(func)
    def wrapper(self,*args,**kwargs):
        try:
            func(self,*args,**kwargs)
        except:
            import traceback
            traceback.print_exc()
            self.resetValue()
            pm.warning(u"错误！请重新生成轮廓")
            pm.headsUpMessage(u"错误！请重新生成轮廓")
    
    return wrapper

class outlineExtrude(QtWidgets.QWidget,outlineExtrude_UI):

    def __init__(self):
        super(outlineExtrude,self).__init__()
        # DIR = os.path.dirname(__file__)
        # ui_file = os.path.join(DIR,"outline.ui")
        # loadUi(ui_file,self)

        self.setupUi(self)
        self.Adjust_Layout.setEnabled(False)

        self.extrude_node = None
        self.origin_edge_list = None

        self.Gen_Profile_BTN.clicked.connect(self.generateProfile)
        self.U_SP.valueChanged.connect(self.UAdjust)
        self.V_SP.valueChanged.connect(self.VAdjust)
        self.Thickness_SP.valueChanged.connect(self.thicknessAdjust)
        self.Complete_BTN.clicked.connect(self.compeleteProfile)

        mel.eval('source "assignPfxToon.mel";')

    def resetValue(self):
        self.Thickness_SP.blockSignals(True)
        self.Thickness_SP.setValue(1)
        self.Thickness_SP.blockSignals(False)
        self.Thickness_SP.blockSignals(True)
        self.U_SP.setValue(1)
        self.Thickness_SP.blockSignals(False)
        self.Thickness_SP.blockSignals(True)
        self.V_SP.setValue(1)
        self.Thickness_SP.blockSignals(False)
        if pm.objExists(self.profile_grp):
            pm.delete(self.profile_grp)
        self.Profile_LE.setText("")
        self.Adjust_Layout.setEnabled(False)

    def inflateCurveOnMeshCVs(self,crv,mesh,scale=1):
        sel_list = om.MSelectionList()
        sel_list.add(str(crv))
        sel_list.add(str(mesh))

        DagPath,_ = sel_list.getComponent(0)

        Curve = om.MFnNurbsCurve(DagPath)
        CurveCVs = Curve.cvPositions(om.MSpace.kWorld)
        newCurveCVs = om.MPointArray()

        DagPath,_ = sel_list.getComponent(1)
        Mesh = om.MFnMesh(DagPath)

        for i in range(len(CurveCVs)):
            cv = CurveCVs[i]

            normal,_ = Mesh.getClosestNormal(cv)
            
            x = cv.x + normal.x * scale
            y = cv.y + normal.y * scale
            z = cv.z + normal.z * scale
            newCurveCV = om.MPoint(x,y,z)
        
            newCurveCVs.append(newCurveCV)

        return newCurveCVs

    def getMFnNurbsCurve(self,crv):
        sel_list = om.MSelectionList()
        sel_list.add(str(crv))
        DagPath,_ = sel_list.getComponent(0)
        return om.MFnNurbsCurve(DagPath)

    def inflateCurveOnMesh(self,crv,mesh,scale=1):
        newCurveCVs = self.inflateCurveOnMeshCVs(crv,mesh,scale=scale)

        newCrv = pm.duplicate(crv)[0]
        newCurve = self.getMFnNurbsCurve(newCrv)
        newCurve.setCVPositions(newCurveCVs)
        newCurve.updateCurve()
        return newCrv
        
    def getActivePanel(self):
        cur_mp = None
        for mp in pm.getPanel(type="modelPanel"):
            if pm.modelEditor(mp, q=1, av=1):
                cur_mp = mp
                break
        return cur_mp

    def getActiveCamera(self):
        panel = self.getActivePanel()
        if panel:
            return pm.PyNode(pm.modelPanel(panel,q=1,cam=1))
            

    def generateProfileCurve(self,profile_node):
        count = profile_node.outMainCurveCount.get()
        crv_list = []
        for i in range(count):
            attr = profile_node.outMainCurves[i]
            if pm.connectionInfo(attr,isSource=1):
                continue
            crv = pm.createNode("nurbsCurve")
            pm.connectAttr(attr,"%s.create"%crv,f=1)
            attr.disconnect(crv.create)
            crv_list.append(crv.getParent())
        return crv_list

    @errorHandler
    def generateProfile(self):

        n_polyType = pm.nurbsToPolygonsPref(q=1,polyType = 1)
        n_format   = pm.nurbsToPolygonsPref(q=1,format   = 1)
        n_uType    = pm.nurbsToPolygonsPref(q=1,uType    = 1)
        n_uNumber  = pm.nurbsToPolygonsPref(q=1,uNumber  = 1)
        n_vType    = pm.nurbsToPolygonsPref(q=1,vType    = 1)
        n_vNumber  = pm.nurbsToPolygonsPref(q=1,vNumber  = 1)

        

        self.sel_list = [sel for sel in pm.ls(sl=1,ni=1) if hasattr(sel,"getShape") and type(sel.getShape()) == pm.nodetypes.Mesh]
        if not self.sel_list: 
            pm.warning(u"请选择 Mesh 模型")
            pm.headsUpMessage(u"请选择 Mesh 模型")
            return
            
        cam = self.getActiveCamera()
        if not cam: 
            pm.warning(u"请打开视窗 获取当前激活的摄像机")
            pm.headsUpMessage(u"请打开视窗 获取当前激活的摄像机")
            return

        pm.nurbsToPolygonsPref(polyType = 1)
        pm.nurbsToPolygonsPref(format   = 2)
        pm.nurbsToPolygonsPref(uType    = 3)
        pm.nurbsToPolygonsPref(uNumber  = 1)
        pm.nurbsToPolygonsPref(vType    = 3)
        pm.nurbsToPolygonsPref(vNumber  = 1)

        self.Adjust_Layout.setEnabled(True)

        pm.undoInfo(ock=1)
        self.crv_dict = {}
        for sel in self.sel_list:
            # NOTE 通过 Toon 创建轮廓
            mel.eval('assignPfxToon "" 0;')
            # NOTE 获取 Toon 节点
            profile_node = pm.ls(sl=1)[0]
            # NOTE 链接当前摄像机 外轮廓
            cam.t.connect(profile_node.cameraPoint,f=1)

            # NOTE 生成描边曲线
            base_crv_list = self.generateProfileCurve(profile_node)

            mesh_list = []
            inflate_crv_list = []
            nurbsTessellate_list = []
            # NOTE 曲线放样成描边模型
            for base in base_crv_list:
                pm.rebuildCurve(base,ch=0,rpo=1,rt=0,end=1,kr=1,kcp=0,kep=1,kt=0,s=0,d=3,tol=0.01)
                inflate = self.inflateCurveOnMesh(base,sel,scale=0.5)
                inflate_crv_list.append(inflate)

                mesh = pm.loft(base,inflate,ch=1,u=1,c=0,ar=1,d=3,ss=1,rn=1,po=1,rsn=1)[0]
                node = mesh.history(type="nurbsTessellate")
                if node:
                    nurbsTessellate_list.extend(node)

                mesh_list.append(mesh)
            
            self.crv_dict[sel] = {
                "base":base_crv_list,
                "inflate":inflate_crv_list,
                "mesh":mesh_list,
                "nurbsTessellate":nurbsTessellate_list,
            }
            

            base_grp = pm.group(base_crv_list,n="base_grp")
            inflate_grp = pm.group(inflate_crv_list,n="inflate_grp")
            # mesh_grp = pm.group(mesh_list,n="inflate_mesh_grp")

            self.profile_grp = pm.group(base_grp,inflate_grp,mesh_list,n="profile_grp")

            self.Profile_LE.setText(str(self.profile_grp))

            # if len(mesh_list) > 2:
            #     pm.polyUnite(mesh_list,n="%s_profile"%sel,ch=0)
            # pm.delete(base_grp,inflate_grp)

            pm.delete(profile_node.getParent())

        pm.undoInfo(cck=1)

        pm.nurbsToPolygonsPref(polyType = n_polyType)
        pm.nurbsToPolygonsPref(format   = n_format  )
        pm.nurbsToPolygonsPref(uType    = n_uType   )
        pm.nurbsToPolygonsPref(uNumber  = n_uNumber )
        pm.nurbsToPolygonsPref(vType    = n_vType   )
        pm.nurbsToPolygonsPref(vNumber  = n_vNumber )

    @errorHandler
    def thicknessAdjust(self,value):
        for sel in self.sel_list:
            base_crv_list = self.crv_dict[sel]["base"]
            inflate_crv_list = self.crv_dict[sel]["inflate"]
            for base,inflate in zip(base_crv_list,inflate_crv_list):
                newCurve = self.getMFnNurbsCurve(inflate)
                newCurveCVs = self.inflateCurveOnMeshCVs(base,sel,scale=value)
                newCurve.setCVPositions(newCurveCVs)
                newCurve.updateCurve()

    @errorHandler
    def UAdjust(self,value):
        for sel in self.sel_list:
            nurbsTessellate_list = self.crv_dict[sel]["nurbsTessellate"]
            for tessellate in nurbsTessellate_list:
                tessellate.uNumber.set(value)

    @errorHandler
    def VAdjust(self,value):
        for sel in self.sel_list:
            nurbsTessellate_list = self.crv_dict[sel]["nurbsTessellate"]
            for tessellate in nurbsTessellate_list:
                tessellate.vNumber.set(value)

    @errorHandler
    def compeleteProfile(self):
        for sel in self.sel_list:
            name = "%s_profile"%sel
            mesh_list = self.crv_dict[sel]["mesh"]
            if len(mesh_list) > 2:
                mesh = pm.polyUnite(mesh_list,n=name,ch=0)
            else:
                mesh = mesh_list[0]
                mesh.rename(name)

            # pm.delete(mesh,ch=1)
            pm.parent(mesh,w=1)

        self.resetValue()

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
        # # NOTE 脱离要删除的窗口
        # window = OpenMayaUI.MQtUtil.mainWindow()
        # window = wrapInstance(long(window), QtWidgets.QMainWindow)
        self.setParent(None)
    
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