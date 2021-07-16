# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-16 20:47:39'

"""
导出 atom 动画 修复动画文件的 IFKK 切换跳动问题
"""

import os
import re
import tempfile

from maya import mel
import pymel.core as pm
import pymel.core.nodetypes as nt

from maya import OpenMayaUI

try:
    from Qt import QtGui
    from Qt import QtCore
    from Qt import QtWidgets
    from Qt.QtCompat import wrapInstance,QFileDialog
except:
    from PySide2 import QtGui
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance
    from PySide2.QtWidgets import QFileDialog



class IMouseClickSignal(QtCore.QObject):
    """IMouseClickSignal 监听鼠标点击信号
    """
    
    # NOTE 点击事件
    LClicked   = QtCore.Signal(QtCore.QEvent)

    def __init__(self,widget):
        super(IMouseClickSignal,self).__init__()
        self.setParent(widget)

        widget.installEventFilter(self)

    def eventFilter(self,reciever,event):
        if event.type() == QtCore.QEvent.Type.MouseButtonPress:
            self.LClicked.emit(event)

        return False

class AtomFixIKFK_UI(QtWidgets.QWidget):

    def __init__(self):
        super(AtomFixIKFK_UI, self).__init__()
        self.setWindowTitle(u"IKFK 切换修复工具")
        layout = QtWidgets.QVBoxLayout(self)
        

        self.label = QtWidgets.QLabel(u"选择绑定引用节点")
        self.combo = QtWidgets.QComboBox()
        self.button = QtWidgets.QPushButton(u"一键修复")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.combo.setSizePolicy(sizePolicy)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.label)
        h_layout.addWidget(self.combo)
        layout.addLayout(h_layout)
        layout.addWidget(self.button)

        self.updateCombo()

        signal = IMouseClickSignal(self)
        signal.LClicked.connect(self.updateCombo)

        self.button.clicked.connect(self.atomFixIKFK)

    def updateCombo(self):
        self.combo.clear()
        self.combo.addItems(["%s -> %s" % (ref.refNode,ref) for ref in pm.listReferences()])

    def mayaShow(self,name=None):
        name = self.__class__.__name__ if name is None else name
        # NOTE 如果变量存在 就检查窗口多开
        if pm.workspaceControl(name,q=1,ex=1):
            pm.deleteUI(name)
        window = pm.workspaceControl(name,label=self.windowTitle())
        pm.showWindow(window)
        # NOTE 将Maya窗口转换成 Qt 组件
        ptr = self.mayaToQT(window)
        ptr.setLayout(QtWidgets.QVBoxLayout())
        ptr.layout().setContentsMargins(0,0,0,0)
        ptr.layout().addWidget(self)
        return ptr
    
    @staticmethod
    def mayaToQT( name ):
        # Maya -> QWidget
        ptr = OpenMayaUI.MQtUtil.findControl( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findLayout( name )
        if ptr is None:     ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
        if ptr is not None: return wrapInstance( long( ptr ), QtWidgets.QWidget )


    def atomFixIKFK(self):
            
        # # NOTE 获取时间滑块
        # env = pm.language.Env()
        # playBackTimes = env.getPlaybackTimes()

        # ref_list = pm.listReferences()
        # if len(ref_list) != 1:
        #     raise RuntimeError(u"存在多个参考或没有参考")
        self.updateCombo()
        currentText = self.combo.currentText()

        for ref_node in pm.listReferences():
            ref_path = ref_node.path
            if "%s -> %s" % (ref_node.refNode,ref_node) == currentText:
                break
        else:
            raise RuntimeError(u"存在多个参考或没有参考")

        namespace = ref_node.namespace
        # namespace = os.path.splitext(os.path.basename(ref_path))[0]
        # NOTE 加载 Atom 插件
        if not pm.pluginInfo('atomImportExport', q=True, loaded=True):
            pm.loadPlugin('atomImportExport')
            
        # NOTE 保存当前文件
        pm.saveFile()

        # NOTE 选择所有带关键帧的控制器
        ctrl_list = {node for crv in pm.ls(type="animCurve") for node in crv.listConnections() if type(node) is nt.Transform}
        pm.select(ctrl_list)
        ctrl_list = [str(ctrl) for ctrl in ctrl_list]

        atom_file = os.path.join(tempfile.gettempdir(),"IKFK_Fix.atom").replace("\\","/")
        mel.eval("""
        file -force -options "precision=8;statics=1;baked=1;sdk=0;constraint=0;animLayers=1;selected=selectedOnly;whichRange=1;range=1:10;hierarchy=none;controlPoints=0;useChannelBox=1;options=keys;copyKeyCmd=-animation objects -option keys -hierarchy none -controlPoints 0 " -typ "atomExport" -es "%s";
        """ % atom_file)

        # NOTE 去除当前参考
        ref_node.remove()

        pm.createReference(ref_path,r=1,namespace=namespace)

        # print([ctrl.fullPathName() for ctrl in ctrl_list])
        pm.select(ctrl_list)

        mel.eval("""
        file -import -type "atomImport" -ra true -options ";;targetTime=3;option=insert;match=hierarchy;;selected=selectedOnly;" "%s";
        """ % atom_file)


if __name__ == "__main__":
    AtomFixIKFK_win = AtomFixIKFK_UI()
    AtomFixIKFK_win.mayaShow()
