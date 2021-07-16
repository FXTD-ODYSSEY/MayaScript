# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-02 13:28:29'

"""

"""
import os
import sys
repo = (lambda f:lambda p=__file__:f(f,p))(lambda f,p: p if [d for d in os.listdir(p if os.path.isdir(p) else os.path.dirname(p)) if d == '.git'] else None if os.path.dirname(p) == p else f(f,os.path.dirname(p)))()
MODULE = os.path.join(repo,'_vendor','Qt')
sys.path.insert(0,MODULE) if MODULE not in sys.path else None

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

        tableView = QtWidgets.QTableView()
        layout.addWidget(tableView)

        red   = QtGui.QColor(255,0,0)
        green = QtGui.QColor(0,255,0)
        blue  = QtGui.QColor(0,0,255)

        rowCount = 4
        columnCount = 6

        # self.model = QtCore.QStringListModel(["red", "green", "blue"])
        # self.model = TestModel(["red", "green", "blue",True])
        red = QtGui.QStandardItem("red")
        green = QtGui.QStandardItem("green")
        blue = QtGui.QStandardItem("blue")
        self.model = QtGui.QStandardItemModel()
        self.model.appendRow([red.clone(), green.clone(), blue.clone()])
        self._model = QtGui.QStandardItemModel()
        self._model.appendRow([red, green, blue])
        
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
        self.mapper_label.addMapping(self.label, 0 , "text")
        self.mapper_label.toFirst()

        self.mapper.addMapping(self.line, 0)
        self.mapper.toFirst()
        # self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)

        self.line.textChanged.connect(self.changeText)

        self.button = QtWidgets.QPushButton('click')
        self.button.clicked.connect(lambda:self._model.item(0,0).setText("ASD"))
        layout.addWidget(self.button)

        # self.model.itemChange(lambda item:None)
        # print(self.mapper.itemDelegate())

    def changeText(self,text):
        # self.setModel()
        # print (dir(self.model))
        print ("submit",self.mapper.submit())
        # self.line.defocus()
        # QtWidgets.QApplication.postEvent( self.line, QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Enter, QtCore.Qt.NoModifier))

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    widget = WidgetTest()

    widget.show()
    
    sys.exit(app.exec_())