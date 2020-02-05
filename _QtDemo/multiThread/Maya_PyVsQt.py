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

def processFunc(runCallback=None):
    curr = time.time()
    while True:
        elapsed = abs(time.time() - curr)
        if elapsed%0.5 < 0.001:
            if runCallback:
                runCallback(elapsed)
        if elapsed > 3:
            break
        
class Worker(QtCore.QRunnable):

    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        processFunc(lambda t: sys.stdout.write("QtThread: %s \n" % t))


def processQtThread(blocking=False):
    thread = QtCore.QThreadPool()
    thread.start(Worker())
    if blocking:
        thread.waitForDone()

    return thread

def porcessPyThread(blocking=False):
    thread = threading.Thread(target=processFunc,kwargs={"runCallback":lambda t: sys.stdout.write("PyThread: %s \n" % t)})
    thread.start()
    if blocking:
        thread.join()

if __name__ == "__main__":
    # NOTE 避免垃圾回收
    thread = processQtThread()
    # porcessPyThread()
    print "done"