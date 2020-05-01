# coding:utf-8
from __future__ import division,print_function

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-05-01 21:37:31'

"""
https://stackoverflow.com/questions/30966487/pyqt-qdatawidgetmapper-mapping-for-custom-property
"""


import sys
from PySide2.QtWidgets import QWidget, QLineEdit, QRadioButton, QButtonGroup, QApplication, QVBoxLayout, QGroupBox, QTreeView,QDataWidgetMapper
from PySide2.QtCore import QAbstractItemModel,QModelIndex,Qt,Property,QEvent
from PySide2.QtGui import QKeyEvent

"""Base class to provide some nodes fro a tree
At the moment each node contains two members: name and option"""
class Node(object):

    def __init__(self,name,parent=None):

        self._name = name
        self._children = []
        self._parent = parent
        self._option = 2

        if parent is not None:
            parent.addChild(self)

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def option(self):
        return self._option

    def setOption(self,option):
        self._option = option  

    def addChild(self,child):
        self._children.append(child)

    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False
        child = self._children.pop(position)
        child._parent = None
        return True

    def child(self,row):
        return self._children[row]

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def __repr__(self):
        return  self.log()


class ButtonGroupWidget(QGroupBox):
    def __init__(self, parent=None):
        super(ButtonGroupWidget, self).__init__(parent)
        self._selectedOption = -1
        self.buttonGroup = QButtonGroup()
        self.layoutGroupBox = QVBoxLayout(self)

    def addRadioButton(self,optionText,optionId):
        print(optionText)
        radioButton = QRadioButton(optionText)
        radioButton.clicked.connect(self.updateOptionSelected)
        self.layoutGroupBox.addWidget(radioButton)
        self.buttonGroup.addButton(radioButton,optionId)

    def updateOptionSelected(self):
        # print(self.buttonGroup.checkedId()) # for test purpose
        # self.selectedOption = self.buttonGroup.checkedId()
        # print(self._selectedOption) # for test purpose
        self.selectedOption = self.buttonGroup.checkedId()
        QApplication.postEvent(  self, QKeyEvent(QEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier))

    def getSelectedOption(self):
        print("get selectedOption is called")
        return self._selectedOption

    def setSelectedOption(self,selectedOption):
        print("set selectedOption is called")
        self._selectedOption = selectedOption
        self.buttonGroup.button(selectedOption).setChecked(True)

    selectedOption = Property(int,getSelectedOption,setSelectedOption)


class DataModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(DataModel, self).__init__(parent)
        self._rootNode = Node("Root Node")
        childNode1 = Node("Child 1",self._rootNode)
        childNode2 = Node("Child 2",self._rootNode)
        childNode3 = Node("Child 3",self._rootNode)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def isNull(self):
        nullObject = DataModel()
        if self.__eq__(nullObject):
            return True
        else:
            return False

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()

    def columnCount(self, parent):
        return 1

    def data(self,index,role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == 0:
                return node.name()
            if index.column() == 1:
                return node.option()

    def setData(self,index,value, role=Qt.EditRole):
        if index.isValid():
            node = index.internalPointer()
            if role == Qt.EditRole:
                if index.column() == 0:
                    node.setName(value)
                if index.column() == 1:
                    node.setOption(value)
                self.dataChanged.emit(index,index)
                return True            
        return False   

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if section == 0:
                return "Select Child"

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def parent(self, index):
        node = index.internalPointer()
        parentNode = node.parent()
        if parentNode == self._rootNode:
            return QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):

        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

class MainWidget(QWidget):

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        # define tree view
        self.treeView = QTreeView(self)

        # insert line edit
        self.lineEdit1 = QLineEdit(self)
        self.lineEdit2 = QLineEdit(self)

        # insert a button group widget
        self.buttonGroupWidget1 = ButtonGroupWidget(self)
        self.buttonGroupWidget1.setTitle("Select option")
        self.buttonGroupWidget1.addRadioButton("Option 1", 1)
        self.buttonGroupWidget1.addRadioButton("Option 2", 2)
        self.buttonGroupWidget1.addRadioButton("Option 3", 3)

        layoutMain = QVBoxLayout(self)
        layoutMain.addWidget(self.treeView)
        layoutMain.addWidget(self.lineEdit1)
        layoutMain.addWidget(self.lineEdit2)
        layoutMain.addWidget(self.buttonGroupWidget1)

        # Create the data model and map the model to the widgets.
        self._model = DataModel()
        self.treeView.setModel(self._model)

        self._dataMapper = QDataWidgetMapper()
        self._dataMapper.setModel(self._model)
        # the mapping works fine for line edits and combo boxes
        self._dataMapper.addMapping(self.lineEdit1, 0)
        self._dataMapper.addMapping(self.lineEdit2, 1)
        # mapping to custom property
        self._dataMapper.addMapping(self.buttonGroupWidget1,1,"selectedOption")

        self.treeView.selectionModel().currentChanged.connect(self.setSelection)

    def setSelection(self, current):

        parent = current.parent()
        self._dataMapper.setRootIndex(parent)
        self._dataMapper.setCurrentModelIndex(current) 


def main():
    app = QApplication(sys.argv)
    form = MainWidget()
    form.show()
    app.exec_()

main() 