# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-04 11:20:02'

"""
# NOTE https://stackoverflow.com/questions/31844736/in-pyqt-how-to-store-data-emitted-from-signal-in-qrunnable
"""

import sys, time
from random import uniform
from PyQt5 import QtCore, QtGui , QtWidgets


class AWorker(QtCore.QRunnable):
    """ Generic Task for ThreadPool to execute required Kwargs =
    target (<function>): function to call
    args  (tuple): args for target
    kwargs (dict): kwargs for target """  
    def __init__(self, target=None, args=(), kwargs={}):
        super(AWorker, self).__init__()
        self.target = target 
        self.args = args
        self.kwargs = kwargs
    def run(self):
        self.target(*self.args, **self.kwargs)

class myTest(QtCore.QObject):  

    doneSignal = QtCore.pyqtSignal(int)  #Create a signal to emit the data

    def __init__(self):
        super(myTest, self).__init__()        
        self._procData = [] #Place to Store data .. maybe        
        self.pool = QtCore.QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(4) #Use up to 8 threads

    # def runAll(self):
    #     worker = AWorker(target=self.processData)
    #     self.pool.start(worker)
    #     self.pool.waitForDone()
    #     self.eventloop.processEvents() 
    #     self.eventloop.exit()
    #     self.button.show()

    def runAll(self):

        self.doneSignal.connect(self.storeData) 
        for data in range(4):
            worker = AWorker(target=self.processData, args=(data,))
            self.pool.start(worker)
        self.pool.waitForDone()
        QtWidgets.QApplication.processEvents()
        print "finish"
        
        
    def generateUI(self):
        self.button = QtWidgets.QPushButton(u"click")
        self.button.clicked.connect(lambda:sys.stdout.write("click\n"))
        # self.storeData(self.button)

    def processData(self,data):        
        print('Crunching ...', str(data))
        outData = data+10
        time.sleep(uniform(1,3))  #Simulate this taking a random amount of time
        self.doneSignal.emit(outData)

    def storeData(self,data):        
        print('Received ...', str(data))
        self._procData.append(data)

    def getData(self):
        return self._procData

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test = myTest()
    test.runAll()
    # QtWidgets.QApplication.processEvents()
    print('All done ... and the data is: ',test.getData())
    app.exec_()