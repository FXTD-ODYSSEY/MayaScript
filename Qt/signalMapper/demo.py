# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-03 18:13:52'

"""
https://stackoverflow.com/questions/54155407/how-to-temporary-disconnect-a-pyqt-qsignalmapper
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
class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        # self._mapper = QtCore.QSignalMapper(self)
        vlay = QtWidgets.QVBoxLayout(self)
        checkbox = QtWidgets.QCheckBox("Block Signals")
        checkbox.stateChanged.connect(self.onStateChanged)
        vlay.addWidget(checkbox)
        for i in range(5):
            button = QtWidgets.QPushButton("{}".format(i))
            button.clicked.connect(partial(self.onClicked,"button-{}".format(i)))
            # self._mapper.setMapping(button, "button-{}".format(i))
            vlay.addWidget(button)
        # self._mapper.mapped[str].connect(self.onClicked)

    @QtCore.Slot(int)
    def onStateChanged(self, state):
        self._mapper.blockSignals(state == QtCore.Qt.Checked)

    @QtCore.Slot(str)
    def onClicked(self, text):
        print(text)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())