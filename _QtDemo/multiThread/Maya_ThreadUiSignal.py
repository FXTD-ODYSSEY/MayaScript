# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-04 15:48:10'

"""

"""

import sys
import time
import threading
from PySide2 import QtCore
from PySide2 import QtWidgets

ui_list = []
def processFunc(runCallback=None):
    button = QtWidgets.QPushButton(u"click")
    ui_list.append(button)
    sys.button = button
    button.clicked.connect(lambda:sys.stdout.write("\nclick\n"))
    QtWidgets.QApplication.processEvents()
    # button.show()

def porcessPyThread(blocking=False):
    thread = threading.Thread(target=processFunc)
    thread.start()
    if blocking:
        thread.join()

if __name__ == "__main__":
    porcessPyThread()
    print "done"