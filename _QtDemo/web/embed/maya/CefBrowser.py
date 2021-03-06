# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-14 23:53:53'

"""

"""


import os
import sys
import time
import ctypes
import subprocess

# from PySide.QtGui import *
# from PySide.QtCore import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

import rpyc

DIR = os.path.dirname(__file__)

class CefWidget(QWidget):
    def __init__(self, parent = None , port=4433):
        super(CefWidget, self).__init__(parent)
        self.port = port
        self._port = port 

    def embed(self,port=None):
        port = int(port) if port else self.port

        cef = os.path.join(DIR,"cefapp")
        cefapp = os.path.join(cef,"cefapp.exe")

        # NOTE 开启 rpyc 服务
        server = os.path.join(cef,"server.exe")
        self.sever_process = subprocess.Popen('"%s" %s' % (server,port),shell=True)

        # self.sever_process = subprocess.Popen('"%s" "%s" %s' % (os.path.join(sys.executable,"..","mayapy.exe"),server,port),shell=True)
        # self.sever_process = subprocess.Popen(' %s %s %s' % (sys.executable,server,port),shell=True)
        try:
            self.conn = rpyc.connect('localhost',port)  
        except:
            if port - self._port < 10:
                self.embed(port=port+1)
            return

        # NOTE 开启 cef 浏览器
        winId = int(self.winIdFixed())
        self.browser_process = subprocess.Popen('"%s" %s %s' % (cefapp,winId,port),shell=True)
        self.window().installEventFilter(self)

    def eventFilter(self,receiver,event):
        if QEvent.Type.Close == event.type() or QEvent.Type.ChildRemoved == event.type():
            print "delete"
            self.conn.root.stop()  
            self.sever_process.terminate()
            self.browser_process.terminate()
            self.deleteLater()
        return False

    def loadUrl(self,url):
        self.conn.root.onLoadUrl(url)  

    def winIdFixed(self):
        try:
            return int(self.winId())
        except:
            if sys.version_info[0] == 2:
                ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
                ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
                return ctypes.pythonapi.PyCObject_AsVoidPtr(self.winId())
            elif sys.version_info[0] == 3:
                ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
                ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
                return ctypes.pythonapi.PyCapsule_GetPointer(self.winId(), None)

    def moveEvent(self, event):
        if hasattr(self,"conn"):
            self.conn.root.onResizeCall()  

    def resizeEvent(self, event):
        if hasattr(self,"conn"):
            self.conn.root.onResizeCall()  


class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(150,150, 800, 800)

        self.view = CefWidget(self)
        
        m_vbox = QVBoxLayout()
        m_button = QPushButton("Change Url")
        m_button.clicked.connect(lambda:self.view.loadUrl(r"http://editor.l0v0.com/"))
        m_button.setMaximumHeight(100)
        
        m_vbox.addWidget(m_button)
        m_vbox.addWidget(self.view)
    
        self.setLayout(m_vbox)

        self.view.embed()

def main():
    # app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    # sys.exit(app.exec_())
    
if __name__ == '__main__':
   main()

# import sys
# MODULE = r"D:\Users\82047\Desktop\repo\MayaScript\_QtDemo\web\embed\maya"
# if MODULE not in sys.path:
#     sys.path.append(MODULE)

# import CefBrowser
# reload(CefBrowser)
# CefBrowser.main()

