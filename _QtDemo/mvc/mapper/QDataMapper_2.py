# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-02 13:28:29'

"""

"""

import os
import sys
MODULE = os.path.join(__file__,"..","..","..","_vendor","Qt")
if MODULE not in sys.path:
    sys.path.append(MODULE)

from Qt import QtCore,QtWidgets,QtGui

# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-29 13:34:11'

"""

"""

import os
import sys
DIR = os.path.dirname(__file__)
MODULE = os.path.join(DIR,"..","..","QMVVM","_vender")
if MODULE not in sys.path:
    sys.path.insert(0,MODULE)

import Qt
from Qt import QtGui,QtWidgets, QtCore
from functools import partial
# class TestModel (QtCore.QAbstractListModel):

#     def __init__(self, data = None, parent = None):
#         super(TestModel,self).__init__( parent)
#         self._data = data if hasattr(data,"__iter__") else [data]

#     def rowCount(self, index):
#         return len(self._data)

#     def data(self, index, role):
#         val = self._data[index.row()] if len(self._data) > index.row() else next(iter(self._data), '')

#         if role == QtCore.Qt.DisplayRole:
#             return str(val)
#         elif role == QtCore.Qt.EditRole:
#             return self._data[index.row()]

#     def setData(self,index,value, role=QtCore.Qt.EditRole):
#         if index.isValid():
#             if role == QtCore.Qt.EditRole:
#                 self._data[index.row()] = value
#                 self.dataChanged.emit(index,index)
#                 return True            
#         return False   

#     def flags(self, index):
#         return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

# class TestLabel(QtWidgets.QLabel):
#     def __init__(self,parent=None):
#         super(TestLabel, self).__init__(parent)
    
#     def getString(self):
#         print("getString call")
#         return self.text()

#     def setString(self,text):
#         self.setText(text)

#     text2 = QtCore.Property(str,lambda *args:"asd",setString)

class WidgetTest(QtWidgets.QWidget):
    def __init__(self):
        super(WidgetTest, self).__init__()
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        #ALL OF OUR VIEWS
        listView = QtWidgets.QListView()
        layout.addWidget(listView)

        treeView = QtWidgets.QTreeView()
        layout.addWidget(treeView)

        comboBox = QtWidgets.QComboBox()
        layout.addWidget(comboBox)
        comboBox.addItem("0")
        comboBox.addItem("1")
        comboBox.addItem("2")
        comboBox.addItem("3")
        comboBox.addItem("4")

        tableView = QtWidgets.QTableView()
        layout.addWidget(tableView)

        red   = QtGui.QColor(255,0,0)
        green = QtGui.QColor(0,255,0)
        blue  = QtGui.QColor(0,0,255)

        rowCount = 4
        columnCount = 6

        # self.model = QtCore.QStringListModel(["red", "green", "blue"])
        # self.model = TestModel(["red", "green", "blue",True])
        self.model = QtGui.QStandardItemModel()
        self.model.appendRow([QtGui.QStandardItem("red"), QtGui.QStandardItem("green"), QtGui.QStandardItem("blue")])
        self.model.appendColumn([QtGui.QStandardItem("red"), QtGui.QStandardItem("green"), QtGui.QStandardItem("blue")])
        
        listView.setModel(self.model)
        comboBox.setModel(self.model)
        tableView.setModel(self.model)
        treeView.setModel(self.model)

        self.mapper = QtWidgets.QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper_label = QtWidgets.QDataWidgetMapper()
        self.mapper_label.setModel(self.model)
        # self.mapper.setItemDelegate(self.model)


        self.label = QtWidgets.QLabel(self)
        layout.addWidget(self.label)
        self.line = QtWidgets.QLineEdit()
        layout.addWidget(self.line)

        # NOTE https://stackoverflow.com/questions/28114655/qdatawidgetmapper-not-working-with-qlabels
        self.mapper_label.addMapping(self.label, 1 , "text")
        self.mapper_label.toFirst()

        self.mapper.addMapping(self.line, 0)
        self.mapper.toFirst()
        # self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)

        self.line.textChanged.connect(self.changeText)

        self.button = QtWidgets.QPushButton('click')
        self.button.clicked.connect(lambda:self.model.item(0,0).setText("ASD"))
        layout.addWidget(self.button)

        # self.model.itemChange(lambda item:None)
        # print(self.mapper.itemDelegate())

    def changeText(self,text):
        # self.setModel()
        print (self.line.text())
        print ("submit",self.mapper.submit())
        # self.line.defocus()
        # QtWidgets.QApplication.postEvent( self.line, QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Enter, QtCore.Qt.NoModifier))

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    widget = WidgetTest()

    widget.show()
    
    sys.exit(app.exec_())