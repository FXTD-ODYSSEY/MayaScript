#!/usr/bin/env python
# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-03-13 10:51:36'

"""
https://stackoverflow.com/questions/29112349/how-to-use-a-terminal-embedded-in-a-pyqt-gui
"""

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class embeddedTerminal(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self._processes = []
        self.resize(800, 600)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self._start_process(
            'xterm',
            ['-into', str(self.terminal.winId()),
             '-e', 'tmux', 'new', '-s', 'my_session']
        )
        button = QPushButton('List files')
        layout.addWidget(button)
        button.clicked.connect(self._list_files)

    def _start_process(self, prog, args):
        child = QProcess()
        self._processes.append(child)
        child.start(prog, args)

    def _list_files(self):
        self._start_process(
            'tmux', ['send-keys', '-t', 'my_session:0', 'ls', 'Enter'])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = embeddedTerminal()
    main.show()
    sys.exit(app.exec_())