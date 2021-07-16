# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-09 22:10:08'

"""
测试阻断 channelbox 的自动更新
"""

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets
from Qt.QtCompat import loadUi
from Qt.QtCompat import wrapInstance
from maya import OpenMayaUI
import maya.cmds as cmds

def mayaToQT(name):
    """
    Maya -> QWidget

    :param str name: Maya name of an ui object
    :return: QWidget of parsed Maya name
    :rtype: QWidget
    """
    ptr = OpenMayaUI.MQtUtil.findControl( name )
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findLayout( name )    
    if ptr is None:         
        ptr = OpenMayaUI.MQtUtil.findMenuItem( name )
    if ptr is not None:     
        return wrapInstance( long( ptr ), QtWidgets.QWidget )



def traverseChildren(parent,childCallback=None,printCallback=None,indent=4,prefix="",log=False):
    """traverseChildren 
    Traverse into the widget children | print the children hierarchy
    
    :param parent: traverse widget
    :type parent: QWidget
    :param indent: indentation space, defaults to ""
    :type indent: str, optional
    :param log: print the data, defaults to False
    :type log: bool, optional
    """

    if callable(printCallback):
        printCallback(prefix,parent)
    elif log:
        event = EventList(parent)
        # print prefix,parent,parent.objectName()
        
    if not hasattr(parent,"children"):
        return

    prefix = "".join([" " for _ in range(indent)]) + prefix
    for child in parent.children():
        traverse_func = lambda:traverseChildren(child,indent=indent,prefix=prefix,childCallback=childCallback,printCallback=printCallback,log=log)
        if callable(childCallback) : 
            childCallback(child,traverse_func)
        else:
            traverse_func()

class EventList(QtCore.QObject):
    def __init__(self,widget):
        super(EventList,self).__init__()
        self.widget = widget
        self.layoutPaint = False
        check = 0
        widget.installEventFilter(self)

        # for i,child in enumerate(widget.children()):
        #     if type(child) is QtWidgets.QWidget:
        #         check += 1
        #     if check == 1:
        #         self.setParent(self)
        #         child.installEventFilter(self)
        #         self.child = child
        #         break

    def eventFilter(self,reciever,event):
        print event.type()
        if event.type() is QtCore.QEvent.LayoutRequest:
            # self.layoutPaint = True
            # print "Timer"
            return True
        elif event.type() is QtCore.QEvent.Paint:
            return True
        return False

cmds.window()
cmds.formLayout( 'form' )
cb = cmds.channelBox( 'dave' )
cmds.formLayout( 'form', e=True, af=(('dave', 'top', 0), ('dave', 'left', 0), ('dave', 'right', 0), ('dave', 'bottom', 0)) )
cmds.showWindow()

channelBox = mayaToQT(cb)
event = EventList(channelBox)
# cmds.channelBox( cb ,e=1,update=True)
# traverseChildren(channelBox,log=True)