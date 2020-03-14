import sys
import os
import ctypes

from PySide.QtGui import *
from PySide.QtCore import *
from cefpython3 import cefpython

class CefWidget(QWidget):
    browser = None
    def __init__(self, parent = None):
        super(CefWidget, self).__init__(parent)
        self.show()
        self.createTimer()

    def createTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(10)

    def onTimer(self):
        cefpython.MessageLoopWork()

    def embed(self):
        #it needs to be called after setupping the layout,
        windowInfo = cefpython.WindowInfo()
        windowInfo.SetAsChild(int(self.winIdFixed()))
        self.browser = cefpython.CreateBrowserSync(windowInfo,
                                                   browserSettings={},
                                                   navigateUrl="https://blog.l0v0.com/my_work/OPENGL_homework/old_Method/")
                                                #    navigateUrl="https://threejs.org/editor/")
                                                #    navigateUrl="http://editor.l0v0.com/")
                                                #    navigateUrl="https://get.webgl.org/")

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
        cefpython.WindowUtils.OnSize(int(self.winIdFixed()), 0, 0, 0)

    def resizeEvent(self, event):
        cefpython.WindowUtils.OnSize(int(self.winIdFixed()), 0, 0, 0)



class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(150,150, 800, 800)

        self.view = CefWidget(self)
        
        m_vbox = QVBoxLayout()
        m_label = QLabel("Another Widget")
        m_label.setMaximumHeight(100)
        
        m_vbox = QVBoxLayout()
        m_vbox.addWidget(m_label)
        m_vbox.addWidget(self.view)
    
        #Do not use it
        #m_vbox.insertStretch(-1, 1)
        
        frame = QFrame()
        frame.setLayout(m_vbox)
        self.setCentralWidget(frame)

        #it needs to be called after setupping the layout 
        self.view.embed()

if __name__ == "__main__":

    settings = {}
    settings["browser_subprocess_path"] = "%s/%s" % (
        cefpython.GetModuleDirectory(), "subprocess")
    settings["context_menu"] = {
        "enabled": False,
        "navigation": False,  # Back, Forward, Reload
        "print": False,
        "view_source": False,
        "external_browser": False,  # Open in external browser
        "devtools": False,  # Developer Tools
    }

    cefpython.Initialize(settings)

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()
  