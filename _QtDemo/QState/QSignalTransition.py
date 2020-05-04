# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-04 12:47:50'

"""
https://stackoverflow.com/questions/55144943/custom-pyqt-signal-never-received-by-qsignaltransition-subclass
"""

import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
MODULE = os.path.join(repo,'_vendor','Qt')
sys.path.insert(0,MODULE) if MODULE not in sys.path else None
from Qt.QtWidgets import *
from Qt.QtCore import *

class Factorial(QObject):
    xChanged = Signal(int)
    def __init__(self):
        super(Factorial, self).__init__()
        self.xval = -1
        self.facval = 1
    def getX(self):
        return self.xval
    def setX(self, x):
        if self.xval == x:
            return
        self.xval = x
        self.xChanged.emit(x)
    x = Property(int, getX, setX)
    def getFact(self):
        return self.facval
    def setFact(self, fac):
        self.facval = fac
    fac = Property(int, getFact, setFact)

class FactorialLoopTransition(QSignalTransition):
    def __init__(self, fact ,signal):
        super(FactorialLoopTransition, self).__init__(signal)
        self.fact = fact
    def eventTest(self, e):
        if not super(FactorialLoopTransition, self).eventTest(e):
            return False
        print ("eventTest",e.arguments())
        return e.arguments()[0] > 1
    def onTransition(self, e):
        x = e.arguments()[0]
        fac = self.fact.fac
        self.fact.fac = x * fac
        self.fact.x = x - 1
        print ("onTransition",self.fact.fac)

class FactorialDoneTransition(QSignalTransition):
    def __init__(self, fact,signal):
        super(FactorialDoneTransition, self).__init__(signal)
        self.fact = fact
    def eventTest(self, e):
        if not super(FactorialDoneTransition, self).eventTest(e):
            return False
        return e.arguments()[0] <= 1
    def onTransition(self, e):
        print(self.fact.fac)

if __name__ == '__main__':
    import sys
    app = QCoreApplication(sys.argv)
    factorial = Factorial()
    machine = QStateMachine()

    compute = QState(machine)
    compute.assignProperty(factorial, 'fac', 1)
    compute.assignProperty(factorial, 'x', 6)
    compute.addTransition(FactorialLoopTransition(factorial,factorial.xChanged))

    done = QFinalState(machine)
    doneTransition = FactorialDoneTransition(factorial,factorial.xChanged)
    doneTransition.setTargetState(done)
    compute.addTransition(doneTransition)

    machine.setInitialState(compute)
    machine.finished.connect(app.quit)
    machine.start()

    sys.exit(app.exec_())