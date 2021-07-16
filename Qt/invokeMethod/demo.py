# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-03 19:15:23'

"""
https://stackoverflow.com/questions/23538904/qmetaobjectinvokemethod-doesnt-find-methods-with-parameters
https://programtalk.com/vs2/?source=python/9670/openshot-qt/src/windows/views/blender_treeview.py
"""


import os
def getGitRepo(p):
    return p if [f for f in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if f == '.git'] else None if os.path.dirname(p) == p else getGitRepo(os.path.dirname(p))
repo = getGitRepo(__file__)

import sys
MODULE = os.path.join(repo,"_vendor","Qt")
sys.path.insert(0,MODULE) if MODULE not in sys.path else None


from Qt import QtCore
# NOTE PySide & PySide2 seem not support
from PyQt5.QtCore import Q_ARG
class Example(QtCore.QObject):
    def __init__(self):
        super(Example,self).__init__()

    @QtCore.Slot()
    def dup(self):
        beep('dup-class')

    @QtCore.Slot(str)
    def beep(self, text):
        print(text)

@QtCore.Slot()
def dup(self):
    beep('dup-local')

@QtCore.Slot(str)
def beep(text):
    print(text)

if __name__ == '__main__':
    # print (QtCore.QMetaObject.invokeMethod(None, 'dup'))
    # QtCore.QMetaObject.invokeMethod(None, 'beep', QtCore.Qt.AutoConnection, QtCore.QGenericArgument('text', 'beep-local'))

    print('now some classy trials')
    t = Example()
    # QtCore.QMetaObject.invokeMethod(t, 'dup')
    print(QtCore.QMetaObject.invokeMethod(t, 'beep', QtCore.Qt.AutoConnection, Q_ARG(str, 'beep132')))
    print ("asdasd")
    # QtCore.QMetaObject.invokeMethod(t, 'beep', QtCore.Qt.AutoConnection, QtCore.QGenericArgument('self', t), QtCore.QGenericArgument('text', 'beep-class-b'))


