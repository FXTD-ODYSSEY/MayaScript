# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-04 19:45:10'

"""
# NOTE https://stackoverflow.com/questions/23317195/pyqt-movetothread-does-not-work-when-using-partial-for-slot
"""
# import pyqtgraph as pg

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from functools import partial
from Queue import Queue
import math
import time
import sys

class Worker(QtCore.QObject):

    termino = QtCore.pyqtSignal()

    def __init__(self, q=None, parent=None):
        super(Worker, self).__init__(parent) 
        self.q = q

    def run(self, m=30000):
        print('worker thread id: {}'.format(QtCore.QThread.currentThreadId()))
        for x in xrange(m):
            #y = math.sin(x)
            y = x**2
            #time.sleep(0.001) # Weird, plotting stops if this is not present...
            self.q.put((x,y,y))
        print('Worker finished')

        self.termino.emit()

class MainWindow(QtWidgets.QWidget):

    relay = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.q = Queue()
        self.termino = False       

        self.worker = Worker(self.q)

        self.workerThread = None
        self.btn = QtWidgets.QPushButton('Start worker')
        # self.pw = pg.PlotWidget(self)
        # pi = self.pw.getPlotItem()
        # pi.enableAutoRange('x', True)
        # pi.enableAutoRange('y', True)
        # self.ge1 = pi.plot(pen='y')
        self.xs = []
        self.ys = []

        layout = QtWidgets.QVBoxLayout(self)
        # layout.addWidget(self.pw)
        layout.addWidget(self.btn)

        self.resize(400, 400)

    def run(self):
        self.workerThread = QtCore.QThread()
        self.worker.termino.connect(self.setTermino)
        self.worker.moveToThread(self.workerThread)
        # moveToThread doesn't work here
        # self.btn.clicked.connect(partial(self.worker.run, 30000))
        # moveToThread will work here
        # assume def worker.run(self): instead of def worker.run(self, m=30000)
        #self.btn.clicked.connect(self.worker.run)        
        self.relay.connect(self.worker.run)
        self.btn.clicked.connect(self.relay_signal)
        self.btn.clicked.connect(self.graficar)

        self.workerThread.start()
        self.show()

    def relay_signal(self):
        self.relay.emit(500)

    def setTermino(self):
        self.termino = True

    def graficar(self):
        if not self.q.empty():
            e1,e2,ciclos = self.q.get()       
            self.xs.append(ciclos)
            self.ys.append(e1)
            # self.ge1.setData(y=self.ys, x=self.xs)

        if not self.termino or not self.q.empty():
            QtCore.QTimer.singleShot(1, self.graficar)

if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    window = MainWindow()

    QtCore.QTimer.singleShot(0, window.run)
    sys.exit(app.exec_())