# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-11-26 16:18:54'


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DockDemo(QMainWindow):
    def __init__(self,parent=None):
        super(DockDemo, self).__init__(parent)
        bar=self.menuBar()
        file=bar.addMenu('File')
        file.addAction('New')
        file.addAction('Save')
        file.addAction('quit')

        self.items=QDockWidget('Dockable',self)
        print(dir(QDockWidget))
        self.listWidget=QListWidget()
        self.listWidget.addItem('Item1')
        self.listWidget.addItem('Item2')
        self.listWidget.addItem('Item3')
        self.listWidget.addItem('Item4')

        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)
        self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea,self.items)

        self.setWindowTitle('Dock')

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=DockDemo()
    demo.show()
    sys.exit(app.exec_())