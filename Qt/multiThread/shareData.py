# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 11:05:12'

"""
https://stackoverflow.com/questions/33081529/in-pyqt-what-is-the-best-way-to-share-data-between-the-main-window-and-a-thread
"""
import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
MODULE = os.path.join(repo,'_vendor','Qt')
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets
import time

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.spinbox = QtWidgets.QSpinBox(self)
        self.spinbox.setValue(1)
        self.layout.addWidget(self.spinbox)
        self.output = QtWidgets.QLCDNumber(self)
        self.layout.addWidget(self.output)

        self.worker = Worker(self.spinbox.value())
        self.worker.beep.connect(self.update)
        self.spinbox.valueChanged.connect(self.worker.update_value)
        self.worker.start()

    def update(self, number):
        self.output.display(number)


class Worker(QtCore.QThread):
    beep=QtCore.Signal(int)

    def __init__(self,sleep_time):
        super(Worker, self).__init__()
        self.running = False
        self.sleep_time=sleep_time

    def run(self):
        self.running = True
        i = 0
        while self.running:
            i += 1
            self.beep.emit(i)
            time.sleep(self.sleep_time)

    def stop(self):
        self.running = False

    def update_value(self,value):
        self.sleep_time=value


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()