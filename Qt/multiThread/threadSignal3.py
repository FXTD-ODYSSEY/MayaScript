# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-04 19:45:10'

"""
# NOTE https://stackoverflow.com/questions/4323678/threading-and-signals-problem-in-pyqt
"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time

class MyThread(QThread):
    def __init__(self, name):
        super(MyThread, self).__init__()
        self.setObjectName(name)

    def run(self):
        print "RUN", QThread.currentThread().objectName(), QApplication.instance().thread().objectName()
        self.exec_()
        print "RUN DONE", QThread.currentThread().objectName()

class Producer(QObject):

    testsignal = pyqtSignal(int)
    def __init__(self, parent=None):
        super(Producer, self).__init__(parent)

    def Start(self):
        for i in range(5):
            print "Producer",i,QThread.currentThread().objectName()
            self.testsignal.emit(i)
            time.sleep(2)
        time.sleep(1)
        qApp.quit()

class Consumer(QObject):
    def __init__(self, parent=None):
        super(Consumer, self).__init__(parent)

    def Consume(self, i):
        print "Consumed",i,QThread.currentThread().objectName()

if __name__ == "__main__":
    app = QApplication([])
    producer = Producer()
    consumer = Consumer()
    QThread.currentThread().setObjectName("MAIN")
    producerThread = MyThread("producer")
    consumerThread = MyThread("consumer")
    producer.moveToThread(producerThread)
    consumer.moveToThread(consumerThread)
    producerThread.started.connect(producer.Start)

    # producer.connect(producer, SIGNAL("testsignal"), consumer.Consume)
    producer.testsignal.connect(consumer.Consume)
    def aboutToQuit():
        producerThread.quit()
        consumerThread.quit()
        time.sleep(1)
    qApp.aboutToQuit.connect(aboutToQuit)
    consumerThread.start()
    time.sleep(.1)
    producerThread.start()
    sys.exit(app.exec_())