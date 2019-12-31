# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2019-12-28 16:18:26'

"""
初始化动画视窗界面
"""
from maya import cmds
from maya import mel
from maya import OpenMayaUI
from maya import utils

import time
from Qt import QtWidgets
from Qt import QtCore
from Qt.QtCompat import wrapInstance

from functools import partial

ASPECT_RATIO = 1.0/2

def mayaToQT( name ):
    # Maya -> QWidget
    ptr = OpenMayaUI.MQtUtil.findControl( name )
    if ptr is None:     ptr = OpenMayaUI.MQtUtil.findLayout( name )
    if ptr is None:     ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
    if ptr is not None: return wrapInstance( long( ptr ), QtWidgets.QWidget )

def mayaWindow():
    """
    Get Maya's main window.
    
    :rtype: QMainWindow
    """
    window = OpenMayaUI.MQtUtil.mainWindow()
    window = wrapInstance(long(window), QtWidgets.QMainWindow)
    
    return window

class LockResizeWindow(QtWidgets.QDialog):
    def __init__(self):
        super(LockResizeWindow,self).__init__(parent=mayaWindow())

        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinMaxButtonsHint)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        # label = QtWidgets.QLabel("test")
        # layout.addWidget(label)

    def resizeEvent(self,e):
        width = e.size().width()
        rect = self.geometry()
        rect.setWidth(width)
        rect.setHeight(width*ASPECT_RATIO)
        self.setGeometry(rect)

            
# MF_ASPECTRATIO_WIN = LockResizeWindow(parent=mayaWindow())
# MF_ASPECTRATIO_WIN.show()
# MF_ASPECTRATIO_WIN.close()

def main():
    desktop = QtWidgets.QApplication.desktop()
    # NOTE 全局变量确保不会被 垃圾回收
    global MF_ASPECTRATIO_WIN
    cmds.windowPref(enableAll=0)
    for mp in cmds.getPanel(type="modelPanel"):
        if cmds.modelEditor(mp,q=1,av=1):
            ptr = mayaToQT(mp)
            win = ptr.window()
            if win.objectName() == "MayaWindow":
                continue
            
            # NOTE 将原窗口的大小修正到特定比例
            width = win.size().width()
            height = width*ASPECT_RATIO
            if height > desktop.height()/2:
                height = desktop.height()/2
                width = desktop.height()
            win.resize(width,height)

            _panel = cmds.modelPanel(toc=mp)
            panel = mayaToQT(_panel).window()
            MF_ASPECTRATIO_WIN = LockResizeWindow()

            # NOTE 添加新的 Panel
            MF_ASPECTRATIO_WIN.layout().addWidget(panel)

            # NOTE 获取原窗口的数据
            MF_ASPECTRATIO_WIN.setObjectName(win.objectName())
            MF_ASPECTRATIO_WIN.setWindowTitle(win.windowTitle())

            # NOTE 获取原窗口长宽
            MF_ASPECTRATIO_WIN.setGeometry(win.geometry())
            
            MF_ASPECTRATIO_WIN.show()
            win.close()
            break

    cmds.windowPref(enableAll=1)

if __name__ == "__main__":
    main()