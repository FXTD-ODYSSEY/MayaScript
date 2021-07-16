# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-01-03 10:07:09'

"""
overlapper 插件改良
"""
import os
import sys

from maya import cmds
from maya import mel
from maya import OpenMayaUI

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from Qt.QtCompat import loadUi
from Qt.QtCompat import wrapInstance

from timeit import timeit


class Overlapper_UI(QtWidgets.QWidget):

    def __init__(self):
        super(Overlapper_UI,self).__init__()

        DIR = os.path.dirname(__file__)
        ui_path = os.path.join(DIR,"ui","overlapper.ui")
        loadUi(ui_path,self)

        self.Overlap_BTN.clicked.connect(self.overlapPrepare)
        
    def overlapPrepare(self):
        Hierarchy = self.Hierarchy_CB.isChecked()
        if Hierarchy:
            sel_list = [cmds.listRelatives(crv,parent=1)[0] for crv in cmds.ls(sl=1,dag=1,type="nurbsCurve")]
            cmds.select(sel_list)
        self.overlap()

    def overlap(self):
        NotUseFirstCtrl = self.First_CB.isChecked()
        CycleCheckBox = self.Cycle_CB.isChecked()
        TRANSLATEmode = self.Translate_CB.isChecked()
        OnLayerSwitch = self.Bake_CB.isChecked()

        WindSwitch = self.Wind_CB.isChecked()
        windScaleValue = self.Wind_Scale_SP.value()
        windSpeedValue = self.Wind_Speed_SP.value()
        
        overlapIntensity = self.Scale_SP.value()
        timeShift = self.Softness_SP.value()
        timeStart = cmds.playbackOptions(q=1,min=1)
        timeEnd = cmds.playbackOptions(q=1,max=1)

        controller_list = cmds.ls(sl=1)

        # NOTE 生成骨骼 | 调整轴向
        cmds.select(cl=1)
        jnt_list = []
        _jnt = None
        for controller in controller_list:
            pos = cmds.xform(controller,q=1,rp=1,ws=1) 
            jnt = cmds.joint(p=pos,rad=1,n="%s_OverlapJoint" % controller)
            if _jnt:
                cmds.joint(_jnt,e=1,zso=1,oj="xyz",sao="yup")
            jnt_list.append(jnt)
            _jnt = jnt
        else:
            last_jnt = cmds.duplicate(jnt,rr=1,n="%s_LastOrientJoint" % controller)[0]
            cmds.move(2,0,0,r=1,ls=1,wd=1)
            cmds.parent(last_jnt,jnt)
            jnt_list.append(last_jnt)
            cmds.joint(jnt,e=1,zso=1,oj="xyz",sao="yup")

            sumLenghtJoints = sum([cmds.getAttr("%s.tx" % jnt) for jnt in jnt_list])
            averageLenghtJoints = (sumLenghtJoints - 2) / len(jnt_list)
            cmds.setAttr( last_jnt + ".tx",averageLenghtJoints)

        constraint_list = []
        for controller,jnt in zip(controller_list,jnt_list):
            constraint_list.extend(cmds.parentConstraint(controller,jnt,mo=1))
        
        # NOTE 烘焙骨骼跟随控制器的关键帧
        cmds.bakeResults(
            jnt_list,
            simulation = 1, # NOTE 开启模拟 解决卡顿问题
            t = (timeStart,timeEnd),
            sampleBy = 1, 
            oversamplingRate = 1, 
            disableImplicitControl = 1, 
            preserveOutsideKeys = 1, 
            sparseAnimCurveBake = 0, 
            removeBakedAttributeFromLayer = 0, 
            removeBakedAnimFromLayer = 0, 
            bakeOnOverrideLayer = 0, 
            minimizeRotation = 1, 
            at=['tx','ty','tz','rx','ry','rz']
        )

        cmds.delete(constraint_list)

        if CycleCheckBox:
            # NOTE 将骨骼关键帧复制多几份
            for i,jnt in enumerate(jnt_list):
                cmds.selectKey(
                    cmds.listConnections(jnt+".tx",type="animCurve"),
                    cmds.listConnections(jnt+".ty",type="animCurve"),
                    cmds.listConnections(jnt+".tz",type="animCurve"),
                    cmds.listConnections(jnt+".rx",type="animCurve"),
                    cmds.listConnections(jnt+".ry",type="animCurve"),
                    cmds.listConnections(jnt+".rz",type="animCurve"),
                    r=1,k=1,t=(timeStart,timeEnd))
                cmds.copyKey()
                cmds.pasteKey(time=(timeEnd,timeEnd),float=(timeEnd,timeEnd),option="insert",copies=2,connect=0,timeOffset=0,floatOffset=0,valueOffset=0)
            
            cycleLenghts = timeEnd - timeStart
            timeEnd = timeEnd + 2*cycleLenghts

        # NOTE 进行 overlap
        overlapIntensityMult = averageLenghtJoints/overlapIntensity*5
        timeShiftNeg = -timeShift
        timeShiftCurrent = 1+timeShift

        gc_list = []
        aim_data = {}
        for i,jnt in enumerate(jnt_list):

            offset_loc = cmds.spaceLocator(n="overlapOffsetLocator%s"%i)[0]
            cmds.delete(cmds.parentConstraint(jnt,offset_loc,w=1))

            cmds.move(overlapIntensityMult,0,0,r=1,os=1,ls=1)
            con = cmds.parentConstraint(jnt,offset_loc,mo=1)

            cmds.bakeResults(
                offset_loc,
                simulation = 0,
                t = (timeStart,timeEnd),
                sampleBy = 1, 
                disableImplicitControl = 1, 
                preserveOutsideKeys = 1, 
                minimizeRotation = 1, 
                at=['tx','ty','tz','rx','ry','rz']
            )

            cmds.delete(con)

            wind_loc = cmds.spaceLocator(n="overlapOffsetLocatorWind%s"%i)[0]
            gc_list.append(wind_loc)
            cmds.parent(wind_loc,offset_loc)
            cmds.makeIdentity(wind_loc,a=0,t=1,r=1,s=1,n=0,pn=1)
            
            animCurve_list = [
                (offset_loc+"_translateX"),
                (offset_loc+"_translateY"),
                (offset_loc+"_translateZ"),
                (offset_loc+"_rotateX"),
                (offset_loc+"_rotateY"),
                (offset_loc+"_rotateZ"),
            ]

            for animCurve in animCurve_list:
                cmds.keyframe(animCurve,e=1,iub=1,r=1,o="over",tc=timeShift)
                cmds.keyframe(animCurve,t=(timeShiftCurrent,timeShiftCurrent),option="over",relative=1,timeChange=timeShiftNeg)

            aim_loc = cmds.spaceLocator(n="overlapInLocator_aim_%s"%i)[0]

            aim_grp = cmds.group(aim_loc,n=aim_loc+"_grp")
            cmds.pointConstraint(jnt,aim_grp)
            aim_data[aim_loc] = aim_grp

            cmds.aimConstraint(wind_loc,aim_grp,aimVector=[1,0,0],upVector=[0,1,0],worldUpType="object",worldUpObject=wind_loc)
            cmds.orientConstraint(wind_loc,aim_loc,mo=1,skip=["y","z"],w=1)

            # NOTE 添加控制器 translate 坐标位移
            if TRANSLATEmode and i != len(jnt_list) - 1:
                IK_loc = cmds.spaceLocator(n="overlapOffsetIKLocator%s"%i)[0]
                cmds.pointConstraint(jnt,IK_loc)
                cmds.bakeResults(
                    IK_loc,
                    simulation = 0,
                    t = (timeStart,timeEnd),
                    sampleBy = 1, 
                    disableImplicitControl = 1, 
                    preserveOutsideKeys = 1, 
                    minimizeRotation = 1, 
                    at=['tx','ty','tz']
                )
                animCurve_list = [
                    (IK_loc+"_translateX"),
                    (IK_loc+"_translateY"),
                    (IK_loc+"_translateZ"),
                ]
                for animCurve in animCurve_list:
                    cmds.keyframe(animCurve,e=1,iub=1,r=1,o="over",tc=timeShift)
                    cmds.keyframe(animCurve,t=(timeShiftCurrent,timeShiftCurrent),option="over",relative=1,timeChange=timeShiftNeg)

                cmds.pointConstraint(IK_loc,aim_loc)
                gc_list.append(IK_loc)

            # NOTE 添加随机风向控制
            if WindSwitch :
                windMultiply = 0.07*overlapIntensityMult*windScaleValue
                speedMultiply = 20/windSpeedValue; 

                cmds.setKeyframe( wind_loc, attribute=['translateY','translateZ'], t=[timeStart,timeStart] )

                cmds.bakeResults(
                    wind_loc,
                    simulation = 0,
                    t = (timeStart,timeEnd+speedMultiply),
                    sampleBy = speedMultiply, 
                    oversamplingRate = 1, 
                    disableImplicitControl = 1, 
                    preserveOutsideKeys = 1, 
                    at = ['ty','tz']
                )

                for attr in cmds.listAttr(wind_loc,k=1):
                    animCurve = cmds.listConnections("%s.%s"%(wind_loc,attr),type="animCurve")
                    if not animCurve:
                        continue
                    for animCurveCurrent in animCurve:
                        for animCurveCurrentKeysTime in cmds.keyframe(animCurveCurrent,q=1,t=(timeStart,timeEnd),tc=1):
                            t = (animCurveCurrentKeysTime,animCurveCurrentKeysTime)
                            animCurveCurrentKeysTimeArray = cmds.keyframe(animCurveCurrent,q=1,time=t,vc=1)
                            RandomizerValue = random.random()*2 - 1
                            animCurveCurrentKeysValueArrayAddRandom = animCurveCurrentKeysTimeArray[0] + windMultiply*RandomizerValue
                            cmds.keyframe(animCurveCurrent,e=1,iub=1,r=1,o="over",vc=animCurveCurrentKeysValueArrayAddRandom,t=t)

                attr = (wind_loc+"_translateY")
                cmds.keyframe(attr,e=1,iub=1,r=1,o="over",tc=speedMultiply/2)
                t = (speedMultiply/2)+1
                cmds.selectKey(attr,add=1,k=1,t=(t,t))
                cmds.keyframe(attr,animation="keys",r=1,o="over",tc=speedMultiply/-2)

            cmds.bakeResults(
                aim_grp,aim_loc,
                simulation = 0,
                t = (timeStart,timeEnd),
                sampleBy = 1, 
                disableImplicitControl = 1, 
                preserveOutsideKeys = 1, 
                minimizeRotation = 1, 
                at=['tx','ty','tz','rx','ry','rz']
            )

            cmds.parentConstraint(aim_loc,jnt,mo=1)
            
            gc_list.append(offset_loc)
            gc_list.append(aim_grp)

        # NOTE 动画循环控制
        if CycleCheckBox:
            timeStart = cmds.playbackOptions(q=1,min=1)
            timeEnd = cmds.playbackOptions(q=1,max=1)
            cycleLenghts = timeEnd - timeStart
            # NOTE 将关键帧挪动回去两个时间范围
            for aim_loc,aim_grp in aim_data.items():
                cmds.keyframe(
                    cmds.listConnections(aim_loc+".tx",type="animCurve"),
                    cmds.listConnections(aim_loc+".ty",type="animCurve"),
                    cmds.listConnections(aim_loc+".tz",type="animCurve"),
                    cmds.listConnections(aim_loc+".rx",type="animCurve"),
                    cmds.listConnections(aim_loc+".ry",type="animCurve"),
                    cmds.listConnections(aim_loc+".rz",type="animCurve"),
                    cmds.listConnections(aim_grp+".tx",type="animCurve"),
                    cmds.listConnections(aim_grp+".ty",type="animCurve"),
                    cmds.listConnections(aim_grp+".tz",type="animCurve"),
                    cmds.listConnections(aim_grp+".rx",type="animCurve"),
                    cmds.listConnections(aim_grp+".ry",type="animCurve"),
                    cmds.listConnections(aim_grp+".rz",type="animCurve"),
                    e=1,iub=1,r=1,o="over",tc=cycleLenghts*-2)

        constraint_list = []
        for i,[controller,jnt] in enumerate(zip(controller_list,jnt_list)):
            if NotUseFirstCtrl and i == 0:
                continue
            if cmds.getAttr(controller+".tx",k=1) and not cmds.getAttr(controller+".tx",l=1) and \
               cmds.getAttr(controller+".ty",k=1) and not cmds.getAttr(controller+".ty",l=1) and \
               cmds.getAttr(controller+".tz",k=1) and not cmds.getAttr(controller+".tz",l=1):
                constraint_list.extend(cmds.pointConstraint(jnt,controller,mo=1))
            if cmds.getAttr(controller+".rx",k=1) and not cmds.getAttr(controller+".rx",l=1) and \
               cmds.getAttr(controller+".ry",k=1) and not cmds.getAttr(controller+".ry",l=1) and \
               cmds.getAttr(controller+".rz",k=1) and not cmds.getAttr(controller+".rz",l=1):
                constraint_list.extend(cmds.orientConstraint(jnt,controller,mo=1))
        
        if NotUseFirstCtrl:
            controller_list = controller_list[1:]

        # NOTE 输出到控制器上
        cmds.bakeResults(
            controller_list,
            simulation = 1, # NOTE 开启模拟 解决卡顿问题
            t = (timeStart,timeEnd),
            sampleBy = 1, 
            disableImplicitControl = 1, 
            bakeOnOverrideLayer = OnLayerSwitch,     
            preserveOutsideKeys = 1, 
            minimizeRotation = 1, 
            at=['tx','ty','tz','rx','ry','rz']
        )

        cmds.delete(constraint_list)
        cmds.delete(jnt_list)
        cmds.delete(gc_list)
    
    def mayaShow(self,name="overlapperEnhance_UI"):
        # NOTE 如果变量存在 就检查窗口多开
        if cmds.window(name,q=1,ex=1):
            cmds.deleteUI(name)
        window = cmds.window(name,title=self.windowTitle())
        cmds.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        self.ptr = self.mayaToQT(window)
        self.ptr.setLayout(QtWidgets.QVBoxLayout())
        self.ptr.layout().setContentsMargins(0,0,0,0)
        self.ptr.layout().addWidget(self)
        self.ptr.resize(300,300)
        self.ptr.setMaximumHeight(300)
        return self.ptr
        
    def mayaToQT( self,name ):
        # Maya -> QWidget
        ptr = OpenMayaUI.MQtUtil.findControl( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findLayout( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
        if ptr is not None: return wrapInstance( long( ptr ), QtWidgets.QWidget )

if __name__ == "__main__":
    # overlap()
    print timeit("overlap()","from __main__ import overlap",number=1)

# import sys
# MODULE = r"F:\MayaTecent\MayaScript\anim\overlapperEnhance"
# if MODULE not in sys.path:
#     sys.path.append(MODULE)

# import overlapper
# reload(overlapper)
# from overlapper import Overlapper_UI

# win = Overlapper_UI()
# win.mayaShow()
