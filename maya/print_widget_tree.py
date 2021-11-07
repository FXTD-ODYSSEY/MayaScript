# -*- coding: utf-8 -*-
"""
print all widget tree in maya
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-10-03 17:30:21'


import os
from codecs import open
from functools import partial
import pymel.core as pm
from maya import cmds 
from maya import mel 
from maya import OpenMayaUI

from PySide2 import QtGui, QtWidgets, QtCore
from shiboken2 import wrapInstance

path = r"D:\repo\MayaScript\maya\tree.txt"

def maya_to_qt(name):
    # Maya -> QWidget
    ptr = OpenMayaUI.MQtUtil.findControl(name)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findLayout(name)
    if ptr is None:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(name)
    if ptr is not None:
        return wrapInstance(int(ptr), QtWidgets.QWidget)

def mayaWindow():
    """
    Get Maya's main window.
    
    :rtype: QMainWindow
    """
    window = OpenMayaUI.MQtUtil.mainWindow()
    window = wrapInstance(int(window), QtWidgets.QMainWindow)
    return window
    
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
        print (prefix,parent)
        
    if not hasattr(parent,"children"):
        return

    prefix = "".join([" " for _ in range(indent)]) + prefix
    for child in parent.children():
        traverse_func = lambda:traverseChildren(child,indent=indent,prefix=prefix,childCallback=childCallback,printCallback=printCallback,log=log)
        if callable(childCallback) : 
            childCallback(child,traverse_func)
        else:
            traverse_func()

def iterate_widget(f,p,w):
    name = ""
    if hasattr(w,"text"):
        name = w.text()
    
    # if name == "New...":
    #     w.setEnabled(True)
    
    f.write(u"%s%s %s\n" % (p,w,name))


def output_widget_tree(mel_global="$gMainWindow"):
    # NOTES(timmyliang) 清空脚本
    with open(path,'w') as f:
        f.write("")
    
    widget_name = pm.melGlobals[mel_global]
    print(widget_name)
    with open(path,'a',encoding="utf-8") as f:
        traverseChildren(maya_to_qt(widget_name),printCallback=partial(iterate_widget,f))

if __name__ == "__main__":
    output_widget_tree("gToolBox")