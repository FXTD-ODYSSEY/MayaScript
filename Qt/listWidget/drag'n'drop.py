# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/4170541
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-09-24 16:12:32"


import sys
from Qt import QtWidgets, QtCore, QtGui


class MainForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = QtGui.QStandardItemModel()

        for k in range(0, 4):
            parentItem = self.model.invisibleRootItem()
            for i in range(0, 4):
                item = QtGui.QStandardItem("item %s %s" % (k, i))
                parentItem.appendRow(item)
                parentItem = item

        self.view = QtWidgets.QTreeView()
        self.view.setModel(self.model)
        self.view.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.setCentralWidget(self.view)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()

