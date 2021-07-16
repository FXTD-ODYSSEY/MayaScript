# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from OverLay import Filter


class MyApp(QWidget):
    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        self.text = "hello world"
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Draw Demo')

        self.btn = QPushButton("Butten should be overlayed", self)
        self.btn.setFixedSize(200, 200)
        self.btn.move(40, 40)
        filt = Filter(self)
        self.installEventFilter(filt)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())