# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-04 11:08:54'

"""
# NOTE https://stackoverflow.com/questions/30676599/emitting-signals-from-a-python-thread-using-qobject?rq=1
"""

import sys, time, threading
from PyQt5 import QtCore, QtWidgets

def thread_info(msg):
    print(msg, int(QtCore.QThread.currentThreadId()),
          threading.current_thread().name)

class PyThreadObject(QtCore.QObject):
    sig = QtCore.pyqtSignal()

    def start(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.start()

    def run(self):
        time.sleep(1)
        thread_info('py:run')
        self.sig.emit()

class QtThreadObject(QtCore.QThread):
    sig = QtCore.pyqtSignal()

    def run(self):
        time.sleep(1)
        thread_info('qt:run')
        self.sig.emit()

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.pyobj = PyThreadObject()
        self.pyobj.sig.connect(self.pyslot)
        self.pyobj.start()
        self.qtobj = QtThreadObject()
        self.qtobj.sig.connect(self.qtslot)
        self.qtobj.start()

    def pyslot(self):
        thread_info('py:slot')

    def qtslot(self):
        thread_info('qt:slot')

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(600, 100, 300, 200)
    window.show()
    thread_info('main')
    sys.exit(app.exec_())