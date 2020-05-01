# coding:utf-8

__author__ =  'timmyliang'
__email__ =  '820472580@qq.com'
__date__ = '2020-04-29 13:34:11'

"""
https://www.youtube.com/watch?v=AONvtOcpaws&list=PL8B63F2091D787896
"""

import os
import sys

from PySide2 import QtGui,QtWidgets, QtCore
from functools import partial

class PaletteListModel(QtCore.QAbstractListModel):
    
    def __init__(self, colors = [], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__colors = colors

    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                return"Palette"
            else:
                return "Color %s" % section

    def rowCount(self, parent):
        return len(self.__colors)


    def data(self, index, role):
        
        
        if role == QtCore.Qt.EditRole:
            return self.__colors[index.row()].name()
        
        
        if role == QtCore.Qt.ToolTipRole:
            return "Hex code: " + self.__colors[index.row()].name()
        

        if role == QtCore.Qt.DecorationRole:
            
            row = index.row()
            value = self.__colors[row]
            
            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(value)
            
            icon = QtGui.QIcon(pixmap)
            
            return icon

              
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            value = self.__colors[row]
            
            return value.name()

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            
            row = index.row()
            color = QtGui.QColor(value)
            
            if color.isValid():
                self.__colors[row] = color
                self.dataChanged.emit(index, index)
                return True
        return False


    #=====================================================#
    #INSERTING & REMOVING
    #=====================================================#
    def insertRows(self, position, rows,parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            self.__colors.insert(position, QtGui.QColor("#000000"))
        
        self.endInsertRows()
        
        return True


    
    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for i in range(rows):
            value = self.__colors[position]
            self.__colors.remove(value)
             
        self.endRemoveRows()
        return True
    
class TestModel (QtCore.QAbstractListModel):

    def __init__(self, data = None, parent = None):
        super(TestModel,self).__init__( parent)
        self._data = data if data else []

    def rowCount(self, index):
        return len(self._data)

    def data(self, index, role):
        # NOTE https://stackoverflow.com/questions/5125619/why-doesnt-list-have-safe-get-method-like-dictionary
        val = self._data[index.row()] if len(self._data) > index.row() else next(iter(self._data), '')

        if role == QtCore.Qt.DisplayRole:
            return val

    def setData(self,data):
        self._data = data

    def getData(self):
        return self._data

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

        self.model = PaletteListModel([red, green, blue])

        listView.setModel(self.model)
        comboBox.setModel(self.model)
        tableView.setModel(self.model)
        treeView.setModel(self.model)

        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)

    widget = WidgetTest()


    widget.show()
    
    sys.exit(app.exec_())