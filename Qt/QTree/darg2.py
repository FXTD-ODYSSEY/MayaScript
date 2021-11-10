# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/a/40421386
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
        self.nodes = ['node0', 'node1', 'node2', 'node3', 'node4', 'node5']

    def index(self, row, column, parent):
        if row < 0 or row >= len(self.nodes):
            return QtCore.QModelIndex()
        return self.createIndex(row, column, self.nodes[row])

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, index):
        if index.isValid():
            return 0
        if index.internalPointer() in self.nodes:
            return 0
        return len(self.nodes)

    def columnCount(self, index):
        if index.isValid():
            return 0
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
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

    def insertRows(self, row, count, index):
        if index.isValid():
            return False
        if count <= 0:
            return False
        # inserting 'count' empty rows starting at 'row'
        self.beginInsertRows(QtCore.QModelIndex(), row, row + count - 1)
        for i in range(0, count):
            self.nodes.insert(row + i, '')
        self.endInsertRows()
        return True

    def removeRows(self, row, count, index):
        if index.isValid():
            return False
        if count <= 0:
            return False
        num_rows = self.rowCount(QtCore.QModelIndex())
        self.beginRemoveRows(QtCore.QModelIndex(), row, row + count - 1)
        for i in range(count, 0, -1):
            self.nodes.pop(row - i + 1)
        self.endRemoveRows()
        return True

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if index.row() < 0 or index.row() > len(self.nodes):
            return False
        self.nodes[index.row()] = str(value)
        self.dataChanged.emit(index, index)

    def mimeTypes(self):
        return ['application/vnd.treeviewdragdrop.list']

    def mimeData(self, indexes):
        mimedata = QtCore.QMimeData()
        encoded_data = QtCore.QByteArray()
        stream = QtCore.QDataStream(encoded_data, QtCore.QIODevice.WriteOnly)
        for index in indexes:
            if index.isValid():
                text = self.data(index, 0)
                stream << text
        mimedata.setData('application/vnd.treeviewdragdrop.list', encoded_data)
        return mimedata

    def dropMimeData(self, data, action, row, column, parent):
        if action == QtCore.Qt.IgnoreAction:
            return True
        if not data.hasFormat('application/vnd.treeviewdragdrop.list'):
            return False
        if column > 0:
            return False

        num_rows = self.rowCount(QtCore.QModelIndex())

        begin_row = 0
        if row != -1:
            begin_row = row
        elif parent.isValid():
            begin_row = parent.row()
        else:
            begin_row = num_rows

        if begin_row != num_rows and begin_row != 0:
            begin_row += 1

        encoded_data = data.data('application/vnd.treeviewdragdrop.list')
        stream = QtCore.QDataStream(encoded_data, QtCore.QIODevice.ReadOnly)
        new_items = []
        rows = 0
        while not stream.atEnd():
            text = ""
            stream >> text
            new_items.append("asd")
            rows += 1

        # insert the new rows for the dropped items and set the data to these items appropriately
        self.insertRows(begin_row, rows, QtCore.QModelIndex())
        for text in new_items:
            idx = self.index(begin_row, 0, QtCore.QModelIndex())
            self.setData(idx, text, 0)
            self.dataChanged.emit(idx, idx)
            begin_row += 1

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