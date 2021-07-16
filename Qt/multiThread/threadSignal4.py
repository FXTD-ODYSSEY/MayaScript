# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-02-04 19:45:10'

"""
# NOTE https://stackoverflow.com/questions/4323678/threading-and-signals-problem-in-pyqt
"""
import sys, time
from PyQt5 import QtGui 
from PyQt5 import QtCore 
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
class widget(QtWidgets.QWidget):
    signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)
        # self.button = QtWidgets.QPushButton(u"clicked",self)


    def appinit(self):
        thread = worker(self)
        thread.start()

    def testfunc(self):
        print "clicked"

class worker(QtCore.QThread):

    def __init__(self,widget):
        QtCore.QThread.__init__(self, parent=app)
        self.widget = widget

    def run(self):
        # time.sleep(5)
        print "in thread"
        self.widget.button = QtWidgets.QPushButton(u"clicked",self.widget)
        self.widget.button.setText("hello")
        self.widget.button.clicked.connect(self.widget.testfunc)

def main():
    w = widget()
    w.show()
    w.appinit()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()