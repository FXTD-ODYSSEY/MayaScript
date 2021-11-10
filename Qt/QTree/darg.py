# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/4170541
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-11-08 16:14:40'

import sys
from Qt import QtGui, QtCore,QtWidgets

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self):
        QtCore.QAbstractItemModel.__init__(self)
        self.nodes = ['node0', 'node1', 'node2']

    def index(self, row, column, parent):
        return self.createIndex(row, column, self.nodes[row])

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, index):
        if index.internalPointer() in self.nodes:
            return 0
        return len(self.nodes)

    def columnCount(self, index):
        return 1

    def data(self, index, role):
        if role == 0: 
            return index.internalPointer()
        else:
            return None

    def supportedDropActions(self): 
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction         

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | \
               QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled        

    def mimeTypes(self):
        return ['text/xml']

    def mimeData(self, indexes):
        mimedata = QtCore.QMimeData()
        mimedata.setData('text/xml', b'mimeData')
        return mimedata

    def dropMimeData(self, data, action, row, column, parent):
        print ('dropMimeData %s %s %s %s' % (data.data('text/xml'), action, row, parent) )
        return True


class MainForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.treeModel = TreeModel()

        self.view = QtWidgets.QTreeView()
        self.view.setModel(self.treeModel)
        self.view.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.setCentralWidget(self.view)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()