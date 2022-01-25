# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/53108545/optional-signal-arguments
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2022-01-02 19:35:03'

# Import built-in modules
import sys

# Import third-party modules
from dayu_widgets.qt import application

# Import local modules
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets


class SignalContainer(QtCore.QObject):
    
    test_signal = QtCore.Signal([str,str],[str,str,int])
    
    def __init__(self,*args,**kwargs):
        super(SignalContainer, self).__init__(*args,**kwargs)
        self.test_signal[str,str].connect(self.call)
        self.test_signal[str,str,int].connect(self.call)
    
    def call(self,name,char,index=1):
        print("name: ",name)
        print("char: ",char)
        print("index: ",index)



with application():
    container = SignalContainer()
    container.test_signal.emit("test","asd",2)
    container.test_signal[str,str].emit("test","asd")
    sys.exit(0)

