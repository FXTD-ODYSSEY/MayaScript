# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-13 14:57:20'

"""
maya 客户端模拟
"""

import os
import sys
import rpyc
import time
import ctypes
import subprocess
from PySide.QtGui import *
from PySide.QtCore import *
# from PySide2.QtWidgets import *

# NOTE https://www.tutorialspoint.com/pyqt/pyqt_qtoolbar_widget.htm

DIR = os.path.dirname(__file__)
class CefWidget(QWidget):
    browser = None
    def __init__(self, parent = None , port=5266):
        super(CefWidget, self).__init__(parent)
        self.port = port

    def embed(self):
        subprocess.Popen('python %s %s %s' % (os.path.join(DIR,"remote.py"), int(self.winIdFixed()),self.port),shell=True)
        self.conn = rpyc.connect('localhost',self.port)  

    def loadUrl(self,url):
        self.conn.root.onLoadUrl(url)  

    def winIdFixed(self):
        # PySide bug: QWidget.winId() returns <PyCObject object at 0x02FD8788>,
        # there is no easy way to convert it to int.
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


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(150,150, 800, 800)

        self.view = CefWidget(self)
        
        m_vbox = QVBoxLayout()
        m_button = QPushButton("Change Url")
        m_button.clicked.connect(lambda:self.view.loadUrl(r"https://www.bilibili.com/"))
        m_button.setMaximumHeight(100)
        
        m_vbox = QVBoxLayout()
        m_vbox.addWidget(m_button)
        m_vbox.addWidget(self.view)
    
        frame = QFrame()
        frame.setLayout(m_vbox)
        self.setCentralWidget(frame)

        self.view.embed()

def main():
   app = QApplication(sys.argv)
   ex = MainWindow()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()