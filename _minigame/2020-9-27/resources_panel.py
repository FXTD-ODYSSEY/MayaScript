# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-02 21:16:58'

"""
将本文件拖拽到 Maya 视窗即可完成安装
"""

import os
import sys
import json
import shutil
import hashlib
import tempfile
import traceback

from maya import cmds
from maya import mel
from maya.app.general import mayaMixin

import pymel.core as pm
import pymel.core.nodetypes as nt

from maya import OpenMayaUI


from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from PySide2.QtWidgets import QFileDialog
from PySide2.QtUiTools import QUiLoader

from textwrap import dedent

def errorLog(func):
    def wrapper(*args, **kwargs):
        res = None
        try:
            res = func(*args, **kwargs)
            return res
        except:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(QtWidgets.QApplication.activeWindow(),u"错误", "未知错误\n%s" %traceback.format_exc())
    return wrapper


class MinigameExporterBase(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(362, 201)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Output_Path = QtWidgets.QLineEdit(Form)
        self.Output_Path.setObjectName("Output_Path")
        self.horizontalLayout.addWidget(self.Output_Path)
        self.Output_BTN = QtWidgets.QPushButton(Form)
        self.Output_BTN.setObjectName("Output_BTN")
        self.horizontalLayout.addWidget(self.Output_BTN)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Export_BTN = QtWidgets.QPushButton(Form)
        self.Export_BTN.setObjectName("Export_BTN")
        self.verticalLayout.addWidget(self.Export_BTN)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.Transparent_BTN = QtWidgets.QPushButton(Form)
        self.Transparent_BTN.setObjectName("Transparent_BTN")
        self.verticalLayout.addWidget(self.Transparent_BTN)
        self.Center_BTN = QtWidgets.QPushButton(Form)
        self.Center_BTN.setObjectName("Center_BTN")
        self.verticalLayout.addWidget(self.Center_BTN)
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.Playblast_BTN = QtWidgets.QPushButton(Form)
        self.Playblast_BTN.setObjectName("Playblast_BTN")
        self.verticalLayout.addWidget(self.Playblast_BTN)
        self.Export_FBX_BTN = QtWidgets.QPushButton(Form)
        self.Export_FBX_BTN.setObjectName("Export_FBX_BTN")
        self.verticalLayout.addWidget(self.Export_FBX_BTN)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "输出路径", None, -1))
        self.Output_BTN.setText(QtWidgets.QApplication.translate("Form", "选择路径", None, -1))
        self.Export_BTN.setText(QtWidgets.QApplication.translate("Form", "选择物体导出", None, -1))
        self.Export_FBX_BTN.setText(QtWidgets.QApplication.translate("Form", "导出 FBX 文件", None, -1))
        self.Transparent_BTN.setText(QtWidgets.QApplication.translate("Form", "修复材质透明", None, -1))
        self.Center_BTN.setText(QtWidgets.QApplication.translate("Form", "原点居中", None, -1))
        self.Playblast_BTN.setText(QtWidgets.QApplication.translate("Form", "批量拍屏截图", None, -1))
        
class MinigameExporter(MinigameExporterBase,mayaMixin.MayaQWidgetBaseMixin,QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(MinigameExporter, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Minigame Maya 资源导出工具")
        
        self.Output_BTN.clicked.connect(self.browse_path)
        self.Export_BTN.clicked.connect(self.export)
        self.Transparent_BTN.clicked.connect(self.transparent_material)
        self.Center_BTN.clicked.connect(self.center_model)
        self.Playblast_BTN.clicked.connect(self.batch_playblast)
        
        self.Export_FBX_BTN.clicked.connect(self.export_fbx)
        

    def show(self):
        for win in QtWidgets.QApplication.topLevelWidgets():
            if self.__class__.__name__ in str(type(win)):
                win.close()
        super(MinigameExporter, self).show()
    
    def browse_path(self,directory=""):
        directory = directory if directory else QFileDialog.getExistingDirectory(self)
        if not os.path.exists(directory):
            return
        self.Output_Path.setText(directory)

    def export(self):
        output_path = self.Output_Path.text()
        if not os.path.exists(output_path):
            self.Output_Path.setText("")
            msg = u"路径不存在"
            QtWidgets.QMessageBox.warning(self,u"警告",msg)
            return
        
        base_name = os.path.basename(output_path)

        sel_list = pm.ls(sl=1)
        if not sel_list:
            msg = u"请选择一个物体"
            QtWidgets.QMessageBox.warning(self,u"警告",msg)
            return
        for sel in sel_list:
            pm.undoInfo(ock=1)

            pm.parent(sel,w=1)
            # NOTE 居中轴心
            pm.xform(sel,cp=1)

            pm.mel.BakeCustomPivot()
            sel.t.set(0,0,0)
            sel.r.set(0,0,0)

            x,_,z = pm.xform(sel,q=1,rp=1)
            bbox = pm.exactWorldBoundingBox(sel)
            pm.xform(sel,piv=[x,bbox[1],z])
            sel.t.set(0,-bbox[1],0)
            pm.makeIdentity(apply=1,t=1,r=1,s=1,n=0,pn=0)
            
            index = 1
            path = os.path.join(output_path,"%s_%s.ma" % (base_name,str(index).zfill(2)))
            while os.path.exists(path):
                index += 1
                path = os.path.join(output_path,"%s_%s.ma" % (base_name,str(index).zfill(2)))

            path = path.replace('\\','/')
            print(path)
            # commnad = 'FBXExport -f "%s.fbx" -s ' % path.replace('\\','/')
            # NOTE 导出 ma 文件
            pm.mel.file(path,f=1,options="v=0;",typ="mayaAscii",pr=1,es=1)
            pm.undoInfo(cck=1)
            
            pm.undo()
    
    def center_model(self):
        sel_list = pm.ls(sl=1)
        sel = sel_list[0]

        pm.parent(sel,w=1)
        # NOTE 居中轴心
        pm.xform(sel,cp=1)

        pm.mel.BakeCustomPivot()
        sel.t.set(0,0,0)
        sel.r.set(0,0,0)

        x,_,z = pm.xform(sel,q=1,rp=1)
        bbox = pm.exactWorldBoundingBox(sel)
        pm.xform(sel,piv=[x,bbox[1],z])
        sel.t.set(0,-bbox[1],0)
        pm.makeIdentity(apply=1,t=1,r=1,s=1,n=0,pn=0)
    
    def transparent_material(self):
        for sel in pm.ls(sl=1):
            shape = sel.getShape()
            for shading in shape.shadingGroups():
                for mat in shading.connections():
                    if not isinstance(mat,nt.ShadingDependNode):
                        continue
                    f = mat.color.connections()
                    if not f:
                        continue
                    f = f[0]
                    try:
                        f.outTransparency.connect(mat.transparency)
                    except:
                        pass
    
    def batch_playblast(self):
        file_list,_ = QFileDialog.getOpenFileNames(self)
        for f in file_list:
            if not f.endswith(".ma") and not f.endswith(".mb") :
                continue
            
            pm.openFile(f,f=1)
            png = "%s.png" % os.path.splitext(pm.sceneName())[0]

            pm.playblast(completeFilename=png,
                        format="image",
                        sequenceTime=0,
                        frame=[1],
                        clearCache=1,
                        viewer=0,
                        showOrnaments=0,
                        percent=100,
                        compression="png",
                        quality=100,
                        forceOverwrite=1)

    def export_fbx(self):
        file_list,_ = QFileDialog.getOpenFileNames(self)
        if not file_list:
            return
        export_path = os.path.dirname(file_list[0])
        for ma in file_list:
            f = ma.lower()
            if not f.endswith(".ma"):
                continue
            cmds.file(ma,o=1,f=1)
            
            base = os.path.basename(ma)
            name = os.path.splitext(base)[0]
            pm.mel.FBXExport(f= os.path.join(export_path,name))

@errorLog
def onMayaDroppedPythonFile(*args):
    parentTab = mel.eval('''global string $gShelfTopLevel;string $shelves = `tabLayout -q -selectTab $gShelfTopLevel`;''')
    py_path = __file__[:-1] if __file__.endswith(".pyc") else __file__
    pm.shelfButton( commandRepeatable = True, image1 = "commandButton.png",iol = "export" ,label = "Minigame Export Window", parent = parentTab, 
        command = dedent(ur"""
        import os
        path = r"%s"
        if os.path.exists(path):
            try:
                exec(open(path).read())
            except:
                QtWidgets.QMessageBox.warning(self,u"警告",u"执行错误\n请重新安装")
        else:
            QtWidgets.QMessageBox.warning(self,u"警告",u"脚本路径不存在\n请重新安装")
    """ % py_path))
    show()

@errorLog
def show():
    global MinigameExporter_ui
    MinigameExporter_ui = MinigameExporter()
    MinigameExporter_ui.show()
    
if __name__ == "__main__":
    show()
