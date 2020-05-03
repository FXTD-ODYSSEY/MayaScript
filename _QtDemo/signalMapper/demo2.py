# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-03 18:13:52'

"""
https://stackoverflow.com/questions/30442158/trouble-understanding-signal-mapper-pyqt
"""

import os
def getGitRepo(p):
    return p if [f for f in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if f == '.git'] else None if os.path.dirname(p) == p else getGitRepo(os.path.dirname(p))
repo = getGitRepo(__file__)

import sys
MODULE = os.path.join(repo,"_vendor","Qt")
sys.path.insert(0,MODULE) if MODULE not in sys.path else None
    

from Qt import QtGui, QtCore , QtWidgets
from functools import partial

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.mapper = QtCore.QSignalMapper(self)
        self.toolbar = self.addToolBar('Foo')
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        for text in 'One Two Three'.split():
            action = QtWidgets.QAction(text, self)
            self.mapper.setMapping(action, text)
            action.triggered.connect(self.mapper.map)
            self.toolbar.addAction(action)
        print (self.mapper.mapped)
        self.mapper.mapped['string'].connect(self.handleButton)
        self.edit = QtWidgets.QLineEdit(self)
        self.setCentralWidget(self.edit)

    def handleButton(self, identifier):
        print ('run',identifier)
        if identifier == 'One':
            text = 'Do This'
            print ('Do One')
        elif identifier == 'Two':
            text = 'Do That'
            print ('Do Two')
        elif identifier == 'Three':
            print ('Do Three')
            text = 'Do Other'
        self.edit.setText(text)

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.resize(300, 60)
    window.show()
    sys.exit(app.exec_())