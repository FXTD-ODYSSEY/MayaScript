# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-04 17:18:16'

"""
# NOTE https://stackoverflow.com/questions/20075368/pyqt-qthread-blocking-main-thread
"""

import time
from PyQt5 import QtCore, QtGui , QtWidgets
import sys
application = QtWidgets.QApplication(sys.argv)

class LoadThread (QtCore.QObject):
    results = QtCore.pyqtSignal(tuple)

    def __init__ (self, arg):
         # Init QObject
         super(QtCore.QObject, self).__init__()

         # Store the argument
         self.arg = arg

    def load(self):
        #
        # Some heavy lifting is done
        #
        print "run"
        time.sleep(5)
        loaded = True
        errors = []
        print "done"
        # Emits the results
        self.results.emit((loaded, errors))

l = LoadThread("test")

class MyThread(QtCore.QThread):
    run = l.load

thread = MyThread()

button = QtWidgets.QPushButton("Do 5 virtual push-ups")
button.clicked.connect(thread.start)
button.show()
l.results.connect(lambda:button.setText("Phew! Push ups done"))
application.exec_()