# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-06 13:46:04'

"""
https://stackoverflow.com/questions/29518069/transpose-proxy-model-doesnt-work-in-pyqt-where-is-an-error
"""

import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
sys.path.insert(0,repo) if repo not in sys.path else None

from Qt import QtGui, QtWidgets, QtCore

# class TransposeModel(QtCore.QAbstractItemModel):
class TransposeModel(QtGui.QStandardItemModel):
    
    def __init__(self, sourceModel):
        super(TransposeModel, self).__init__()
        self.setSourceModel(sourceModel)

    def setSourceModel(self, sourceModel):
        self._sourceModel = sourceModel

    def index(self, row, column, parent=QtCore.QModelIndex()):
        return self.createIndex(row, column)

    def parent(self, index):
        return QtCore.QModelIndex()

    def rowCount(self, parent):
        print ("rowCount",self._sourceModel.columnCount(parent))
        return self._sourceModel.columnCount(parent)

    def columnCount(self, parent):
        return self._sourceModel.rowCount(parent)

    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole :
            if index.isValid():
                return '1'
                item = self._sourceModel.item(index.column(),index.row())
                return item.text() if item else None

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            if index.isValid():
                item = self._sourceModel.item(index.column(),index.row())
                if not item : return False
                item.setText(value)
                self.dataChanged.emit(index, index)
                return True
        return False
        
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

class WidgetTest(QtWidgets.QWidget):

    def __init__(self):
        super(WidgetTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.line = QtWidgets.QLineEdit()
        layout.addWidget(self.line)
        
        #ALL OF OUR VIEWS
        listView = QtWidgets.QListView()
        layout.addWidget(listView)

        treeView = QtWidgets.QTreeView()
        layout.addWidget(treeView)

        comboBox = QtWidgets.QComboBox()

        # print ("dynamicPropertyNames",comboBox.dynamicPropertyNames())
        layout.addWidget(comboBox)

        tableView = QtWidgets.QTableView()
        layout.addWidget(tableView)

        red   = QtGui.QStandardItem("red")
        green   = QtGui.QStandardItem("green")
        blue   = QtGui.QStandardItem("blue")
        item_list = [red, green, blue]
        self.model = QtGui.QStandardItemModel()
        self.model.appendColumn(item_list)
        self.model.appendRow([item.clone() for item in item_list])
        # index = QtCore.QModelIndex().child(0, 0)
        # print("data",self.model.row())
        self.proxy = TransposeModel(self.model)

        listView.setModel(self.proxy)
        treeView.setModel(self.proxy)
        comboBox.setModel(self.proxy)
        tableView.setModel(self.proxy)

        button = QtWidgets.QPushButton("change")
        button.clicked.connect(self.changeOrder)
        layout.addWidget(button)
        button = QtWidgets.QPushButton("change2")
        button.clicked.connect(self.addComboBox)
        layout.addWidget(button)

    def addComboBox(self):
        print (self.state.item_list)
        # import pdb
        # pdb.set_trace()
        self.state.option_B = "BBB"
        # self.model.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        print (self.state.item_list)

    def changeOrder(self):
        self.model.setData([])
        self.model.dataChanged.emit(QtCore.QModelIndex(), QtCore.QModelIndex())
        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    widget = WidgetTest()

    widget.show()
    
    sys.exit(app.exec_())