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
        line.setValidator(QtGui.QIntValidator())
        label = QtWidgets.QLabel()

        layout.addWidget(line)
        layout.addWidget(label)

        machine = QtCore.QStateMachine(self)
        input_state = QtCore.QState()
        input_state.assignProperty(label, 'text', 'key press...')
        default_state = QtCore.QState()
        default_state.assignProperty(label, 'text', 'nothing...')

        enterTransition = QtCore.QEventTransition(line, QtCore.QEvent.KeyRelease)
        enterTransition.setTargetState(default_state)
        input_state.addTransition(enterTransition)
        # input_state.addTransition(line.textChanged,default_state)

        leaveTransition = QtCore.QEventTransition(line, QtCore.QEvent.KeyPress)
        leaveTransition.setTargetState(input_state)
        default_state.addTransition(leaveTransition)
        # default_state.addTransition(line.textChanged,input_state)

        machine.addState(input_state)
        machine.addState(default_state)
        machine.setInitialState(default_state)
        machine.start()

        # line.textChanged.connect(lambda text:print(text))

        button = QtWidgets.QPushButton()
        layout.addWidget(button)
        machine = QtCore.QStateMachine(self)

        off = QtCore.QState()
        off.assignProperty(button, 'text', 'Off')
        off.setObjectName('off')

        on = QtCore.QState()
        on.setObjectName('on')
        on.assignProperty(button, 'text', 'On')

        off.addTransition(button.clicked, on)
        # Let's use the new style signals just for the kicks.
        on.addTransition(button.clicked, off)

        machine.addState(off)
        machine.addState(on)
        machine.setInitialState(off)
        machine.start()
        button.resize(100, 50)
        
        # textChange.addTransition(line.textChanged, default)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = InputTest()
    widget.show()
    sys.exit(app.exec_())
