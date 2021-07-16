# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-14 17:03:59'

"""
https://stackoverflow.com/questions/53461496/trying-to-get-qprocess-to-work-with-a-queue
https://stackoverflow.com/questions/51364552/how-do-i-queue-qprocesses-in-pyqt5
"""

import Queue
from PySide2 import QtCore, QtGui, QtWidgets


class TaskManager(QtCore.QObject):
    messageChanged = QtCore.Signal(str)
    numbersTaskRunningChanged = QtCore.Signal(int)
    finished = QtCore.Signal()

    def __init__(self, parent=None):
        super(TaskManager, self).__init__(parent)
        self._max_task = 1
        self._queue = Queue.Queue()
        self._numbers_task_running = 0
        self._running = False

    def setMaxTask(self, max_task):
        self._max_task = max_task
        if self._running:
            self.call_task()

    def maxTask(self):
        return self._max_task

    def appendTask(self, task):
        self._queue.put(task)
        self.call_task()

    def start(self):
        self._running = True
        self.call_task()

    def stop(self):
        self._running = False

    def call_task(self):
        if self._numbers_task_running < self.maxTask() and not self._queue.empty() and self._running:
            cmd = self._queue.get()
            process = QtCore.QProcess(self)
            process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
            process.readyReadStandardOutput.connect(self.on_readyReadStandardOutput)
            process.finished.connect(self.on_finished)
            process.started.connect(self.on_started)
            process.errorOccurred.connect(self.on_errorOccurred)
            process.start(cmd)

    def on_readyReadStandardOutput(self):
        codec = QtCore.QTextCodec.codecForLocale()
        decoder_stdout = codec.makeDecoder()
        process = self.sender()
        text = decoder_stdout.toUnicode(process.readAllStandardOutput())
        self.messageChanged.emit(text)

    def on_errorOccurred(self, error):
        process = self.sender()
        print("error: ", error, "-", " ".join([process.program()] + process.arguments()))
        self.call_task()

    def on_finished(self):
        process = self.sender()
        self._numbers_task_running -= 1
        self.numbersTaskRunningChanged.emit(self._numbers_task_running)
        self.call_task()
        print(self._numbers_task_running)
        if self._numbers_task_running == 0:
            self.finished.emit()

    def on_started(self):
        process = self.sender()
        print("started: ", " ".join([process.program()] + process.arguments()))
        self._numbers_task_running += 1
        self.numbersTaskRunningChanged.emit(self._numbers_task_running)
        self.call_task()

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        manager = TaskManager(self)
        task_list = ['subst','ipconfig','taskkill','cscript']
        for task in task_list:
            manager.appendTask(task)

        button_start = QtWidgets.QPushButton("Start", clicked=manager.start)
        button_stop = QtWidgets.QPushButton("Stop", clicked=manager.stop)
        label = QtWidgets.QLabel("0", alignment=QtCore.Qt.AlignCenter)
        manager.numbersTaskRunningChanged.connect(label.setNum)
        spinBox = QtWidgets.QSpinBox()
        spinBox.valueChanged.connect(manager.setMaxTask)
        spinBox.setValue(3)
        textEdit = QtWidgets.QTextEdit()
        manager.messageChanged.connect(textEdit.append)
        manager.finished.connect(lambda:sys.stdout.write('complete'))

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(spinBox)
        lay.addWidget(button_start)
        lay.addWidget(button_stop)
        lay.addWidget(label)
        lay.addWidget(textEdit)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())