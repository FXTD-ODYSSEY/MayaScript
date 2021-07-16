# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 16:13:47'

"""

"""

import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
MODULE = os.path.join(repo,'_vendor','Qt')
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

from Qt import QtGui
from Qt import QtCore
from Qt import QtWidgets

class Ui_MainWindow(object):

    def connect(self):
        self.updateWindow=QtWidgets.QDialog()
        self.ui_update=Ui_Dialog()
        self.ui_update.setupUi(self.updateWindow)
        self.updateWindow.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(("MainWindow"))
        MainWindow.resize(391, 248)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(("centralwidget"))
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(80, 60, 113, 27))
        self.lineEdit.setObjectName(("lineEdit"))
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 100, 112, 34))
        self.pushButton.setObjectName(("pushButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 391, 31))
        self.menubar.setObjectName(("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None))
        self.pushButton.setText(QtWidgets.QApplication.translate("MainWindow", "B1", None))
        self.pushButton.clicked.connect(self.connect)

class Ui_Dialog(object):

    def save_data(self):
        d= self.lineEdit.text()
        print(d)

    def setupUi(self, Dialog):
        Dialog.setObjectName(("Dialog"))
        Dialog.resize(397, 219)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(110, 100, 112, 34))
        self.pushButton.setObjectName(("pushButton"))
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(110, 60, 113, 27))
        self.lineEdit.setText((""))
        self.lineEdit.setObjectName(("lineEdit"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None))
        self.pushButton.setText(QtWidgets.QApplication.translate("Dialog", "B2", None))
        self.pushButton.clicked.connect(self.save_data)
        
class Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.close)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.onClicked)

    def onClicked(self):
        updateDialog = Dialog()
        updateDialog.exec_()
        self.lineEdit.setText(updateDialog.lineEdit.text())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())