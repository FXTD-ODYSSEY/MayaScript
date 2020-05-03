# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-03 17:13:33'

"""

"""

import os
def getGitRepo(p):
    return p if [f for f in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if f == '.git'] else None if os.path.dirname(p) == p else getGitRepo(os.path.dirname(p))
repo = getGitRepo(__file__)

import sys
MODULE = os.path.join(repo,"_vendor","Qt")
if MODULE not in sys.path:
    sys.path.insert(0,MODULE)

from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

class InputTest(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(InputTest,self).__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)

        line = QtWidgets.QLineEdit()
        label = QtWidgets.QLabel()

        layout.addWidget(line)
        layout.addWidget(label)

        machine = QtCore.QStateMachine(self)
        textChange = QtCore.QState()
        textChange.assignProperty(label, 'text', 'key press...')
        default = QtCore.QState()
        textChange.assignProperty(label, 'text', 'nothing...')

        # enterTransition = QtCore.QEventTransition(line, QtCore.QEvent.HoverLeave)
        # enterTransition.setTargetState(default)
        # textChange.addTransition(enterTransition)

        leaveTransition = QtCore.QEventTransition(line, QtCore.QEvent.KeyPress)
        leaveTransition.setTargetState(textChange)
        default.addTransition(leaveTransition)

        machine.addState(textChange)
        machine.addState(default)
        machine.setInitialState(default)
        machine.start()
        # textChange.addTransition(line.textChanged, default)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = InputTest()
    widget.show()
    # button = QtWidgets.QPushButton()
    # machine = QtCore.QStateMachine()

    # off = QtCore.QState()
    # off.assignProperty(button, 'text', 'Off')
    # off.setObjectName('off')

    # on = QtCore.QState()
    # on.setObjectName('on')
    # on.assignProperty(button, 'text', 'On')

    # off.addTransition(button.clicked, on)
    # # Let's use the new style signals just for the kicks.
    # on.addTransition(button.clicked, off)

    # machine.addState(off)
    # machine.addState(on)
    # machine.setInitialState(off)
    # machine.start()
    # button.resize(100, 50)
    # button.show()
    sys.exit(app.exec_())
