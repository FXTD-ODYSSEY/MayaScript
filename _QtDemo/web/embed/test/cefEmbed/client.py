import os
import sys
import ctypes
from PySide.QtGui import *
from PySide.QtCore import *
# from PySide2.QtWidgets import *

# NOTE https://www.tutorialspoint.com/pyqt/pyqt_qtoolbar_widget.htm

DIR = os.path.dirname(__file__)
class CefWidget(QWidget):
    browser = None
    def __init__(self, parent = None):
        super(CefWidget, self).__init__(parent)
        self.show()
        self.process = QProcess()
        self.process.start('python',[os.path.join(DIR,"browser.py"), str(int(self.winIdFixed()))])

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(u"test")
        self.button = QPushButton(u"test")
        self.button.clicked.connect(self.getWidgetChildren)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

    def getWidgetChildren(self):
        for child in self.window().children():
            print child

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

    # def moveEvent(self, event):
    #     cefpython.WindowUtils.OnSize(int(self.winIdFixed()), 0, 0, 0)

    # def resizeEvent(self, event):
    #     cefpython.WindowUtils.OnSize(int(self.winIdFixed()), 0, 0, 0)


def main():
   app = QApplication(sys.argv)
   ex = CefWidget()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()