# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/21997090/pyqt-qt4-how-to-add-a-tiny-arrow-collapse-button-to-qsplitter
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-05-31 15:53:13'


from Qt import QtCore,QtWidgets

class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.addWidget(QtWidgets.QTextEdit(self))
        self.splitter.addWidget(QtWidgets.QTextEdit(self))
        self.splitter.setHandleWidth(10)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.splitter)
        handle = self.splitter.handle(1)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        button = QtWidgets.QToolButton(handle)
        button.setArrowType(QtCore.Qt.LeftArrow)
        button.clicked.connect(
            lambda: self.handleSplitterButton(True))
        layout.addWidget(button)
        button = QtWidgets.QToolButton(handle)
        button.setArrowType(QtCore.Qt.RightArrow)
        button.clicked.connect(
            lambda: self.handleSplitterButton(False))
        layout.addWidget(button)
        handle.setLayout(layout)

    def handleSplitterButton(self, left=True):
        if not all(self.splitter.sizes()):
            self.splitter.setSizes([1, 1])
        elif left:
            self.splitter.setSizes([0, 1])
        else:
            self.splitter.setSizes([1, 0])

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 300, 300)
    window.show()
    sys.exit(app.exec_())