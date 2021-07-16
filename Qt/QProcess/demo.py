# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/58846237/pyqt5-how-to-read-write-from-to-a-qprocess
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2020-11-05 17:39:29'


import os
import sys

from PySide2 import QtCore, QtGui, QtWidgets


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget,self).__init__(parent)

        self._textedit = QtWidgets.QTextEdit(readOnly=True)
        self._lineedit = QtWidgets.QLineEdit()
        self._pushbutton = QtWidgets.QPushButton("Send")
        self._pushbutton.clicked.connect(self.on_clicked)

        lay = QtWidgets.QGridLayout(self)
        lay.addWidget(self._textedit, 0, 0, 1, 2)
        lay.addWidget(self._lineedit, 1, 0)
        lay.addWidget(self._pushbutton, 1, 1)

        self._process = QtCore.QProcess(self)
        self._process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self._process.readyRead.connect(self.on_readReady)

        current_dir = os.path.dirname(os.path.realpath(__file__))
        self._process.start(os.path.join(current_dir, "goo"))

    @QtCore.Slot()
    def on_readReady(self):
        cursor = self._textedit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(str(self._process.readAll(), "utf-8"))
        self._textedit.ensureCursorVisible()

    @QtCore.Slot()
    def on_clicked(self):
        text = self._lineedit.text() + "\n"
        self._process.write(text.encode())


if __name__ == "__main__":
    os.environ["PYTHONUNBUFFERED"] = "1"

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())