import os
import sys
import ctypes
import subprocess
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# NOTE https://www.tutorialspoint.com/pyqt/pyqt_qtoolbar_widget.htm

DIR = os.path.dirname(__file__)
class CefWidget(QWidget):
    browser = None
    def __init__(self, parent = None):
        super(CefWidget, self).__init__(parent)
        self.show()
        self.process = QProcess(self)
        # subprocess.Popen(r'F:\py_env\ENV\Scripts\activate & F:\py_env\ENV\Scripts\python.exe %s' % os.path.join(DIR,"cefBrowser.py"))

        window = QWindow.fromWinId(658406)
        window.setFlags(Qt.FramelessWindowHint)

        widget = QWidget.createWindowContainer(window)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(u"test")
        self.button = QPushButton(u"test")
        self.button.clicked.connect(self.printTest)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(widget)
    
    def printTest(self):
        print "test"

def main():
   app = QApplication(sys.argv)
   ex = CefWidget()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()